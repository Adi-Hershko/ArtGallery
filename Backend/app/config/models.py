from dataclasses import dataclass

@dataclass
class DbConfig:
    host: str
    port: int
    username: str
    password: str
    database: str

    def __init__(self, host: str, port: int, username: str, password: str, database: str):  
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database


class S3Config:
    access_key: str
    secret_access_key: str
    bucket_name: str
    endpoint_url: str

    def __init__(self, access_key: str, secret_access_key: str, bucket_name: str):
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.bucket_name = bucket_name


class AuthConfig:
    secret_key: str
    algorithm: str

    def __init__(self, secret_key, algo):
        self.secret_key = secret_key
        self.algorithm = algo
