import os
import shutil
import logging
from pathlib import Path
import yaml  # pip install PyYAML

# Set up logging: Logs to console + file for full visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('organizer.log'),  # Saves to file
        logging.StreamHandler()  # Also prints to console
    ]
)
logger = logging.getLogger(__name__)

# Load configuration from YAML
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

DIRECTORY_TO_SORT = config['directory_to_sort']
DIRECTORIES = config['categories']


def organize_files():
    try:
        os.chdir(DIRECTORY_TO_SORT)
        logger.info(f"Starting organization in {DIRECTORY_TO_SORT}")

        for file_path in Path('.').iterdir():
            if file_path.is_file():
                file_suffix = file_path.suffix.lower()
                moved = False

                # Find category and move file
                for category, extensions in DIRECTORIES.items():
                    if file_suffix in extensions:
                        Path(category).mkdir(exist_ok=True)
                        shutil.move(str(file_path), Path(
                            category) / file_path.name)
                        logger.info(f"Moved {file_path.name} to {category}/")
                        moved = True
                        break

                # Unknown files go to OTHER
                if not moved:
                    Path("OTHER").mkdir(exist_ok=True)
                    shutil.move(str(file_path), Path("OTHER") / file_path.name)
                    logger.warning(
                        f"Unknown extension for {file_path.name}; moved to OTHER/")

        logger.info("Organization complete!")
    except Exception as e:
        logger.error(f"Error during organization: {e}")


if __name__ == "__main__":
    organize_files()
# Test comment