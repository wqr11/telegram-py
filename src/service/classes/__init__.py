from db import db_client


class ClassService:
    @staticmethod
    def create_class(name: str, user_id: str):
        cur = db_client.cursor()
        cur.execute(
            """
            INSERT INTO "class" (name, group_name) VALUES (%s, (SELECT group_name FROM "student" WHERE id = %s));
            """,
            (name, user_id),
        )
        data = cur.statusmessage
        db_client.commit()
        cur.close()
        return data

    @staticmethod
    def get_classes_by_user_id(user_id: str) -> list[tuple[int, str, str]] | None:
        cur = db_client.cursor()
        cur.execute(
            """
            SELECT * FROM "class" WHERE group_name = (SELECT group_name FROM "student" WHERE id = %s);
            """,
            (user_id,),
        )
        data = cur.fetchall()
        cur.close()
        return data
