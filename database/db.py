from typing import TYPE_CHECKING

from .sql_server import DatabaseConnection

if TYPE_CHECKING:
    from main import DatabaseConfigs


class DatabaseController:

    def __init__(self, configs: "DatabaseConfigs") -> None:
        self.database = DatabaseConnection(configs)

    async def get_posts(self):
        return await self.database.call_get_posts_sp()
