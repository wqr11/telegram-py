from db import db_client


class TaskService:
    @staticmethod
    def get_tasks(id: int) -> list[tuple[int, str, str, bool, bool, str]]:
        cur = db_client.cursor()
        cur.execute(
            """
            SELECT * FROM "task" WHERE id = %s;
            """,
            (id,),
        )
        data = cur.fetchall()
        cur.close()
        return data
