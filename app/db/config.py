from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    name: str
    user: str
    password: str
    host: str
    port: str

    @property
    def database_url_psycopg2(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


# settings = PostgresSettings()
