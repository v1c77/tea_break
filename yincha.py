# -*- coding: utf-8 -*-
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time
import datetime

now = datetime.datetime.now()

# quit if not in 15.
if now.hour != 15 or now.weekday() > 4:
    print("do what you want...")
    exit(0)

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])


user_profile_resp = client.users_profile_get()
if user_profile_resp.status_code != 200:
    exit(1)

user_profile = user_profile_resp['profile']

old_user_profile={
    'status_text': user_profile_resp['profile']['status_text'],
    'status_empji':user_profile_resp['profile']['status_emoji']
}

new_status={'status_text': "喂, 3点几啦~", 'status_emoji': ":tea:"}

new_resp = client.users_profile_set(profile=new_status)
if new_resp.status_code != 200:
    print("set profile failed,")
    exit(1)
print("update current new status to: {}".format(new_resp['profile']['status_text']))


time.sleep(3600)

revert_resp = client.users_profile_set(profile=old_user_profile)
if revert_resp.status_code != 200:
    print("set old_user_profile failed")
    exit(1)
print("revert to status {}".format(revert_resp['profile']['status_text']))
