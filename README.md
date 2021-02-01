# Akame Monitor

Akame Monitor is a collection of tools to constantly monitor web changes. It contains a couple of modules such as extraction, comparison, and notification and allows users to design their own units and flexibly construct the monitoring workflow.

- [Akame Monitor](#akame-monitor)
  - [Use Cases](#use-cases)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Extraction Sets Available](#extraction-sets-available)

## Use Cases

Akame Monitor can **monitor a web change every X seconds for Y rounds**. Specifically, some common tasks that Akame Monitor can handle are as follows:

- Extraction: Fetching the response from an API endpoint using a specific request header
- Comparison: Compare the latest API response against the previous version
- Notification: Send out a notification through [Pullover](https://pushover.net/) if there are changes between the monitored content

## Installation

```bash
# switch to the download folder as necessary
$ git clone https://github.com/mcknote/AkameMonitor.git
```

## Usage

```python
from os import environ

from akame import run_task

# credentials specific to pushover
pushover_creds = {
    "token": environ["PUSHOVER_TOKEN"],
    "user_key": environ["PUSHOVER_USERKEY"],
}

if __name__ == "__main__":
    run_task(
        task_name="Does Time Flow in Taipei?",
        target_url=(r"http://worldtimeapi.org/api/timezone/Asia/Taipei"),
        exset_name="basic",
        loop_seconds=30,
        loop_max_rounds=86400,
        notify_creds=pushover_creds,
    )

```

Parameters for `akame.run_task`:

- `task_name`: Name of the monitoring task; this will appear in the console logs and notification programs.
- `target_url`: URL to be monitored, e.g. an API endpoint or a webpage.
- `exset_name`: Name of the extraction set, which handles both the URL and content extraction. Default to `basic`. See [Extraction Sets Available](#extraction-sets-available) for more details.
- `loop_seconds`: Interval in seconds between all monitoring rounds. Default to `30` seconds.
- `loop_max_rounds`: Maximum number of rounds to monitor. Default to `86400` rounds (so with 30 seceonds, this would make a one-month monitoring task).
- `notify_creds`: Crentials to be used in the notifier, which is default to Pushover and requires two attributes: `token` and `user_key`.

## Extraction Sets Available

All available extraction sets are located under `akame.extraction.sets`.

| Name | Description |
| --- | --- |
| `basic` | The basic extraction set that almost equates to a `requests.get(target_url)` call. |
