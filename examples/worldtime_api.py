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
        task_name="Does Time Flow in Taipei?",
        target_url=(r"http://worldtimeapi.org/api/timezone/Asia/Taipei"),
        exset_name="basic",
        loop_seconds=30,
        loop_max_rounds=86400,
        notify_creds=pushover_creds,
    )
