import os
from typing import Annotated
from fastapi import FastAPI, Depends
from pydantic.dataclasses import dataclass

from database.db import DatabaseController

app = FastAPI()


@dataclass
class DatabaseConfigs:
    host: str | None = None
    port: int = 1433
    user: str | None = None
    password: str | None = None
    database: str | None = None
    debug: bool = True

    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "debug": self.debug,
        }


def db_configs(
    host: str | None = None,
    user: str | None = None,
    password: str | None = None,
    port: int = 1433,
    database: str | None = None,
    debug: bool = True,
) -> DatabaseConfigs:
    host = os.getenv("DB_HOST", host)
    user = os.getenv("DB_USER", user)
    password = os.getenv("DB_PASS", password)
    port = int(os.getenv("DB_PORT", port))
    database = os.getenv("DB_NAME", database)
    debug_value = os.getenv("DB_DEBUG", debug)
    if not isinstance(debug_value, bool):
        debug = bool(debug_value)
    return DatabaseConfigs(host, port, user, password, database, debug)


DBConfigs = Annotated[DatabaseConfigs, Depends(db_configs)]


@app.get("/posts")
async def get_all_posts(db_configs: DBConfigs):
    controller = DatabaseController(db_configs)
    posts = await controller.get_posts()

    return {"Hello": "World"}


@app.get("/posts/{post_id}")
async def get_one_post(db_configs: DBConfigs):
    return db_configs
