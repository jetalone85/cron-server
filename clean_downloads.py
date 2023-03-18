import shutil
import time
from pathlib import Path
from typing import List

# Define the download folder, the folder to move old files to, and the threshold for old files
DOWNLOAD_FOLDER = Path("/Users/marcin.pyrka/Downloads")
TO_DELETE_FOLDER = DOWNLOAD_FOLDER / "to_delete"
OLD_FILE_THRESHOLD_DAYS = 30

# Create the folder to move old files to if it does not exist
if not TO_DELETE_FOLDER.exists():
    TO_DELETE_FOLDER.mkdir()


# Define a function to determine whether a file is old enough to be deleted
def is_old_file(file_path: Path) -> bool:
    return (
        file_path.is_file()
        and time.time() - file_path.stat().st_mtime
        > OLD_FILE_THRESHOLD_DAYS * 24 * 60 * 60
    )


# Define a function to move a file to the folder to delete
def move_file_to_delete_folder(file_path: Path) -> None:
    with file_path.open("rb") as f:
        shutil.move(str(file_path), str(TO_DELETE_FOLDER))


# Filter the list of files in the download folder to only include files that are old enough to be deleted
files_to_move = list(filter(is_old_file, DOWNLOAD_FOLDER.iterdir()))

# Move each file in the filtered list to the folder to delete
list(map(move_file_to_delete_folder, files_to_move))
