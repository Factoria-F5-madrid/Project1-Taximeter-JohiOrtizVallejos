import logging
from taximeter import Taximeter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("taximeter.log"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    Taximeter().run()