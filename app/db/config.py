import os

from pydantic_settings import BaseSettings


class SettingsPostgres(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    model_config = {
        "env_file": "local.env" if os.getenv("USE_LOCAL_DB") == "True" else ".env"
    }

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @classmethod
    def switch_env_file(cls, local_db: bool = False):
        """
        Switch between local.env and .env
        Parameters
        ----------
        local_db: bool = False

        Returns
        -------

        """
        if local_db:
            cls.model_config = {"env_file": "local.env"}
        else:
            cls.model_config = {"env_file": ".env"}
        return cls()


settings = SettingsPostgres()
