from src.app.core.config import Settings


def construct_postgresql_url(settings: Settings):
    postgresql_dsn = (
        f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}"f"/{settings.db_name}"
    )
    return postgresql_dsn