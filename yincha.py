# -*- coding: utf-8 -*-
import os
import time
import datetime

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# break time map
break_map = {
    # start at  |   end at  |   weekday_start   | weekday_end  |
    (datetime.time(hour=12), datetime.time(hour=13, minute=30), 0, 5): {
        "status_text": "睡了，但没完全睡",
        "status_emoji": ":sleeping:",
    },
    (
        datetime.time(hour=13, minute=31),
        datetime.time(hour=13, minute=50),
        0,
        5,
    ): {
        "status_text": "醒了，但没完全醒",
        "status_emoji": ":monkas:",
    },
    (datetime.time(hour=15), datetime.time(hour=16), 0, 5): {
        "status_text": "3点几啦~",
        "status_emoji": ":tea:",
    },
}


def set_slack_status(client: WebClient, status: dict, revert_at: datetime.time):
    now = datetime.datetime.now()
    revert_time = now.replace(
        hour=revert_at.hour,
        minute=revert_at.minute,
        second=revert_at.second,
        microsecond=revert_at.microsecond,
    )

    user_profile_resp = client.users_profile_get()
    if user_profile_resp.status_code != 200:
        print("set profile failed,", user_profile_resp.data)
        raise SlackApiError(response=user_profile_resp.data)

    old_user_profile = {
        "status_text": user_profile_resp["profile"]["status_text"],
        "status_emoji": user_profile_resp["profile"]["status_emoji"],
    }

    new_resp = client.users_profile_set(profile=status)
    if new_resp.status_code != 200:
        print("set profile failed,", new_resp.data)
        raise SlackApiError(response=new_resp.data)

    print(
        "update current new status to: {}".format(
            new_resp["profile"]["status_text"]
        )
    )

    period = revert_time - now
    time.sleep(period.total_seconds())

    revert_resp = client.users_profile_set(profile=old_user_profile)
    if revert_resp.status_code != 200:
        print("set old_user_profile failed", revert_resp.data)
        raise SlackApiError(response=revert_resp.data)

    print("revert to status {}".format(revert_resp["profile"]["status_text"]))


def what_should_i_do() -> (datetime.time, dict):
    curr_time = datetime.datetime.now()
    for key in break_map.keys():
        start_at, end_at, weekday_start, weekday_end = key
        if (
            weekday_start <= curr_time.weekday() <= weekday_end
            and start_at <= curr_time.time() <= end_at
        ):
            return end_at, break_map.get(key)

    return None


if __name__ == "__main__":

    # break time
    resp = what_should_i_do()
    if not resp:
        print("do what you want")
        exit(0)

    end_at, status = resp
    print("get new status conf", status)
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    try:
        set_slack_status(client, status, end_at)
    except SlackApiError as e:
        raise
