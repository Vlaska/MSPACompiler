import logging

from .textParser import TextCompiler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = [TextCompiler]
