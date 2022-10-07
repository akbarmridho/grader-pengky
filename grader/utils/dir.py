import os
from pathlib import Path
from typing import List


def get_files(folder: str):

    result: List[str] = []
    test_path = Path(os.getcwd()).joinpath(folder)

    for file in os.listdir(test_path):
        if file.endswith('.py'):
            result.append(test_path.joinpath(file).__str__())

    return result
