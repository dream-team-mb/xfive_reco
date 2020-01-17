import pickle
from typing import List


class Reco:
    def __init__(self, file_path: str = None):
        if file_path:
            with open(file_path, 'rb') as f:
                self.model = pickle.load(f)['estimator']

    def recommend(self, user_items: List[str]) -> List[int]:
        return user_items

    @staticmethod
    def train(input_file: str, output_file: str):
        with open(output_file, 'wb') as f:
            pickle.dump({'estimator': None}, f)
