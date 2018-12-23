from main import RedditApi
from main import hangoutsApi
from PIL import Image
import requests
from io import BytesIO
import virtualenv
from twilio.rest import Client


import urllib

def getCatPhoto(api,i=0):
    for submission in api.reddit.subreddit("aww").hot(limit=40):
        if(submission.url.endswith("jpg")):
            i += 1
            if i > 2:
                return submission.url

reddit = RedditApi()
reddit.getAuthToken()
image = getCatPhoto(reddit)

# Your Account Sid and Auth Token from twilio.com/console
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="These should show up on schedule now!",
                     from_='+',
                     media_url=image,
                     to='+'
                 )
print(message.sid)
