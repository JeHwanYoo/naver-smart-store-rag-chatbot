import re
from typing import List, Dict

from scripts.preprocessing import load_pickle, compress_pickle, remove_unnecessary_words


def extract_related_title(pkl: List[Dict]) -> List[Dict]:
    """
    PKL 데이터의 'content'에서 'related_titles'를 추출합니다.
    추출 기준:
    - '\n관련 도움말/키워드'부터 '\n도움말 닫기'까지의 내용을 '\n'으로 구분하여 리스트로 반환.

    :param pkl: (List[Dict]) 'title'과 'content'를 포함한 데이터 리스트.
    :return: (List[Dict]) 'title', 'content', 'related_titles'를 포함한 데이터 리스트.
    """

    def extract_titles(content: str) -> List[str]:
        match = re.search(r'\n관련 도움말/키워드(.*?)\n도움말 닫기', content, re.DOTALL)
        if match:
            return [title.strip() for title in match.group(1).split('\n') if title.strip()]
        return []

    return [
        {'title': item['title'], 'content': item['content'], 'related_titles': extract_titles(item['content'])}
        for item in pkl
    ]


if __name__ == '__main__':
    pkl = load_pickle('../faq/final_result.pkl')
    compressed_pkl = compress_pickle(pkl)
    tiny_pkl = remove_unnecessary_words(compressed_pkl)
    structured_pkl = extract_related_title(tiny_pkl)
    print([x for x in structured_pkl if len(x.get('related_titles')) > 0])
