import io
from PIL import Image
from fastapi import UploadFile
from kink import inject
from botocore.client import BaseClient
from app.config.config import s3_config, THUMBNAILS_SIZE
from app.exceptions import OperationError
from app import logger
from uuid import uuid4

module_name = __name__


@inject
class OsService:
    def __init__(self, session: BaseClient):
        self.session = session

    async def upload_image(self, file: UploadFile, title: str, username: str) -> str:
        logger.info(f"{module_name}.upload_image Start uploading images: {title}, of {username}")
        try:
            file_content = file.file.read()
            image_uuid = uuid4()
            path_to_image = f"{username}/{image_uuid}.png"
            self.session.put_object(Bucket=s3_config.bucket_name, Key=path_to_image, Body=file_content)
            logger.info(f"{module_name}.upload_image Finish uploading image: {title}, of {username}")
        except IOError as e:
            logger.error(f"{module_name}.upload_image Failed to open image, error: {e}")
            raise OperationError(e)
        except Exception as e:
            logger.error(f"{module_name}.upload_image Failed to save, error: {e}")
            raise OperationError(e)
        else:                        
            return path_to_image
        
    async def delete_image(self, path_to_image: str):
        logger.info(f"{module_name}.delete_image Start deleting image at path: {path_to_image}")
        try:            
            self.session.delete_object(Bucket=s3_config.bucket_name, Key=path_to_image)
            logger.info(f"{module_name}.delete_image Finished deleting image at path: {path_to_image}")
        except Exception as e:
            logger.error(f"{module_name}.delete_image Failed to delete image, error: {e}")
            raise OperationError(e)

        
    async def update_image(self, file: UploadFile, path_to_image: str, username: str) -> str:
        logger.info(f"{module_name}.update_image Start updating image of: {username}, at path: {path_to_image}")

        await self.delete_image(path_to_image)
        
        try:            
            file_content = file.file.read()
            image_uuid = uuid4()
            new_path_to_image = f"{username}/{image_uuid}.png"
            self.session.put_object(Bucket=s3_config.bucket_name, Key=new_path_to_image, Body=file_content)
            logger.info(f"{module_name}.update_image Finish updating image of {username}, at path: {path_to_image}")
        except IOError as e:
            logger.error(f"{module_name}.update_image Failed to open image, error: {e}")
            raise OperationError(e)
        except Exception as e:
            logger.error(f"{module_name}.update_image Failed to save, error: {e}")
            raise OperationError(e)
        else:            
            return new_path_to_image



