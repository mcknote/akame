from akame import monitor_in_console


def main() -> None:
    """Function that runs the example"""

    monitor_in_console(
        task_name="Does Time Flow in Taipei?",
        target_url=(r"http://worldtimeapi.org/api/timezone/Asia/Taipei"),
        exset_name="basic",
        loop_seconds=30,
        loop_max_rounds=86400,
    )


if __name__ == "__main__":
    main()
