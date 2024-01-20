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