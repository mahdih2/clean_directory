import shutil
import sys
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.util.io import read_json


class CleanDirectory:

    def __init__(self):
        self.ext_read = read_json(DATA_DIR / 'extracton.json')

    def __call__(self, directory: Union[str, Path]):
        directory = Path(directory)

        for file_path in directory.iterdir():

            if file_path.is_dir():
                continue

            if file_path.name.startswith('.'):
                continue

            for key, value in self.ext_read.items():
                if file_path.suffix in value:
                    dir_name = key
                    DIRECTORY_FINALLY = file_path.parent / dir_name
                    DIRECTORY_FINALLY.mkdir(exist_ok=True)
                    break
            else:
                continue

            shutil.move(str(file_path), str(DIRECTORY_FINALLY))

            logger.info(f"{file_path.suffix:10} {DIRECTORY_FINALLY}")

if __name__ == '__main__':
    clean = CleanDirectory()
    clean(sys.argv[1])
    logger.info('done')
