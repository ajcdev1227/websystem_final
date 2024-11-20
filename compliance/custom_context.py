import os

from django.db.models import Q

from home.constants import COMPLIANCE_STATUS
from home.models import Submission


def global_data(request):
    user_id = request.user.id
    # TODO Figure out what to do with this
    #compliance_cnt = Submission.objects.filter(Q(status=COMPLIANCE_STATUS["pending"]) & Q(submitter_id=user_id)).count()
    compliance_cnt = 10
    approved_cnt = Submission.objects \
        .filter(Q(status=COMPLIANCE_STATUS["approved"]) & Q(checked=0) & Q(submitter_id=user_id)).count()

    JITSI_APP_ID = os.getenv('JITSI_APP_ID', None)
    JITSI_APP_JWT_KEY = os.getenv('JITSI_APP_JWT_KEY', None)
    return {
        'compliance_cnt': compliance_cnt,
        'approved_cnt': approved_cnt,
        'JITSI_APP_ID': JITSI_APP_ID,
        'JITSI_APP_JWT_KEY': JITSI_APP_JWT_KEY
    }
