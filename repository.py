import os
from typing import Protocol

import psycopg
from psycopg.rows import dict_row


class TaskRepository(Protocol):
    def get_all(self) -> list[dict]:
        ...

    def get_by_id(self, task_id: int) -> dict | None:
        ...

    def create(self, title: str) -> dict:
        ...

    def update(
        self,
        task_id: int,
        title: str,
        done: bool
    ) -> dict | None:
        ...

    def delete(self, task_id: int) -> bool:
        ...


class PostgresTaskRepository:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not set")

    def get_connection(self):
        return psycopg.connect(
            self.database_url,
            row_factory=dict_row
        )

    def get_all(self) -> list[dict]:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, done FROM tasks ORDER BY id"
                )
                return list(cursor.fetchall())

    def get_by_id(self, task_id: int) -> dict | None:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,)
                )
                return cursor.fetchone()

    def create(self, title: str) -> dict:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, FALSE)
                    RETURNING id, title, done
                    """,
                    (title,)
                )
                return cursor.fetchone()

    def update(
        self,
        task_id: int,
        title: str,
        done: bool
    ) -> dict | None:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s, done = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (title, done, task_id)
                )
                return cursor.fetchone()

    def delete(self, task_id: int) -> bool:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM tasks WHERE id = %s",
                    (task_id,)
                )
                return cursor.rowcount > 0
