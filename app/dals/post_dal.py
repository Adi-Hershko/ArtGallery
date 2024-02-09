from kink import di
from app.exceptions import OperationError, PostNotFoundException
from app.DB.db_operations import DatabaseOperations
from ..DB.models import Post
from .queries_statement.query_params import posts_statement_by_name
from ..pydantic_models.post_models.post_request_model import *

db_operations = di[DatabaseOperations]


async def get_all_posts(feed_reqs: dict) -> list[Post]:
    print("Getting all posts...")
    posts_response_list = []
    try:
        with db_operations.get_session() as session:
            print("Getting all posts...")
            query = session.query(Post).filter(Post.isActive)

            for filter_name, value in feed_reqs.items():
                print(f"Add join: {filter_name}")
                query = posts_statement_by_name[filter_name].append_join(query)

            for filter_name, condition in feed_reqs.items():
                print(f"Add filter: {filter_name}, {query}")
                query = posts_statement_by_name[filter_name].append_where(query, condition)

            print("Query: ", query)
            posts = query.all()

            print("Posts found: ", posts) if posts else print("Posts not found.")

            for post in posts:
                posts_response_list.append(Post(postId=post.postId, username=post.username, title=post.title, description=post.description, pathToImage=post.pathToImage, insertionTime=post.insertionTime, isActive=post.isActive))
            return posts_response_list
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Operation error.")


async def add_post(post: Post):
    print("Inserting post...")
    try:
        with db_operations.get_session() as session:
            print("Adding post...")
            print("New post: ", post)
            session.add(Post(username=post.username, title=post.title, description=post.description, pathToImage=post.pathToImage))
            print("Post added.")
            session.commit()
            print(f"Post '{post.title}' added successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Operation error.")


async def delete_post_in_db(post_id: UUID) -> bool:
    try:
        with db_operations.get_session() as session:
            print("Deleting post...")
            result = session.query(Post).filter(Post.postId == post_id).first()
            print("Query: ", result) if result else print("Post not found.")
            if result is None:
                return False
            result.isActive = False
            session.commit()
            print(f"Post '{post_id}' deleted successfully.")
            return True
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Operation error.")


async def update_post_in_db(post_id: UUID, updates: dict) -> int:
    try:
        with db_operations.get_session() as session:
            print("Updating post...")
            for key, value in updates.items():
                updates[key] = value

            result = session.query(Post).filter(Post.postId == post_id)
            rows_affected = result.update(updates)
            session.commit()
            print(f"Post '{post_id}' updated successfully.")
            print(rows_affected)
            return rows_affected
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Operation error.")