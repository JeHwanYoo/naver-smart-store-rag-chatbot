import os
from typing import List, Dict

import chromadb
import chromadb.utils.embedding_functions.openai_embedding_function as embedding_functions
from dotenv import load_dotenv

from scripts.preprocessing import load_pickle, compress_pickle, remove_unnecessary_words
from scripts.structuring import extract_related_title

load_dotenv()

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPEN_AI_KEY'),
    model_name='text-embedding-3-small',
    dimensions=1536,
)


def store_in_chromadb(
    data: List[Dict],
    host: str,
    port: int,
    collection_name: str,
    chunk_size: int = 8192,
    overlap_size: int = 512,
):
    """
    데이터를 ChromaDB에 저장하고, 오버랩 방식을 사용하여 문서를 나눕니다.
    각 슬라이스에 'prev', 'next' 메타데이터를 추가합니다.

    :param data: (List[Dict]) 저장할 데이터 리스트.
                 각 딕셔너리는 'title', 'content', 'related_titles'를 포함해야 합니다.
    :param host: (str) ChromaDB 서버의 호스트명.
    :param port: (int) ChromaDB 서버의 포트 번호.
    :param collection_name: (str) ChromaDB 컬렉션 이름.
    :param chunk_size: (int) 슬라이스 크기 (기본값: 8192).
    :param overlap_size: (int) 슬라이스 간 오버랩 크기 (기본값: 512).
    """
    client = chromadb.HttpClient(host=host, port=port)
    collection = client.get_or_create_collection(
        collection_name,
        embedding_function=openai_ef,
    )

    existing_ids = set(collection.get()['ids'])

    for idx, item in enumerate(data):
        doc_id_base = f'doc_{idx}'
        document = item['content']
        metadata = {
            'title': item['title'],
            'related_titles': ','.join(item['related_titles']),
        }

        # 문서를 슬라이스로 나눔 (오버랩 포함)
        chunks = []
        for i in range(0, len(document), chunk_size - overlap_size):
            chunks.append(document[i : i + chunk_size])

        for chunk_idx, chunk in enumerate(chunks):
            doc_id = f'{doc_id_base}' if chunk_idx == 0 else f'{doc_id_base}_{chunk_idx}'

            if doc_id in existing_ids:
                print(f'진행도 {idx + 1}/{len(data)} - {chunk_idx + 1}/{len(chunks)} [스킵]')
                continue

            metadata['doc_idx'] = doc_id_base
            metadata['next'] = f'{doc_id_base}_{chunk_idx + 1}' if chunk_idx < len(chunks) - 1 else ''

            collection.add(ids=[doc_id], documents=[chunk], metadatas=[metadata])
            print(f'진행도 {idx + 1}/{len(data)} - {chunk_idx + 1}/{len(chunks)}')

    print(f'컬렉션 "{collection_name}"에 저장된 문서 개수: {collection.count()}')


def clear_collection(host: str, port: int, collection_name: str):
    """
    지정된 ChromaDB 컬렉션의 모든 데이터를 삭제합니다.
    컬렉션이 존재하지 않는 경우 적절한 메시지를 출력합니다.

    :param host: (str) ChromaDB 서버의 호스트명.
    :param port: (int) ChromaDB 서버의 포트 번호.
    :param collection_name: (str) ChromaDB 컬렉션 이름.
    """
    client = chromadb.HttpClient(host=host, port=port)
    try:
        client.delete_collection(collection_name)
        print(f'컬렉션 "{collection_name}"의 모든 데이터가 삭제되었습니다.')
    except Exception as e:
        if 'Collection faq does not exist.' in str(e):
            print(f'컬렉션 "{collection_name}"이 존재하지 않습니다.')
        else:
            print(f'컬렉션 삭제 중 오류 발생: {e}')


if __name__ == '__main__':
    # clear_collection(host='localhost', port=8000, collection_name='faq')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(script_dir, '../faq/final_result.pkl')
    pkl = load_pickle(pkl_path)
    compressed_pkl = compress_pickle(pkl)
    tiny_pkl = remove_unnecessary_words(compressed_pkl)
    structured_pkl = extract_related_title(tiny_pkl)
    store_in_chromadb(structured_pkl, host='localhost', port=8000, collection_name='faq')
