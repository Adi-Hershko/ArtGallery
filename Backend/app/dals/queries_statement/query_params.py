from typing import Dict
from app.dals.queries_statement.TitlesStatement import TitlesStatement
from app.dals.queries_statement.UserJoinedToPostsStatement import UserJoinedToPostsStatement
from app.dals.queries_statement.QueryStatementABC import QueryStatement

posts_statement_by_name: Dict[str, QueryStatement] = {
    'username': UserJoinedToPostsStatement(),
    'title': TitlesStatement()
}