import aioodbc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import DatabaseConfigs


class DatabaseConnection:
    DRIVER = "sqlserver"

    def __init__(self, configs: "DatabaseConfigs") -> None:
        self.dsn = f"Driver={{ODBC Driver 18 for SQL Server}};server={configs.host},{configs.port};UID={configs.user};PWD={configs.password};database={configs.database};TrustServerCertificate=yes;"

    async def call_get_posts_sp(self):
        db = await aioodbc.connect(dsn=self.dsn)
        cur = await db.cursor()
        await cur.execute("EXEC dbo.GetPosts")
        rows = await cur.fetchall()
        print(rows)
        print(rows[0])
        await cur.close()
        await db.close()
