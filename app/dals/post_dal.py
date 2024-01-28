from app.exceptions import FeedNotFoundException, PostNotFoundException
from app.DB.db_operations import DatabaseOperations
from ..DB.models import Post
from .queries_statement.query_params import posts_statement_by_name


async def get_all_posts(filters: dict) -> list:
    print("Getting all posts...")
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("Getting all posts...")
            query = session.query(Post)

            for filter_name in filters.keys():
                query = posts_statement_by_name[filter_name].append_join(query)
            
            for filter_name, condition in filters.items():
                query = posts_statement_by_name[filter_name].append_where(query, condition)

            print("Query: ", query)
            posts = query.all()
            
            print("Posts found: ", posts) if posts else print("Posts not found.")
            session.close()
            return posts
    except Exception as e:
        print(f"Error: {e}")        
        raise FeedNotFoundException("Feed not found.")


async def add_post(username: str, title: str, description: str, pathToImage: str) -> Post:
    print("Inserting post...")
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("Adding post...")
            new_post = Post(username=username, title=title, description=description, pathToImage=pathToImage)
            print("New post: ", new_post)            
            session.add(new_post)
            print("Post added.")
            session.commit()
            session.close()
            print(f"Post '{title}' added successfully.")
            return new_post
    except Exception as e:
        print(f"Error: {e}")
        raise PostNotFoundException("Post not found.")
    
