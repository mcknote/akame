from akame import init, monitor_in_console


def main() -> None:
    """Function that runs the example"""

    monitor_in_console(
        task_name="Does Time Flow in Taipei?",
        target_url=(r"http://worldtimeapi.org/api/timezone/Asia/Taipei"),
        loop_seconds=60,  # every 1 minute
        loop_max_rounds=43200,  # for a month
    )


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()
