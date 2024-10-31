import aioodbc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..main import DatabaseConfigs

from .models.post import PostData


class DatabaseConnection:

    def __init__(self, configs: "DatabaseConfigs") -> None:
        self.dsn = f"Driver={{ODBC Driver 18 for SQL Server}};server={configs.host},{configs.port};UID={configs.user};PWD={configs.password};database={configs.database};TrustServerCertificate=yes;"

    async def call_get_posts_sp(self) -> list[PostData]:
        db = await aioodbc.connect(dsn=self.dsn)
        cursor = await db.cursor()
        await cursor.execute("EXEC dbo.GetPosts")
        rows = await cursor.fetchall()
        await cursor.close()
        await db.close()
        return [PostData(x[0], x[1], x[2], x[4], x[5], x[6], x[3]) for x in rows]

    async def call_get_post(self, post_id) -> PostData | None:
        db = await aioodbc.connect(dsn=self.dsn)
        cursor = await db.cursor()
        sql = "EXEC dbo.GetPost @post_id = ?"
        values = (post_id)
        await cursor.execute(sql, values)
        rows = await cursor.fetchall()
        await cursor.close()
        await db.close()
        if not rows:
            return None
        row = rows[0]
        return PostData(row[0], row[1], row[2], row[4], row[5], row[6], row[3], row[7])

    async def call_get_post_by_category(self, category) -> list[PostData]:
        db = await aioodbc.connect(dsn=self.dsn)
        cursor = await db.cursor()
        sql = "EXEC dbo.GetPosts @category = ?"
        values = (category)
        await cursor.execute(sql, values)
        rows = await cursor.fetchall()
        await cursor.close()
        await db.close()
        return [PostData(x[0], x[1], x[2], x[4], x[5], x[6], x[3]) for x in rows]

