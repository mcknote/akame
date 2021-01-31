from os import environ

from akame_monitor import run_task

notify_creds = {
    "token": environ["PUSHOVER_TOKEN"],
    "user_key": environ["PUSHOVER_USERKEY"],
}

if __name__ == "__main__":
    run_task(
        task_name="Akame Reservation",
        target_url=(
            "https://inline.app/api/booking-capacities?"
            "\companyId=-LzoDiSgrwoz1PHLtibz%3Ainline-live-1"
            "&branchId=-LzoDjNruO8RBsVIMQ9W"
        ),
        exset_id="BASIC",
        loop_seconds=2,
        loop_max_rounds=10,
        notify_creds=notify_creds,
    )
