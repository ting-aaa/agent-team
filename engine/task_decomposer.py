"""任务分解系统"""
from typing import List, Optional
from projects.project import Task
from datetime import datetime
from config import DATETIME_FORMAT


class TaskDecomposer:
    """任务分解器"""

    @staticmethod
    def decompose_task(main_task: Task, subtasks_data: List[dict]) -> Task:
        """将主任务分解为子任务"""
        for subtask_data in subtasks_data:
            subtask = Task(
                name=subtask_data["name"],
                description=subtask_data["description"],
                assigned_to=subtask_data.get("assigned_to", main_task.assigned_to),
                status="pending",
            )
            main_task.subtasks.append(subtask)
        return main_task

    @staticmethod
    def create_iteration(main_task: Task, iteration_num: int, subtasks_data: List[dict]) -> Task:
        """创建迭代任务"""
        iteration_task = Task(
            name=f"{main_task.name} - Iteration {iteration_num}",
            description=f"Iteration {iteration_num} of {main_task.name}",
            assigned_to=main_task.assigned_to,
            status="pending",
        )

        for subtask_data in subtasks_data:
            subtask = Task(
                name=subtask_data["name"],
                description=subtask_data["description"],
                assigned_to=subtask_data.get("assigned_to", main_task.assigned_to),
                status="pending",
            )
            iteration_task.subtasks.append(subtask)

        main_task.subtasks.append(iteration_task)
        return main_task

    @staticmethod
    def get_task_progress(task: Task) -> dict:
        """获取任务进度"""
        total = len(task.subtasks)
        completed = sum(1 for st in task.subtasks if st.status == "completed")

        return {
            "task_name": task.name,
            "total_subtasks": total,
            "completed_subtasks": completed,
            "progress_percentage": (completed / total * 100) if total > 0 else 0,
            "status": task.status,
        }

    @staticmethod
    def mark_subtask_completed(task: Task, subtask_name: str) -> bool:
        """标记子任务完成"""
        for subtask in task.subtasks:
            if subtask.name == subtask_name:
                subtask.status = "completed"
                subtask.completed_at = datetime.now().strftime(DATETIME_FORMAT)
                return True
        return False

    @staticmethod
    def check_all_subtasks_completed(task: Task) -> bool:
        """检查所有子任务是否完成"""
        if not task.subtasks:
            return False
        return all(st.status == "completed" for st in task.subtasks)
