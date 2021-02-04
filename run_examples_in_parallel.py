from concurrent.futures import ThreadPoolExecutor

from akame import init
from examples import check_time_in_taipei, check_usd_exchange_rate


# https://stackoverflow.com/questions/7207309/how-to-run-functions-in-parallel
def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def main():
    """Function that gets and runs multiple examples"""
    tasks = [
        getattr(example, "main")
        for example in (check_time_in_taipei, check_usd_exchange_rate)
    ]
    run_io_tasks_in_parallel(tasks)


if __name__ == "__main__":
    # initialize akame
    init()
    # run multiple examples
    main()
