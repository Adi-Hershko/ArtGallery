from app.exceptions import OperationError, PostNotFoundException
from app.DB.db_operations import DatabaseOperations
from ..DB.models import Post
from .queries_statement.query_params import posts_statement_by_name
from ..pydantic_models.post_models.post_request_model import *
from ..pydantic_models.post_models.post_response_model import *
from uuid import UUID


async def get_all_posts(feedReqs: PostFeedRequestModel) -> list[PostGetResponseModel]:
    print("Getting all posts...")
    posts_response_list = []
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("Getting all posts...")
            query = session.query(Post).filter(Post.isActive == True)

            for filter_name, value in feedReqs.__dict__.items():
                print("Filter name in join: ", filter_name)                
                query = posts_statement_by_name[filter_name].append_join(query)
            
            for filter_name, condition in feedReqs.__dict__.items():
                print("Filter name in where:", filter_name)
                print("Condition: ", condition)
                if condition is not None:
                    query = posts_statement_by_name[filter_name].append_where(query, condition)

            print("Query: ", query)
            posts = query.all()
            
            print("Posts found: ", posts) if posts else print("Posts not found.")
            session.close()
            
            for post in posts:
                posts_response_list.append(PostGetResponseModel(postId=post.postId, username=post.username, title=post.title, description=post.description, pathToImage=post.pathToImage, insertionTime=post.insertionTime, isActive=post.isActive))
            return posts_response_list
    except Exception as e:
        print(f"Error: {e}")        
        raise OperationError("Operation error.")


async def add_post(post: PostUploadRequestModel):
    print("Inserting post...")
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("Adding post...")
            new_post = Post(username=post.username, title=post.title, description=post.description, pathToImage=post.pathToImage)
            print("New post: ", new_post)            
            session.add(new_post)
            print("Post added.")
            session.commit()
            session.close()
            print(f"Post '{post.title}' added successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Operation error.")

    
async def delete_post_in_db(post: PostIdSearchRequestModel) -> bool:
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("Deleting post...")
            result = session.query(Post).filter(Post.postId == post.postId).first()        
            print("Query: ", result) if result else print("Post not found.")
            if result is None:
                return False
            result.isActive = False            
            session.commit()
            session.close()
            print(f"Post '{post.postId}' deleted successfully.")
            return True
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Operation error.")


async def update_post_in_db(post: PostUpdateRequestModel) -> int:
    updates = {}
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("Updating post...")
            for key, value in post.__dict__.items():
                if value is not None:
                    updates[key] = value

            result = session.query(Post).filter(Post.postId == post.postId)                        
            rows_affected = result.update(updates)
            session.commit()
            session.close()
            print(f"Post '{post.postId}' updated successfully.")
            return rows_affected
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Operation error.")