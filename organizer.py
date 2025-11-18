import os
import shutil
import logging
from pathlib import Path

# ONLY console logging – safe for Fargate
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Safe defaults
DIRECTORY_TO_SORT = os.environ.get('DIRECTORY_TO_SORT', 'watch_folder')
DIRECTORIES = {
    "IMAGES":   [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "DOCUMENTS":[".pdf", ".txt", ".docx", ".xlsx", ".pptx"],
    "VIDEO":    [".mp4", ".mov", ".avi", ".mkv"],
    "AUDIO":    [".mp3", ".wav", ".flac"],
    "ARCHIVES": [".zip", ".rar", ".7z", ".tar.gz"]
}

def organize_files():
    try:
        watch_path = Path(DIRECTORY_TO_SORT)
        watch_path.mkdir(exist_ok=True)          # ← create if missing
        os.chdir(watch_path)                     # ← now safe
        logger.info(f"Organizing files in: {watch_path.resolve()}")

        for file_path in watch_path.iterdir():
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                moved = False
                for cat, exts in DIRECTORIES.items():
                    if suffix in [e.lower() for e in exts]:
                        (watch_path / cat).mkdir(exist_ok=True)
                        shutil.move(str(file_path), watch_path / cat / file_path.name)
                        logger.info(f"Moved {file_path.name} → {cat}/")
                        moved = True
                        break
                if not moved:
                    (watch_path / "OTHER").mkdir(exist_ok=True)
                    shutil.move(str(file_path), watch_path / "OTHER" / file_path.name)

        logger.info("Organization complete!")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

# Keep this for local testing
if __name__ == "__main__":
    organize_files()