"""isort:skip_file"""
from os import environ

from akame import init

# container for the monitoring tasks
from akame.tasks import SingleMonitorTask

# to extract the content
from akame.extraction import BasicExtractor

# to compare the content
from akame.comparison import BasicComparer

# to push notifications if the content changes
from akame.notification import BasicNotifier
from akame.notification.pushover import PushoverNotifier
from akame.notification.email_sendgrid import SendGridNotifier


def main() -> None:
    """Function that runs the example"""

    # define the task
    TASK_NAME = "How's the weather in Taipei?"
    WOEID_TAIPEI = "2487956"  # Where On Earth ID of Taipei
    TARGET_URL = rf"https://www.metaweather.com/api/location/{WOEID_TAIPEI}/"
    LOOP_SECONDS = 60 * 60 * 1  # every two hours
    LOOP_MAX_ROUNDS = int(24 / 1)  # for a day

    # initiate extractor
    extractor = BasicExtractor(TARGET_URL)

    # initiate comparer
    comparer = BasicComparer()

    # initiate notifiers and required credentials
    pushover_token = environ["PUSHOVER_TOKEN"]
    pushover_user_key = environ["PUSHOVER_USER_KEY"]
    sendgrid_api_key = environ["SENDGRID_API_KEY"]

    notifiers = [
        BasicNotifier(),
        PushoverNotifier(
            pushover_token=pushover_token,
            pushover_user_key=pushover_user_key,
        ),
        SendGridNotifier(
            sendgrid_api_key=sendgrid_api_key,
            from_email="from@foobar.baz",
            to_email="to@foobar.baz",
        ),
    ]

    # construct the monitoring task
    task = SingleMonitorTask(
        task_name=TASK_NAME,
        extractor=extractor,
        comparer=comparer,
        notifiers=notifiers,
        loop_seconds=LOOP_SECONDS,
        loop_max_rounds=LOOP_MAX_ROUNDS,
    )

    task.main()


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()
