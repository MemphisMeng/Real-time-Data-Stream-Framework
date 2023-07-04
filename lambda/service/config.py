import logging, os, sys

LOGGER = logging.getLogger(__name__)


def load_env():
    """Load enviroment variables."""
    try:
        return {
                "DATA_STREAM": os.environ['DATA_STREAM']
                }
    except KeyError as error:
        LOGGER.exception("Enviroment variable %s is required.", error)
        sys.exit(1)