import json

from app.memory.database import (
    get_connection
)

from app.memory.models import (
    MemoryRecord
)


class MemoryManager:

    def save_memory(
        self,
        memory: MemoryRecord
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO user_memory
            (
                user_id,
                goal,
                completed_tasks,
                observations
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                memory.user_id,
                memory.goal,
                json.dumps(
                    memory.completed_tasks
                ),
                json.dumps(
                    memory.observations
                )
            )
        )

        connection.commit()

        connection.close()

    def load_memory(
        self,
        user_id: str
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                user_id,
                goal,
                completed_tasks,
                observations
            FROM user_memory
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return MemoryRecord(
            user_id=row[0],
            goal=row[1],
            completed_tasks=json.loads(
                row[2]
            ),
            observations=json.loads(
                row[3]
            )
        )