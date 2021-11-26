import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class TaskManager:
    def __init__(self):
        self.task_list = []

    def add_task(self, task_name: str):
        if task_name.isnumeric():
            logger.error(f"Error occurred here")
            raise Exception("Task cannot be a number")
        self.task_list.append(task_name)


class ManageSchedule:
    def __init__(self, name):
        self.name = name
        self.crate_my_tasks()

    def crate_my_tasks(self):
        self.my_task_manager = TaskManager()

    def set_task_list(self, task_list: list):
        for task in task_list:
            self.my_task_manager.add_task(task)
        return self.my_task_manager.task_list


def main():
    my_schedule = ManageSchedule(name="Seun")
    try:
        print(my_schedule.set_task_list(["Wash dishes", "Take out trash"]))
    except Exception as e:
        logger.error(f"Error Detail: {e}")


if __name__ == "__main__":
    main()
