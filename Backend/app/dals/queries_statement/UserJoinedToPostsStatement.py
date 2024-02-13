from abc import ABC, abstractmethod
from sqlalchemy.orm import Query
from .QueryStatementABC import QueryStatement
from ...DB.models import User, Post

class UserJoinedToPostsStatement(QueryStatement):
    def append_join(self, query: Query) -> Query:
        return query.join(User, User.username == Post.username)
    
    def append_where(self, query: Query, condition) -> Query:
        return query.filter(User.username == condition)
