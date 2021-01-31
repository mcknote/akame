from os import environ

from akame_monitor import run_task

# credentials specific to pushover
pushover_creds = {
    "token": environ["PUSHOVER_TOKEN"],
    "user_key": environ["PUSHOVER_USERKEY"],
}

if __name__ == "__main__":
    run_task(
        task_name="Akame Reservation",
        target_url=(
            r"https://inline.app/api/booking-capacities?"
            r"companyId=-LzoDiSgrwoz1PHLtibz%3Ainline-live-1"
            r"&branchId=-LzoDjNruO8RBsVIMQ9W"
        ),
        exset_id="BASIC",
        loop_seconds=30,
        loop_max_rounds=86400,
        notify_creds=pushover_creds,
    )
