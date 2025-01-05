import os
from typing import List

import chromadb
import chromadb.utils.embedding_functions.openai_embedding_function as embedding_functions

from naver_smart_store_rag_chatbot.domain.entities.document import Document
from naver_smart_store_rag_chatbot.domain.interfaces.services.vector_db_service import VectorDBService

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPEN_AI_KEY'),
    model_name='text-embedding-3-small',
    dimensions=1536,
)


class ChromaDBVectorDBService(VectorDBService):
    async def find_related_documents(self, user_message: str, limit=5) -> List[Document]:
        client = chromadb.HttpClient(
            host=os.getenv('CHROMA_HOST'),
            port=int(os.getenv('CHROMA_PORT')),
        )

        coll = client.get_collection('faq', embedding_function=openai_ef)

        query_result = coll.query(
            query_texts=[user_message],
            n_results=limit,
        )

        chroma_ids = query_result['ids'][0]
        chroma_documents = query_result['documents'][0]
        chroma_metadatas = query_result['metadatas'][0]

        documents: List[Document] = []

        doc_idx_map = {}
        for i, metadata in enumerate(chroma_metadatas):
            d_idx = metadata.get('doc_idx')
            if d_idx:
                doc_idx_map[d_idx] = i

        def follow_chain(start_doc_idx: str) -> dict:
            if not start_doc_idx or start_doc_idx.strip() == '':
                return {'content': '', 'related_titles': []}

            content_parts = []
            related_titles_parts = []

            current_doc_idx = start_doc_idx

            while True:
                index = doc_idx_map[current_doc_idx]

                content_parts.append(chroma_documents[index])
                related_titles = chroma_metadatas[index].get('related_titles', '')
                if related_titles:
                    related_titles_parts.extend(related_titles.split(','))

                next_idx = chroma_metadatas[index].get('next')
                if not next_idx or next_idx.strip() == '':
                    break

                current_doc_idx = next_idx

            return {
                'content': ' '.join(content_parts),
                'related_titles': list(set(related_titles_parts)),
            }

        for idx, doc in enumerate(chroma_documents):
            doc_idx = chroma_metadatas[idx].get('doc_idx')
            merged_data = follow_chain(doc_idx)

            documents.append(
                Document(
                    id=chroma_ids[idx],
                    title=chroma_metadatas[idx].get('title'),
                    content=merged_data['content'],
                    related_titles=merged_data['related_titles'],
                )
            )

        return documents
