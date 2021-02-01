from os import environ

from akame import run_task


def main() -> None:
    """Function that runs the example"""
    # credentials specific to pushover
    pushover_creds = {
        "token": environ["PUSHOVER_TOKEN"],
        "user_key": environ["PUSHOVER_USERKEY"],
    }
    run_task(
        task_name="USD based exchange rates",
        target_url=(r"https://api.exchangeratesapi.io/latest?base=USD"),
        exset_name="basic",
        loop_seconds=300,
        loop_max_rounds=8640,
        notify_creds=pushover_creds,
    )


if __name__ == "__main__":
    main()
