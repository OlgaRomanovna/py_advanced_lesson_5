from pydantic import BaseModel


class Envs(BaseModel):
    app_url: str
    db_engine: str
    pool_size: int
    pg_user:str
    pg_password:str