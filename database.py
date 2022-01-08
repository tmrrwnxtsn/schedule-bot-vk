from psycopg2 import connect


class StudentDatabase:
    def __init__(self, database_url: str):
        self.db = connect(database_url)
        self.sql = self.db.cursor()
        self.sql.execute("""CREATE TABLE IF NOT EXISTS student(
        id SERIAL PRIMARY KEY,
        user_id INTEGER UNIQUE NOT NULL,
        group_name VARCHAR(50) NOT NULL
        )""")
        self.db.commit()

    def information(self, user_id: int, group_name: str):
        self.sql.execute(f"SELECT user_id FROM student WHERE user_id={user_id}")
        if self.sql.fetchone() is None:
            self.sql.execute(f"INSERT INTO student (user_id, group_name) VALUES (%s, %s)", (user_id, group_name))
            self.db.commit()
        else:
            self.update_group(user_id, group_name)

    def update_group(self, user_id: int, group_name: str):
        self.sql.execute(f"UPDATE student SET group_name='{group_name}' WHERE user_id='{user_id}'")
        self.db.commit()

    def check_student(self, user_id: int) -> bool:
        self.sql.execute(f"SELECT user_id FROM student WHERE user_id='{user_id}'")
        return not self.sql.fetchone() is None

    def get_group(self, user_id: int) -> str:
        self.sql.execute(f"SELECT group_name FROM student WHERE user_id='{user_id}'")
        return self.sql.fetchone()[0]

    def get_student_ids_by_group(self, group_name: str) -> []:
        self.sql.execute(f"SELECT user_id FROM student WHERE group_name='{group_name}'")
        return self.sql.fetchall()
