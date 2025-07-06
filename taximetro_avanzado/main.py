import logging
from auth import authenticate_user
from taximeter import Taximeter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("taximeter.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()
    
file_handler = logging.FileHandler("taximeter.log", mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

if __name__ == "__main__":
    authenticate_user()
    Taximeter().run()