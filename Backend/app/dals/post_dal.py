from kink import di
import inspect
from app.exceptions import OperationError, PostNotFoundException
from app.DB.db_operations import DatabaseOperations
from ..DB.models import Post
from .queries_statement.query_params import posts_statement_by_name
from ..pydantic_models.post_models.post_request_model import *

db_operations = di[DatabaseOperations]


async def get_all_posts(feed_reqs: dict) -> list[Post]:    
    posts_response_list = []
    try:
        with db_operations.get_session() as session:            
            query = session.query(Post).filter(Post.isActive)

            for filter_name, value in feed_reqs.items():
                # print(f"Add join: {filter_name}")
                query = posts_statement_by_name[filter_name].append_join(query)

            for filter_name, condition in feed_reqs.items():
                # print(f"Add filter: {filter_name}, {query}")
                query = posts_statement_by_name[filter_name].append_where(query, condition)
            
            posts = query.all()

            print(f"Rows fetched: {len(posts)}") if posts else print("Posts not found.")

            posts_response_list = list(map(lambda post: Post(
                postId=post.postId,
                username=post.username,
                title=post.title,
                description=post.description,
                pathToImage=post.pathToImage,
                insertionTime=post.insertionTime,
                isActive=post.isActive
            ), posts))
            return posts_response_list
    except Exception as e:
        module_name = __name__
        function_name = inspect.currentframe().f_code.co_name
        print(f"Error in {module_name}.{function_name}: Error: {e}")
        raise OperationError("Operation error.")


async def add_post(post: Post):
    print("Inserting post...")    
    with db_operations.get_session() as session:            
        session.add(Post(username=post.username, title=post.title, description=post.description, pathToImage=post.pathToImage))        
        try:
            session.commit()
            print(f"Post '{post.title}' added successfully.")
        except Exception as e:
            module_name = __name__
            function_name = inspect.currentframe().f_code.co_name
            print(f"Error in {module_name}.{function_name}: Error: {e}")
            raise OperationError("Operation error.")


async def delete_post_in_db(post_id: UUID) -> bool:    
    with db_operations.get_session() as session:
        print("Deleting post...")
        result = session.query(Post).filter(Post.postId == post_id).first()        
        if result is None:
            print(f"Post '{post_id}' not found.")
            return False
        try:
            result.isActive = False
            session.commit()
            print(f"Post '{post_id}' deleted successfully.")
            return True
        except Exception as e:
            module_name = __name__
            function_name = inspect.currentframe().f_code.co_name
            print(f"Error in {module_name}.{function_name}: Error: {e}")
            raise OperationError("Operation error.")


async def update_post_in_db(post_id: UUID, updates: dict) -> int:    
    with db_operations.get_session() as session:
        print("Updating post...")

        result = session.query(Post).filter(Post.postId == post_id)
        try:
            rows_affected = result.update(updates)
            session.commit()
            print(f"Post '{post_id}' updated successfully.")                
            return rows_affected
        except Exception as e:
            module_name = __name__
            function_name = inspect.currentframe().f_code.co_name
            print(f"Error in {module_name}.{function_name}: Error: {e}")
            raise OperationError("Operation error.")