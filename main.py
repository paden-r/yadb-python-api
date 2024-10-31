import logging
import os
import sys
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.dataclasses import dataclass

from database.db import DatabaseController

app = FastAPI()

# TODO: Move logger creation to function and clean up the format
logger = logging.getLogger("YADB")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.info("API is starting up")


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
async def get_all_posts(db_configs: DBConfigs, category: str | None = None):
    controller = DatabaseController(db_configs)
    if category:
        posts = await controller.get_posts_by_category(category)
    else:
        posts = await controller.get_posts()
    logger.debug(posts)

    return jsonable_encoder(posts)


@app.get("/posts/{post_id}")
async def get_one_post(db_configs: DBConfigs, post_id: int):
    try:
        int(post_id)
    except ValueError:
        logger.exception("post id is not int")
        raise HTTPException(status_code=400, detail="Invalid Post ID")
    controller = DatabaseController(db_configs)
    post = await controller.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return jsonable_encoder(post)
