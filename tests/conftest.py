import os
import dotenv
import pytest
from sqlalchemy import create_engine
from app.client.api.user_api import UsersApi
from app.models.Envs import Envs


@pytest.fixture(scope="session", autouse=True)
def envs() -> Envs:
    dotenv.load_dotenv()
    envs_instance = Envs(
        app_url=os.getenv("APP_URL"),
        db_engine=os.getenv("DATABASE_ENGINE"),
        pool_size=os.getenv("DATABASE_POOL_SIZE"),
        pg_user=os.getenv("POSTGRES_USER"),
        pg_password=os.getenv("POSTGRES_PASSWORD")
    )
    return envs_instance

@pytest.fixture(scope="session")
def _db_engine_(envs):
    return create_engine(envs.db_engine, pool_size=os.getenv("DATABASE_POOL_SIZE", 10))

@pytest.fixture
def users_api(envs):
    return UsersApi(f"{envs.app_url}/api")



