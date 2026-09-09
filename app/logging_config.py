import logging
import sys

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s | " "%(levelname)s | " "%(filename)s | " "%(lineno)s | " "%(name)s | " "%(message)s"),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )

    logging.getLogger("uvicorn").setLevel(logging.DEBUG)

    logging.getLogger("injectq").setLevel(logging.DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    logging.getLogger("app").setLevel(logging.DEBUG)
