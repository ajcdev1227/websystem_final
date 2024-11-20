from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class JitsiLinkCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Generate a unique identifier for the meeting
        meeting_id = generate_random_string(20)
        # Construct the Jitsi Meet URL
        jitsi_url = f"home.websystemcontrol.com/meeting/{meeting_id}"
        # Return the Jitsi Meet URL as JSON
        return Response({'meeting_url': jitsi_url}, status=status.HTTP_200_OK)
