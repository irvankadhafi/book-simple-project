import logging

logger = logging.getLogger(__name__)


class QueryCollector:
    def __init__(self):
        self.queries = []

    def collect(self, query):
        self.queries.append(query)

    def clear(self):
        self.queries = []

    def print_queries(self):
        for query in self.queries:
            logger.info(f"Executed Query: {query}")


query_collector = QueryCollector()
