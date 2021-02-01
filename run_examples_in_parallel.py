from concurrent.futures import ThreadPoolExecutor

from akame import init
from examples import worldtime_api


# https://stackoverflow.com/questions/7207309/how-to-run-functions-in-parallel
def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def main():
    init()
    tasks = [getattr(example, "main") for example in (worldtime_api,)]
    run_io_tasks_in_parallel(tasks)


if __name__ == "__main__":
    main()
