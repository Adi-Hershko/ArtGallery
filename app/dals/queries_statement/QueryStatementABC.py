from abc import ABC, abstractmethod
from sqlalchemy.orm import Query

class QueryStatement(ABC):
    @abstractmethod
    def append_join(self,query: Query) -> Query:
        pass
    
    @abstractmethod
    def append_where(self, query: Query, condition) -> Query:
        pass