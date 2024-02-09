from kink import di
from app.DB.db_operations import DatabaseOperations
from app.DB.models import Post

db_operations = di[DatabaseOperations]


async def get_all_posts() -> list:
    print("Getting all posts...")
    try:
        with db_operations.get_session() as session:
            print("Getting all posts...")
            posts = session.query(Post).all()
            print("Posts found: ", posts) if posts else print("Posts not found.")
            session.close()
            return posts
    except Exception as e:
        print(f"Error: {e}")
        return None


async def add_post(username: str, title: str, description: str, pathToImage: str) -> int:
    print("Inserting post...")
    try:
        with db_operations.get_session() as session:
            print("Adding post...")
            new_post = Post(username=username, title=title, description=description, pathToImage=pathToImage)
            print("New post: ", new_post)
            session.add(new_post)
            print("Post added.")
            session.commit()
            session.close()

        print(f"Post '{title}' added successfully.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 0


async def find_posts_by_title(title: str) -> Post:
    print("Finding post...")
    try:
        with db_operations.get_session() as session:
            print("Locating post...")
            post = session.query(Post).filter(Post.title.ilike(f"%{title}%")).all()
            print("Post found: ", post) if post else print("Post not found.")
            session.close()
            return post
    except Exception as e:
        print(f"Error: {e}")
        return None


async def find_posts_by_username(username: str):
    print("Finding post...")
    try:
        with db_operations.get_session() as session:
            print("Locating post...")
            post = session.query(Post).filter(Post.username == username).all()
            print("Post found: ", post) if post else print("Post not found.")
            session.close()
            return post
    except Exception as e:
        print(f"Error: {e}")
        return None
