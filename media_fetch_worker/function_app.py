
import hashlib
import json
import logging
import os
from datetime import datetime, timezone

import azure.functions as func
import feedparser  # type: ignore[import-untyped]
from azure.functions import TimerRequest
from azure.storage.blob import BlobServiceClient, ContentSettings

STORAGE_CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
RAW_CONTAINER_NAME = os.environ.get("RAW_CONTAINER_NAME", "media-raw-store")
FEED_CONFIG = [{}]

app = func.FunctionApp()
