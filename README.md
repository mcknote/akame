# Akame Monitor

Akame Monitor is a modulized tool to constantly monitor web changes every X seconds for Y rounds. It contains a couple of modules such as extraction, comparison, and notification and allows users to design their own units and flexibly construct the monitoring workflow.

- [Akame Monitor](#akame-monitor)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Build Your Own Monitor](#build-your-own-monitor)

## Installation

```bash
# switch to the download folder as necessary
$ git clone https://github.com/mcknote/akame.git
```

## Usage

Example from `examples/check_time_in_taipei.py`.

```python
from akame import Monitor, init


def main() -> None:
    """Function that runs the example"""

    monitor = Monitor(
        task_name="Does Time Flow in Taipei?",
        target_url=(r"http://worldtimeapi.org/api/timezone/Asia/Taipei"),
        loop_seconds=60,  # every 1 minute
        loop_max_rounds=43200,  # for a month
    )

    monitor.main()


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()

```

At a bare minimum `akame.Monitor` takes four parameters:

- `task_name`: Name of the monitoring task; this will appear in the console logs and notification programs.
- `target_url`: URL to be monitored, e.g. an API endpoint or a webpage.
- `loop_seconds`: Interval in seconds between all monitoring rounds. Default to `300` seconds.
- `loop_max_rounds`: Maximum number of rounds to monitor. Default to `12` rounds (so with 300 seceonds, this would make a one-hour monitoring task).

With these four parameters specified, `Monitor` will constantly monitor any changes at the URL given and report the difference through console.

## Build Your Own Monitor

Under the hood `Monitor` takes three more parameters that allow greater flexibility:

| Parameter | What does it do | Where can it be found | How to get started |
| --- | --- | --- | --- |
| `extractor` | Extracts the content to monitor from the target url | `akame.extraction` (*1) | `BasicExtractor`
| `comparer` | Compares the monitored content against its previous version or a specified value | `akame.comparison` | `BasicComparer` |
| `notifiers` | Notifies of the comparison results (e.g. changes detected) (*2) | `akame.notification` | `BasicNotifier` |

Notes:

1. Site-specific extractors can be imported from and are recommended to be defined in `akame.extraction.sets.{site_name}`
2. Additional setups may be required by the notification program

All these components can be designed and initialized separately. Below is an example from `examples/check_weather_in_taipei.py` that use Pushover and Sendgrid notifiers on top of the console outputs.

```python
from os import environ

from akame import init, Monitor

# to extract the content (this is the default extractor)
from akame.extraction import BasicExtractor

# to compare the content (this is the default comparer)
from akame.comparison import BasicComparer

# to push notifications if the content changes
from akame.notification.pushover import PushoverNotifier
from akame.notification.email_sendgrid import SendGridNotifier


def main() -> None:
    """Function that runs the example"""

    # define the task
    TASK_NAME = "How's the weather in Taipei?"
    TARGET_URL = r"https://www.metaweather.com/api/location/2487956/"
    LOOP_SECONDS = 60 * 60 * 2  # every two hours
    LOOP_MAX_ROUNDS = int(24 / 2)  # for a day

    # initiate extractor
    extractor = BasicExtractor()

    # initiate comparer
    comparer = BasicComparer()

    # initiate notifiers and required credentials
    pushover_token = environ["PUSHOVER_TOKEN"]
    pushover_user_key = environ["PUSHOVER_USER_KEY"]
    sendgrid_api_key = environ["SENDGRID_API_KEY"]

    notifiers = [
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

    # construct the monitor
    monitor = Monitor(
        target_url=TARGET_URL,
        task_name=TASK_NAME,
        extractor=extractor,
        comparer=comparer,
        # notifiers can also be defined here
        loop_seconds=LOOP_SECONDS,
        loop_max_rounds=LOOP_MAX_ROUNDS,
    )

    # add additional notifiers
    monitor.add_notifiers(notifiers)

    # execute the monitor
    monitor.main()


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()

```
