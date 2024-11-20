from datetime import datetime
from enum import Enum
from typing import Union
from logging import warning

from nylas import APIClient
from nylas.client.restful_models import Event

from home.models import CustomUser, Meetings
from home.utils import create_nylas_client_for_user


# Stuff
