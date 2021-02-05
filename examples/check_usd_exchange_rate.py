from os import environ

from akame import Monitor, init
from akame.notification.pushover import PushoverNotifier


def main() -> None:
    """Function that runs the example"""

    # load pushover credentials
    pushover_token = environ["PUSHOVER_TOKEN"]
    pushover_user_key = environ["PUSHOVER_USER_KEY"]

    # initialize the Pushover notifier
    notifiers = [
        PushoverNotifier(
            pushover_token=pushover_token, pushover_user_key=pushover_user_key
        )
    ]

    monitor = Monitor(
        task_name="USD based exchange rates",
        target_url=(r"https://api.exchangeratesapi.io/latest?base=USD"),
        loop_seconds=300,  # every 5 minutes
        loop_max_rounds=8640,  # for a month
        notifiers=notifiers,
    )

    monitor.main()


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()
