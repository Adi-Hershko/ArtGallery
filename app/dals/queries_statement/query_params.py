from typing import Dict
from .TitlesStatement import TitlesStatement
from .UserJoinedToPostsStatement import UserJoinedToPostsStatement
from .QueryStatementABC import QueryStatement

# This is where we add another parameters and their corresponding query statements
posts_statement_by_name: Dict[str, QueryStatement] = {
    'username': UserJoinedToPostsStatement(),
    'title': TitlesStatement()
}