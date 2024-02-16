from sqlalchemy.orm import Query
from app.DB.models import Post
from app.dals.queries_statement.QueryStatementABC import QueryStatement


class TitlesStatement(QueryStatement):
    def append_join(self, query: Query) -> Query:
        return query
    
    def append_where(self, query: Query, condition) -> Query:
        return query.filter(Post.title.ilike(f"%{condition}%"))
 