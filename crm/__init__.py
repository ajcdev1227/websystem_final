
# Work here Hi, I fixed the issue.

import json
import urllib.parse
from typing import Optional

import requests
from datetime import datetime
from dateutil import parser as dt_parser

from compliance.models import Case
from home.constants import CRM_ROOT, CRM_API_KEY


class CrmComplianceCase(object):
    """
    A compliance case from the CRM
    """

    id: int

    acx_customer_id: str

    item_id: int

    item_type_id: int

    type: str

    created_ts: datetime

    review_no: int

    status = 'pending'  # Implicitly pending for now


class CrmComplianceCaseItem(object):
    """
    An item associated with a compliance case from the CRM
    """

    subject: Optional[str]
    '''Item subject, or None if not available'''

    body: str
    '''The item body (possibly HTML if it is an email template)'''


def parse_crm_compliance_cases(json_array) -> list[CrmComplianceCase]:
    """
    Parses a JSON array of CRM compliance case objects
    """

    res = []

    if isinstance(json_array, str):
        arr = json.loads(json_array)
    else:
        arr = json_array
    if arr is not None: # Added None fix
        for case in arr:
            obj = CrmComplianceCase()

            obj.id = case['moderation_id']
            obj.acx_customer_id = case['acx_customer_id']
            obj.item_id = case['item_id']
            obj.item_type_id = case['item_type_id']
            obj.type = case['type']

            date_val = case['date_submitted']

            if date_val is str:
                obj.created_ts = dt_parser.parse(date_val)
            else:
                obj.created_ts = datetime.fromtimestamp(date_val)

            obj.review_no = case['review_no']

            res.append(obj)

    return res


def fetch_all_crm_compliance_cases() -> list[CrmComplianceCase]:
    """
    Fetches all CRM compliance cases
    """

    url = CRM_ROOT + '/api/v1/compliance'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Apikey': CRM_API_KEY,
    }
    return parse_crm_compliance_cases(requests.get(url, headers=headers).text)


def fetch_crm_compliance_case_by_id(case_id: int) -> CrmComplianceCase:
    """
    Fetches the CRM compliance case with the specified ID, or None if not found
    """

    cases = fetch_all_crm_compliance_cases()

    for case in cases:
        if case.id == case_id:
            return case

    return None


def approve_crm_compliance_case(case: CrmComplianceCase):
    """
    Approves the specified CRM compliance case
    """

    url = f'{CRM_ROOT}/api/v1/compliance-approve/{case.item_id}/0'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Apikey': CRM_API_KEY,
    }
    requests.get(url, headers=headers)


def reject_crm_compliance_case(case: CrmComplianceCase, note: str):
    """
    Rejects the specified CRM compliance case
    """

    url = f'{CRM_ROOT}/api/v1/compliance-fail.php'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Apikey': CRM_API_KEY,
    }
    params = {
        'item_id': case.item_id,
        'item_type_id': case.item_type_id,
        'note': note,
    }
    requests.get(url, headers=headers, params=params)


def crm_case_to_case(crm_case: CrmComplianceCase) -> Case:
    """
    Converts a CrmComplianceCase object to a Case object
    """

    res = Case()
    res.id = crm_case.id
    res.uuid = 'crm:' + str(crm_case.id)
    res.created_ts = crm_case.created_ts
    res.updated_ts = None
    res.approved_ts = None
    res.rejected_ts = None
    res.resource_title = crm_case.type
    res.resource_key = f'{crm_case.item_type_id}:{crm_case.item_id}'
    res.type = 'crm'
    res.status = 'pending'
    res.reviewed_by = None
    res.officer_notes = None
    res.tenant = None

    return res


def fetch_crm_case_item(case: CrmComplianceCase) -> Optional[CrmComplianceCaseItem]:
    """
    Fetches data about a CRM compliance case
    """

    url = f'{CRM_ROOT}/api/v1/compliance-item/{case.item_id}/{case.item_type_id}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Apikey': CRM_API_KEY,
    }
    obj_res = json.loads(requests.get(url, headers=headers).text)

    if len(obj_res) < 1:
        return None

    obj = obj_res[0]

    res = CrmComplianceCaseItem()
    res.subject = obj.get('subject')
    res.body = obj['body']

    return res
