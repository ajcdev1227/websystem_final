import os

from django.db.models import Q

from compliance.utils import get_cases_count_assigned_to_officer, get_cases_count_for_user_id
from home.constants import COMPLIANCE_STATUS
from home.models import Submission

from home.utils import is_req_user_officer

def global_data(request):
    user_id = request.user.id

    if is_req_user_officer(request):
        compliance_cnt = get_cases_count_assigned_to_officer(user_id, 'pending')
    else:
        compliance_cnt = get_cases_count_for_user_id(user_id, 'pending')

    # TODO Figure out what to do with this
    # compliance_cnt = Submission.objects.filter(Q(status=COMPLIANCE_STATUS["pending"]) & Q(submitter_id=user_id)).count()
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
