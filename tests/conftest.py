import logging
import os
import sys
from pathlib import Path

ROOT_DIR_PATH = Path(__file__).parent.parent.absolute()
sys.path.append(os.path.join(ROOT_DIR_PATH))

logger = logging.getLogger(__name__)

logger.info("Start root conftest.py")
