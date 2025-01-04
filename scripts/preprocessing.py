import pickle
import re
from typing import Dict, List


def load_pickle(path: str) -> List[Dict]:
    """
    피클 파일을 읽어 'title'과 'content' 필드를 포함한 리스트로 반환합니다.
    각 필드의 공백을 제거합니다.

    :param path: (str) 피클 파일 경로.
    :return: (List[Dict]) 'title'과 'content' 필드를 가진 딕셔너리 리스트.
    """
    with open(path, 'rb') as f:
        return [{'title': k.strip(), 'content': v.strip()} for k, v in pickle.load(f).items()]


def compress_pickle(pkl: List[Dict]) -> List[Dict]:
    """
    PKL 데이터를 정리합니다:
    - 연속적인 공백을 하나의 공백으로 축소.
    - 연속적인 개행 문자를 하나의 개행 문자로 축소.
    - 특수 문자 (\xa0, \u200b 등)를 제거.

    :param pkl: (List[Dict]) 'title'과 'content'를 포함한 데이터 리스트.
    :return: (List[Dict]) 정리된 데이터 리스트.
    """

    def clean_text(text: str) -> str:
        if not isinstance(text, str):
            return ''
        text = re.sub(r'[\u200b\xa0]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    return [{'title': clean_text(item.get('title')), 'content': clean_text(item.get('content'))} for item in pkl]


def remove_unnecessary_words(pkl: List[Dict]) -> List[Dict]:
    """
    'content' 필드에서 불필요한 문구를 제거합니다.

    :param pkl: (List[Dict]) 'title'과 'content'를 포함한 데이터 리스트.
    :return: (List[Dict]) 불필요한 문구가 제거된 데이터 리스트.
    """
    return [
        {
            'title': item.get('title'),
            'content': item.get('content')
            .replace(
                '\n위 도움말이 도움이 되었나요?\n별점1점\n별점2점\n별점3점\n별점4점\n별점5점\n소중한 의견을 남겨주시면 보완하도록 노력하겠습니다.\n보내기',
                '',
            )
            .strip(),
        }
        for item in pkl
    ]


if __name__ == '__main__':
    pkl = load_pickle('../faq/final_result.pkl')
    compressed_pkl = compress_pickle(pkl)
    tiny_pkl = remove_unnecessary_words(compressed_pkl)
    print(tiny_pkl)
