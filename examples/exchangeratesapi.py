from os import environ

from akame import run_basic_task


def main() -> None:
    """Function that runs the example"""

    run_basic_task(
        task_name="USD based exchange rates",
        target_url=(r"https://api.exchangeratesapi.io/latest?base=USD"),
        exset_name="basic",
        loop_seconds=300,
        loop_max_rounds=8640,
    )


if __name__ == "__main__":
    main()
