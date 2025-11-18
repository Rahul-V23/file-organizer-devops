import os
import shutil
import logging
from pathlib import Path

# ───────────────────── FARGATE-SAFE LOGGING ─────────────────────
# Only log to console (stdout) — Fargate can always write there
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]   # ← ONLY console, no file
)
logger = logging.getLogger(__name__)

# Config loading (safe)
try:
    import yaml
    if Path('config.yaml').exists():
        with open('config.yaml') as f:
            config = yaml.safe_load(f) or {}
        DIRECTORY_TO_SORT = config.get('directory_to_sort', 'watch_folder')
        DIRECTORIES = config.get('categories', {})
    else:
        DIRECTORIES = {}
except Exception:
    DIRECTORIES = {}

# Fallback categories if nothing loaded
if not DIRECTORIES:
    DIRECTORIES = {
        "IMAGES": [".jpg", ".jpeg", ".png", ".gif"],
        "DOCUMENTS": [".pdf", ".txt", ".docx"],
        "VIDEO": [".mp4", ".mov", ".avi"],
        "AUDIO": [".mp3", ".wav"],
        "ARCHIVES": [".zip", ".rar"]
    }

DIRECTORY_TO_SORT = os.environ.get('DIRECTORY_TO_SORT', 'watch_folder')


def organize_files():
    try:
        watch_path = Path(DIRECTORY_TO_SORT)
        watch_path.mkdir(exist_ok=True)
        os.chdir(watch_path)
        logger.info(f"Organizing files in: {watch_path}")

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


if __name__ == "__main__":
    organize_files()