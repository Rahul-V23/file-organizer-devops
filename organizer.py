import os
import shutil
import logging
from pathlib import Path

# Safe logging — only stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Hard-coded — no YAML, no env, no surprises
DIRECTORY_TO_SORT = "watch_folder"

CATEGORIES = {
    "IMAGES":   [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".tiff"],
    "DOCUMENTS":[".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
    "VIDEO":    [".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv"],
    "AUDIO":    [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "ARCHIVES": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"]
}


def organize_files() -> None:
    """This is the ONLY function that does work. Safe to import."""
    try:
        watch_path = Path(DIRECTORY_TO_SORT)
        watch_path.mkdir(exist_ok=True)
        os.chdir(watch_path)
        logger.info(f"Successfully changed to directory: {watch_path.resolve()}")

        for file_path in watch_path.iterdir():
            if not file_path.is_file():
                continue

            suffix = file_path.suffix.lower()
            moved = False

            for folder_name, extensions in CATEGORIES.items():
                if suffix in extensions:
                    target_dir = watch_path / folder_name
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file_path), target_dir / file_path.name)
                    logger.info(f"Moved: {file_path.name} → {folder_name}/")
                    moved = True
                    break

            if not moved:
                other_dir = watch_path / "OTHER"
                other_dir.mkdir(exist_ok=True)
                shutil.move(str(file_path), other_dir / file_path.name)
                logger.info(f"Moved: {file_path.name} → OTHER/")

        logger.info("File organization completed successfully!")

    except Exception as e:
        logger.error(f"Unexpected error in organize_files: {e}", exc_info=True)


# This block only runs when you do "python organizer.py" locally
if __name__ == "__main__":
    organize_files()