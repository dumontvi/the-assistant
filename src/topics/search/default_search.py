import logging

from .search import Search

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class DefaultSearch(Search):
    def search_engine(self, query):
        logger.info(f"JAZZ: Querying default engine for {query}")
        super().search_engine(query)
