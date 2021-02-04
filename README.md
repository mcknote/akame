# Akame Monitor

Akame Monitor is a collection of tools to constantly monitor web changes every X seconds for Y rounds. It contains a couple of modules such as extraction, comparison, and notification and allows users to design their own units and flexibly construct the monitoring workflow.

- [Akame Monitor](#akame-monitor)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Monitor in Console](#monitor-in-console)
    - [Monitor with Pushover](#monitor-with-pushover)
    - [Monitor with SendGrid](#monitor-with-sendgrid)
  - [Build Your Own Monitor](#build-your-own-monitor)
    - [Example](#example)

## Installation

```bash
# switch to the download folder as necessary
$ git clone https://github.com/mcknote/akame.git
```

## Usage

### Monitor in Console

Example from `examples/check_time_in_taipei.py`.

```python
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

```

Parameters for `akame.monitor_in_console`:

- `task_name`: Name of the monitoring task; this will appear in the console logs and notification programs.
- `target_url`: URL to be monitored, e.g. an API endpoint or a webpage.
- `loop_seconds`: Interval in seconds between all monitoring rounds. Default to `30` seconds.
- `loop_max_rounds`: Maximum number of rounds to monitor. Default to `86400` rounds (so with 30 seceonds, this would make a one-month monitoring task).

### Monitor with Pushover

Example from `examples/check_usd_exchange_rate.py`.

```python
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

```

Parameters for `akame.monitor_with_pushover` include those from `akame.monitor_in_console` and the following:

- `pushover_token`: Pushover token
- `pushover_user_key`: Pushover user key

Read more about the Pushover API [here](https://pushover.net/api).

### Monitor with SendGrid

Example from `examples/check_weather_on_mars.py`.

```python
from os import environ

from akame import init, monitor_with_sendgrid


def main() -> None:
    """Function that runs the example"""

    # load sendgrid credentials
    sendgrid_api_key = environ["SENDGRID_API_KEY"]

    monitor_with_sendgrid(
        task_name="USD based exchange rates",
        target_url=(
            r"https://api.nasa.gov/insight_weather/"
            r"?api_key=DEMO_KEY&feedtype=json&ver=1.0"
        ),
        loop_seconds=60 * 60 * 1,  # every 1 hour
        loop_max_rounds=24,  # for a day
        sendgrid_api_key=sendgrid_api_key,
        from_email="from@foobar.baz",
        to_email="to@foobar.baz",
    )


if __name__ == "__main__":
    # initialize akame
    init()
    # run the example
    main()

```

Parameters for `akame.monitor_with_sendgrid` include those from `akame.monitor_in_console` and the following:

- `sendgrid_api_key`: SendGrid API key
- `from_email`: Email to be sent from
- `to_email`: Email to be sent to

Read more about the Pushover API [here](https://sendgrid.com/docs/api-reference/).

## Build Your Own Monitor

Under the hood the monitors above are all constructed using `akame.tasks.SingleMonitorTask`, which requires three main components:

| Component | What does it do | Where can it be found | How to get started |
| --- | --- | --- | --- |
| **Extractor** | Extracts the content to monitor from the target url | `akame.extraction` (*1) | `akame.extraction.BasicExtractor`
| **Comparer** | Compares the monitored content against its previous version or a specified value | `akame.comparison` | `akame.comparison.BasicComparer` |
| **Notifier** | Notifies of the comparison results (e.g. changes detected) (*2) | `akame.notification` | `akame.notification.BasicNotifier` |

Notes:

1. Site-specific extractors can be imported from and recommended to be defined in `akame.extraction.sets.{site_name}`
2. Additional setups may be required by the notification program

### Example

Below is an example from `examples/check_weather_in_taipei.py` that uses all the basic components from the table above, plus two notifiers from Pushover and Sendgrid. Using `SingleMonitorTask` allows us to flexibly add in multiple notifiers.

```python
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

```
