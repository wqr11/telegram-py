from db import db_client


class UserService:
    @staticmethod
    def get_users():
        cur = db_client.cursor()
        cur.execute("""
            SELECT * FROM "student";
            """)
        data = cur.fetchall()
        cur.close()
        return data

    @staticmethod
    def find_user_by_id(id: str) -> tuple[str, str, str] | None:
        cur = db_client.cursor()
        cur.execute(
            """
            SELECT * FROM "student" WHERE id = %s;
            """,
            (id,),
        )
        data = cur.fetchone()
        cur.close()
        return data

    @staticmethod
    def create_user(id: str, full_name: str):
        cur = db_client.cursor()
        cur.execute(
            """
            INSERT INTO "student" (id, full_name) VALUES (%s, %s);
            """,
            (id, full_name),
        )
        data = (
            id,
            full_name,
        )
        db_client.commit()
        cur.close()
        return data

    @staticmethod
    def join_group(user_id: str, group_name: str):
        cur = db_client.cursor()
        cur.execute(
            """
            UPDATE "student" SET group_name = %s WHERE id = %s;
            """,
            (group_name, user_id),
        )
        data = cur.statusmessage
        db_client.commit()
        cur.close()
        return data
