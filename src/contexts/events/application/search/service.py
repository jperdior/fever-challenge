class SearchService:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    def search(self, query: str) -> List[Event]:
        return self.repository.search(query)