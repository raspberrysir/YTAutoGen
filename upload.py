import httplib2
import os
import random
import time
import logging
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from delete import delete  # Assuming the delete function is in a separate "delete.py" file

# Set your OAuth 2.0 client ID and client secret file (client_secrets.json)
CLIENT_SECRETS_FILE = "client_secrets.json"

# Define the scope and API details
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Define your video properties
VIDEO_FILE = "upload.mp4"
VIDEO_TITLE = "Reddit Video #"
VIDEO_DESCRIPTION = "Bot Generated hottest r/wholesomestories with Subway Surfers Content"
VIDEO_CATEGORY = "22"  # Category ID for gaming
VIDEO_KEYWORDS = ["Reddit", "Subway Surfers"]
VIDEO_PRIVACY_STATUS = "public"  # or "private" or "unlisted"

# Retry parameters
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# Initialize OAuth2 credentials and YouTube service
def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    storage = Storage("oauth2.json")  # This stores your OAuth2 credentials
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

# Upload a video
def upload(index):
    youtube = get_authenticated_service()

    tags = VIDEO_KEYWORDS if VIDEO_KEYWORDS else []
    body = {
        'snippet': {
            'title': VIDEO_TITLE + str(index),
            'description': VIDEO_DESCRIPTION,
            'tags': tags,
            'categoryId': VIDEO_CATEGORY
        },
        'status': {
            'privacyStatus': VIDEO_PRIVACY_STATUS
        }
    }

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

# Resumable video upload
def resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(f"Video id '{response['id']}' was successfully uploaded.")
                else:
                    print("The upload failed with an unexpected response.")
                  # Call the delete function after a successful upload
            return

        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"


