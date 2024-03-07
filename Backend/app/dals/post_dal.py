from typing import List

from kink import inject
from app.exceptions import OperationError
from app.DB.db_operations import DatabaseOperations
from app.DB.models import Post
from app.dals.queries_statement.query_params import posts_statement_by_name
from app.pydantic_models.post_models.post_request_model import *
from app import logger

module_name = __name__


@inject
class PostDal:
    def __init__(self, db_operations: DatabaseOperations):
        self.db_operations = db_operations

    async def get_all_posts(self, feed_reqs: dict) -> List[Post]:
        logger.info(f"{module_name}.get_all_posts Start fetching post by filters: {feed_reqs}")
        with self.db_operations.get_session() as session:
            query = session.query(Post).filter(Post.is_active)

            for filter_name, value in feed_reqs.items():
                logger.debug(f"{module_name}.get_all_posts Add join: {filter_name}")
                query = posts_statement_by_name[filter_name].append_join(query)

            for filter_name, condition in feed_reqs.items():
                logger.debug(f"{module_name}.get_all_posts Add filter: {filter_name}")
                query = posts_statement_by_name[filter_name].append_where(query, condition)
            try:
                posts = query.all()
            except Exception as e:
                logger.error(f"{module_name}.get_all_posts Failed to fetch posts, error: {e}")
                raise OperationError("Operation error.")
            else:
                logger.info(f"{module_name}.get_all_posts Rows fetched: {len(posts)}")
                return posts

    async def add_post(self, post: Post):
        logger.info(f"{module_name}.add_post Inserting post {post.title}, of {post.username}")
        with self.db_operations.get_session() as session:
            session.add(post)
            try:
                session.commit()
                session.refresh(post)                
            except Exception as e:
                logger.error(f"{module_name}.add_post Failed to insert post Error: {e}")
                session.rollback()
                raise OperationError("Operation error.")
            else:
                logger.info(f"{module_name}.add_post Post {post.title}, of {post.username} added successfully.")
                return post

    async def delete_post_in_db(self, post_id: UUID):
        logger.info(f"{module_name}.delete_post_in_db Deleting post {post_id}")

        with self.db_operations.get_session() as session:
            result = session.query(Post).filter(Post.post_id == post_id).first()
            if result is None:
                logger.info(f"{module_name}.delete_post_in_db Post '{post_id}' not found.")
            try:
                logger.info(f"{module_name}.delete_post_in_db Deleting post '{post_id}'...")                                
                result.is_active = False
                session.commit()
                logger.info(f"{module_name}.delete_post_in_db Post '{post_id}' deleted successfully.")
            except Exception as e:
                logger.error(f"{module_name}.delete_post_in_db Error: {e}")
                raise OperationError("Operation error.")

    async def update_post_in_db(self, post_id: UUID, updates: dict) -> Post:
        logger.info(f"{module_name}.update_post_in_db Updating post...")        
        with self.db_operations.get_session() as session:
            result = session.query(Post).filter(Post.post_id == post_id)
            try:                
                result.update(updates)                
                session.commit()           
                session.refresh(result.first())
                updated_post = result.first()
                if updated_post is None:
                    logger.info(f"{module_name}.update_post_in_db Post '{post_id}' not found.")
                    raise OperationError("Operation error.")     
            except Exception as e:
                logger.error(f"{module_name}.update_post_in_db Error: {e}")
                session.rollback()
                raise OperationError("Operation error.")
            else:
                logger.info(f"{module_name}.update_post_in_db Post '{post_id}' updated successfully.")
                return updated_post

