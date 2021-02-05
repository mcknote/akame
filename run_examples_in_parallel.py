from akame import init
from akame.utility.tasking import run_tasks_in_parallel
from examples import check_time_in_taipei, check_usd_exchange_rate


def main():
    """Function that gets and runs multiple examples"""
    tasks = [
        getattr(example, "main")
        for example in (check_time_in_taipei, check_usd_exchange_rate)
    ]
    run_tasks_in_parallel(tasks)


if __name__ == "__main__":
    # initialize akame
    init()
    # run multiple examples
    main()
