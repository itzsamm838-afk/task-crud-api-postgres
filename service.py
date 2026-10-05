from fastapi import HTTPException

from repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_tasks(self) -> list[dict]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> dict | None:
        return self.repository.get_by_id(task_id)

    def create_task(self, title: str) -> dict:
        if not title.strip():
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )

        return self.repository.create(title)

    def update_task(
        self,
        task_id: int,
        title: str | None,
        done: bool | None
    ) -> dict | None:
        current = self.repository.get_by_id(task_id)

        if current is None:
            return None

        new_title = title if title is not None else current["title"]
        new_done = done if done is not None else current["done"]

        if not new_title.strip():
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )

        return self.repository.update(
            task_id,
            new_title,
            new_done
        )

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)
