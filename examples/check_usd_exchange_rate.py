from os import environ

from akame import init, monitor_with_pushover


def main() -> None:
    """Function that runs the example"""

    # load pushover credentials
    pushover_token = environ["PUSHOVER_TOKEN"]
    pushover_user_key = environ["PUSHOVER_USER_KEY"]

    monitor_with_pushover(
        task_name="USD based exchange rates",
        target_url=(r"https://api.exchangeratesapi.io/latest?base=USD"),
        loop_seconds=300,  # every 5 minutes
        loop_max_rounds=8640,  # for a month
        pushover_token=pushover_token,
        pushover_user_key=pushover_user_key,
    )


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()
