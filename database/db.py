from typing import TYPE_CHECKING

from .sql_server import DatabaseConnection

if TYPE_CHECKING:
    from main import DatabaseConfigs


class DatabaseController:

    def __init__(self, configs: "DatabaseConfigs") -> None:
        self.database = DatabaseConnection(configs)

    async def get_posts(self):
        return await self.database.call_get_posts_sp()

    async def get_post(self, post_id):
        return await self.database.call_get_post(post_id)

    async def get_posts_by_category(self, category):
        return await self.database.call_get_post_by_category(category)
