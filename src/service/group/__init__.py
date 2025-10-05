from db import db_client


class GroupService:
    @staticmethod
    def find_by_name(name: str) -> tuple[str] | None:
        cur = db_client.cursor()
        cur.execute(
            """
            SELECT * FROM "group" WHERE name = %s;
            """,
            (name,),
        )
        data = cur.fetchone()
        cur.close()
        return data

    @staticmethod
    def list() -> list[tuple[str]]:
        cur = db_client.cursor()
        cur.execute("""
            SELECT * FROM "group";
            """)
        data = cur.fetchall()
        cur.close()
        return data
