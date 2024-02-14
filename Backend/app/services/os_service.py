import io
from PIL import Image
from fastapi import UploadFile
from kink import di
from botocore.client import BaseClient
from Backend.app.config.config import s3_config, THUMBNAILS_SIZE
from exceptions import OperationError
from Backend.app import logger
from Backend.app.exceptions import ImageAlreadyExists


module_name = __name__
session = di[BaseClient]


async def upload_image_and_thumbnail(file: UploadFile, title: str, username: str) -> tuple:
    logger.info(f"{module_name}.upload_image_and_thumbnail Start uploading images: {title}, of {username}")
    try:
        file_content = file.file.read()

        if await _validate_already_exists(title, username):
            logger.info(f"{module_name}.upload_image_and_thumbnail File {title} already exists for {username}")
            raise ImageAlreadyExists(f"File {title} already exists for {username}")
        else:
            session.put_object(Bucket=s3_config.bucket_name, Key=f"{username}/{title}.png", Body=file_content)
            logger.info(f"{module_name}.upload_image_and_thumbnail Finish uploading image: {title}, of {username}")
            session.put_object(
                Bucket=s3_config.bucket_name,
                Key=f"thumbnails/{username}/{title}.png",
                Body=_create_thumbnail(file_content)
            )
    except IOError as e:
        logger.error(f"{module_name}.upload_image_and_thumbnail Failed to open image, error: {e}")
        raise OperationError(e)
    except Exception as e:
        logger.error(f"{module_name}.upload_image_and_thumbnail Failed to save, error: {e}")
        raise OperationError(e)
    else:
        logger.info(f"{module_name}.upload_image_and_thumbnail Finish uploading thumbnail image: {title}, of {username}")
        path_image_and_thumbnail = (f"{username}/{title}.png", f"thumbnails/{username}/{title}.png")
        return path_image_and_thumbnail


async def _validate_already_exists(title, username):
    try:
        session.head_object(Bucket=s3_config.bucket_name, Key=f"{username}/{title}.png")
        session.head_object(Bucket=s3_config.bucket_name, Key=f"thumbnails/{username}/{title}.png")
    except Exception as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

    return True


def _create_thumbnail(file: bytes):
    image = Image.open(io.BytesIO(file))
    thumbnail_bytes = io.BytesIO()

    thumbnail = image.copy()
    thumbnail.thumbnail(THUMBNAILS_SIZE)
    thumbnail.save(thumbnail_bytes, format="JPEG")

    thumbnail_bytes.seek(0)
    return thumbnail_bytes
