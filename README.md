# Akame Monitor

Akame Monitor is a collection of tools useful for web monitoring. It contains a couple of modules such as extraction, comparison, and notification and allows users to design their own units and construct the workflow flexibly.

- [Akame Monitor](#akame-monitor)
  - [Use Cases](#use-cases)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Extractor Sets Available](#extractor-sets-available)

## Use Cases

Some common tasks that Akame Monitor can handle are as follows:

- Extraction: Fetching the response from an API endpoint using a specific request header
- Comparison: Compare the latest API response with the previous version
- Notification: If there is change between the responses, send out a notification through [Pullover](https://pushover.net/)

## Installation

```bash
# cd to the folder to save the script
git clone https://github.com/mcknote/AkameMonitor.git
```

## Usage

Follow these steps to use Akame Monitor:

1. Modify `AkameMonitor/config.json`
   1. `task_name`: The name of this monitoring task; this will appear in the console logs and notification programs.
   2. `target_url`: The URL to be monitored, e.g. an API endpoint or a webpage.
   3. `exset_id`: The ID of Extractor Set, which handles both the URL and content extraction. Default to `BASIC`. See [Extractor Sets Available](##extractor-sets-available) for more details.
   4. `loop_seconds`: The interval in seconds between all monitoring rounds. Default to 30 seconds.
   5. `loop_max_rounds`: The maximum number of rounds to monitor. Default to 86400 rounds (so with 30 seceonds, this would make a one-month monitoring task).
2. Run `AkameMonitor/main.py`

## Extractor Sets Available

| ID | Description | URL Base | Content Extractor |
| --- | --- | --- | --- |
| `BASIC` | The basic extractor set that fetches content directly from only the URL given. In technical terms, this would almost equate to a direct `request.get(target_url)` call. | `core.URLBase` | `basic.BasicExtractor` |
