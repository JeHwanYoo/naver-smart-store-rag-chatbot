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


def store_in_chromadb(data: List[Dict], host: str, port: int, collection_name: str):
    """
    데이터를 ChromaDB에 저장하고, 저장된 문서의 개수를 출력합니다.
    - 'title'과 'related_titles'는 메타데이터로 저장합니다.
    - 'content'는 텍스트 문서로 저장합니다.

    :param data: (List[Dict]) 저장할 데이터 리스트.
                 각 딕셔너리는 'title', 'content', 'related_titles'를 포함해야 합니다.
    :param host: (str) ChromaDB 서버의 호스트명.
    :param port: (int) ChromaDB 서버의 포트 번호.
    :param collection_name: (str) ChromaDB 컬렉션 이름.
    """
    client = chromadb.HttpClient(host=host, port=port)
    collection = client.get_or_create_collection(
        collection_name,
        embedding_function=openai_ef,
    )
    existing_ids = set(collection.get()['ids'])

    for idx, item in enumerate(data):
        doc_id = f'doc_{idx}'
        # 이미 저장한 데이터는 스킵
        if doc_id in existing_ids:
            print(f'진행도 {idx + 1}/{len(data)} [스킵]')
            continue
        else:
            metadata = {'title': item['title'], 'related_titles': ','.join(item['related_titles'])}
            collection.add(ids=[doc_id], documents=[item['content']], metadatas=[metadata])
            print(f'진행도 {idx + 1}/{len(data)}')

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
    pkl = load_pickle('../faq/final_result.pkl')
    compressed_pkl = compress_pickle(pkl)
    tiny_pkl = remove_unnecessary_words(compressed_pkl)
    structured_pkl = extract_related_title(tiny_pkl)
    store_in_chromadb(structured_pkl, host='localhost', port=8000, collection_name='faq')
