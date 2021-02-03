from akame import monitor_in_console


def main() -> None:
    """Function that runs the example"""

    monitor_in_console(
        task_name="USD based exchange rates",
        target_url=(r"https://api.exchangeratesapi.io/latest?base=USD"),
        exset_name="basic",
        loop_seconds=300,
        loop_max_rounds=8640,
    )


if __name__ == "__main__":
    main()
