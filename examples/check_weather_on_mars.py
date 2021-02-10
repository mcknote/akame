from os import environ

from akame import Monitor, init
from akame.notification.email_sendgrid import SendGridNotifier


def main() -> None:
    """Function that runs the example"""

    monitor = Monitor(
        task_name="USD based exchange rates",
        target_url=(
            r"https://api.nasa.gov/insight_weather/"
            r"?api_key=DEMO_KEY&feedtype=json&ver=1.0"
        ),
        loop_seconds=60 * 60 * 1,  # every 1 hour
        loop_max_rounds=24,  # for a day
    )

    # initiate notifiers and required credentials
    sendgrid_api_key = environ["SENDGRID_API_KEY"]
    notifiers = [
        SendGridNotifier(
            sendgrid_api_key=sendgrid_api_key,
            from_email="from@foobar.baz",
            to_email="to@foobar.baz",
        ),
    ]
    monitor.add_notifiers(notifiers=notifiers)

    monitor.main()


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()
