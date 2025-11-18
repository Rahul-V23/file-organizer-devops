import os
import shutil
import logging
from pathlib import Path

try:
    import yaml  # For local config fallback
except ImportError:
    yaml = None

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('organizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config loading
DIRECTORY_TO_SORT = os.environ.get('DIRECTORY_TO_SORT', 'watch_folder')
CATEGORIES_JSON = os.environ.get('CATEGORIES_JSON', None)

if CATEGORIES_JSON:
    import json
    DIRECTORIES = json.loads(CATEGORIES_JSON)
else:
    if yaml and Path('config.yaml').exists():
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f) or {}
            DIRECTORY_TO_SORT = config.get('directory_to_sort', DIRECTORY_TO_SORT)
            DIRECTORIES = config.get('categories', {})
    else:
        DIRECTORIES = {
            "IMAGES": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
            "DOCUMENTS": [".pdf", ".docx", ".txt", ".doc", ".xlsx", ".pptx"],
            "AUDIO": [".mp3", ".wav", ".flac", ".aac"],
            "VIDEO": [".mp4", ".mov", ".avi", ".mkv"],
            "ARCHIVES": [".zip", ".rar", ".7z", ".tar", ".gz"]
        }


def organize_files():
    """Main function – safe for import and direct run"""
    try:
        # Ensure watch_folder exists and cd into it
        watch_path = Path(DIRECTORY_TO_SORT)
        watch_path.mkdir(exist_ok=True)
        os.chdir(watch_path)
        logger.info(f"Started organizing files in '{watch_path.resolve()}'")

        for file_path in watch_path.iterdir():
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                moved = False

                for category, extensions in DIRECTORIES.items():
                    if suffix in [ext.lower() for ext in extensions]:
                        target_dir = watch_path / category
                        target_dir.mkdir(exist_ok=True)
                        shutil.move(str(file_path), target_dir / file_path.name)
                        logger.info(f"Moved {file_path.name} → {category}/")
                        moved = True
                        break

                if not moved:
                    other_dir = watch_path / "OTHER"
                    other_dir.mkdir(exist_ok=True)
                    shutil.move(str(file_path), other_dir / file_path.name)
                    logger.warning(f"Unknown type: {file_path.name} → OTHER/")

        logger.info("File organization completed successfully!")

    except Exception as e:
        logger.error(f"Error during organization: {e}", exc_info=True)


# This allows both: python organizer.py  AND  from organizer import organize_files
if __name__ == "__main__":
    organize_files()