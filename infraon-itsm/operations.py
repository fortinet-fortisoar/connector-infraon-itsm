"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""

import requests
import json
import base64
import mimetypes
from os.path import join
from datetime import datetime, timezone

from .auth import InfraonAuth
from .constants import LOGGER_NAME, ENDPOINTS, impact_map, urgency_map, priority_map

try:
    from connectors.core.connector import get_logger, ConnectorError
    from connectors.cyops_utilities.builtins import download_file_from_cyops
    from integrations.crudhub import make_request
except:
    pass

logger = get_logger(LOGGER_NAME)


class InfraonClient:
    """
    Wrapper for Infraon API calls
    """

    def __init__(self, config):
        self.config = config
        self.auth = InfraonAuth(config)
        self.server_url = self.auth.server_url
        self.verify_ssl = self.auth.verify_ssl

    def make_request(self, method, endpoint, params=None, json_data=None):
        """
        Handles the specific request logic from original _make_api_call
        """
        url = f"{self.server_url}{endpoint}"
        headers = self.auth.get_auth_header()

        # Original logic: Handle data_payload vs json_payload specific to Infraon
        data_payload = None
        json_payload = None
        if method.upper() == 'GET' and json_data is not None:
            data_payload = json.dumps(json_data)
        else:
            json_payload = json_data

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data_payload,
                json=json_payload,
                verify=self.verify_ssl
            )

            if response.ok:
                return response.json() if response.text else {"status": "success"}
            else:
                raise ConnectorError(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            raise ConnectorError(str(e))


def check_health(config):
    """Health check implementation"""
    client = InfraonClient(config)
    # Just generating a token is sufficient for health check per original code
    client.auth.get_access_token()
    return True


# --- Helper Functions (Preserved from original) ---
# --- New helper for resolving team/user during updates ---
def _resolve_team_and_user_for_update(incident_data, team_name=None, assignee_name=None,
                                      team_id=None, assignee_profile_id=None, assignee_email=None):
    """
    Resolve team and user identifiers using incident_data['options'] and other incident fields.
    Supports resolution by:
      - team_id or team_name -> team.team_id
      - assignee_profile_id -> direct
      - assignee_email -> looks in options['users'], selected_assignee_info.profile, teams owners/staffs
      - assignee_name -> matches users[].full_name
    Returns a dict that may contain: group, group_name, assignee, assignee_profile
    Raises ConnectorError if a provided name/email cannot be found.
    """
    assignment_payload = {}
    options = incident_data.get('options', {}) if incident_data else {}
    all_teams = options.get('teams', []) or []

    # --- Team resolution ---
    if team_id:
        assignment_payload['group'] = team_id
        team_obj = next((t for t in all_teams if t.get('team_id') == team_id or t.get('id') == team_id), None)
        assignment_payload['group_name'] = team_obj.get('name') if team_obj else None
    elif team_name:
        team_obj = next((t for t in all_teams if t.get('name', '').lower() == team_name.lower()), None)
        if not team_obj:
            raise ConnectorError(f"Team '{team_name}' not found.")
        assignment_payload['group'] = team_obj.get('team_id') or team_obj.get('id')
        assignment_payload['group_name'] = team_obj.get('name')

    # Helper to compare emails safely
    def _matches_email(candidate, target_email):
        if not candidate or not target_email:
            return False
        try:
            return str(candidate).strip().lower() == target_email.strip().lower()
        except Exception:
            return False

    # --- User resolution: priority order ---
    # 1) Direct profile_id if provided
    if assignee_profile_id:
        assignment_payload['assignee'] = assignee_profile_id
        # try to attach full profile if available
        all_users = options.get('users', []) or []
        user_obj = next((u for u in all_users if
                         u.get('profile_id') == assignee_profile_id or u.get('user') == assignee_profile_id), None)
        if user_obj:
            assignment_payload['assignee_profile'] = user_obj
        return assignment_payload

    # 2) Resolve by email if provided
    if assignee_email:
        email = assignee_email.strip().lower()
        # Search options.users
        for u in options.get('users', []) or []:
            if _matches_email(u.get('email'), email) or _matches_email(u.get('ci_descr'), email):
                assignment_payload['assignee'] = u.get('profile_id') or u.get('user')
                assignment_payload['assignee_profile'] = u
                return assignment_payload

        # Search selected_assignee_info.profile
        sel = incident_data.get('selected_assignee_info') or {}
        profile = sel.get('profile') if isinstance(sel, dict) else None
        if profile and (_matches_email(profile.get('email'), email) or _matches_email(
                profile.get('unmasked_email') if profile.get('unmasked_email') else None, email)):
            assignment_payload['assignee'] = profile.get('profile_id') or profile.get('user')
            assignment_payload['assignee_profile'] = profile
            return assignment_payload

        # Search current_assignment_info.assignee_profile
        current = incident_data.get('incident', {}).get('current_assignment_info', {}) or {}
        ass_prof = current.get('assignee_profile') or {}
        if ass_prof and _matches_email(ass_prof.get('email'), email):
            assignment_payload['assignee'] = ass_prof.get('profile_id') or ass_prof.get('user')
            assignment_payload['assignee_profile'] = ass_prof
            return assignment_payload

        # Search within teams -> staffs and owner lists
        for team in all_teams:
            for staff in team.get('staffs', []) + team.get('owner', []):
                if _matches_email(staff.get('email'), email):
                    assignment_payload['assignee'] = staff.get('profile_id') or staff.get('user')
                    # build a minimal assignee_profile from staff entry
                    assignment_payload['assignee_profile'] = {
                        "profile_id": staff.get('profile_id'),
                        "full_name": staff.get('full_name') or staff.get('name'),
                        "email": staff.get('email')
                    }
                    return assignment_payload

        # not found by email
        raise ConnectorError(f"No user found with email '{assignee_email}'")

    # 3) Resolve by assignee_name if provided
    if assignee_name:
        for u in options.get('users', []) or []:
            if str(u.get('full_name', '')).strip().lower() == assignee_name.strip().lower():
                assignment_payload['assignee'] = u.get('profile_id') or u.get('user')
                assignment_payload['assignee_profile'] = u
                return assignment_payload

        # fallback search in teams staff/owner
        for team in all_teams:
            for staff in team.get('staffs', []) + team.get('owner', []):
                if str(staff.get('full_name', staff.get('name', ''))).strip().lower() == assignee_name.strip().lower():
                    assignment_payload['assignee'] = staff.get('profile_id') or staff.get('user')
                    assignment_payload['assignee_profile'] = {
                        "profile_id": staff.get('profile_id'),
                        "full_name": staff.get('full_name') or staff.get('name'),
                        "email": staff.get('email')
                    }
                    return assignment_payload

        raise ConnectorError(f"Assignee with name '{assignee_name}' not found.")

    # nothing requested
    return assignment_payload


def _find_incident_id(client, display_id):
    logger.info(f"Searching for incident with Display ID: {display_id}")

    endpoint = ENDPOINTS['incident']
    target_id = str(display_id).strip().lower()

    page = 1
    items_per_page = 100
    max_pages = 300

    while page <= max_pages:
        params = {
            "items_per_page": items_per_page,
            "page": page
        }

        logger.info(f"Requesting incidents - page {page}")

        try:
            response = client.make_request("GET", endpoint, params=params)
        except Exception as e:
            logger.error(f"API call failed on page {page}: {str(e)}")
            raise ConnectorError("Failed to query incidents API")

        results = response.get("results") if response else None

        if not results:
            logger.info(f"No results returned on page {page}. Stopping pagination.")
            break

        for inc in results:
            disp_id = str(inc.get("display_id", "")).strip().lower()

            if disp_id == target_id:
                incident_id = (
                        inc.get("incident_id") or
                        inc.get("id") or
                        inc.get("uuid")
                )

                if not incident_id:
                    raise ConnectorError("Incident found but no incident identifier present")

                logger.info(f"Found Incident ID: {incident_id} for Display ID: {display_id}")
                return incident_id

        # Stop conditions
        total_pages = response.get("total_pages")

        if total_pages:
            if page >= int(total_pages):
                break
        else:
            if len(results) < items_per_page:
                break

        page += 1

    raise ConnectorError(
        f"No matching incident found for Display ID: {display_id} after scanning {page - 1} pages"
    )


def _find_option_obj(options_data, name_to_find, field_name):
    if not name_to_find:
        return None
    name_to_find_lower = name_to_find.lower()
    options_iterable = []
    if isinstance(options_data, dict):
        options_iterable = options_data.values()
    elif isinstance(options_data, list):
        options_iterable = options_data
    found_obj = next((opt for opt in options_iterable if opt.get('name', '').lower() == name_to_find_lower), None)
    if not found_obj:
        valid_names = list(set(opt.get('name') for opt in options_iterable if opt.get('name')))
        raise ConnectorError(f"Invalid {field_name} '{name_to_find}'. Valid options are: {valid_names}")
    return found_obj


def _get_file_data(iri_type, iri):
    try:
        file_name = None
        if iri_type == 'Attachment ID':
            if not iri.startswith('/api/3/attachments/'):
                iri = f'/api/3/attachments/{iri}'
            attachment_data = make_request(iri, 'GET')
            file_iri = attachment_data['file']['@id']
            file_name = attachment_data['file']['filename']
        else:
            file_iri = iri
        file_download_response = download_file_from_cyops(file_iri)
        if not file_name:
            file_name = file_download_response['filename']
        file_path = join('/tmp', file_download_response['cyops_file_path'])
        logger.info(f'File ID = {file_iri}, File Name = {file_name}')
        return file_name, file_path
    except Exception as err:
        logger.exception(str(err))
        raise ConnectorError(f'Could not find attachment with ID {iri}')


# --- Main Operations ---

def get_incident_details(config, params, **kwargs):
    client = InfraonClient(config)
    display_id = params.get('ticket_id')

    incident_id = _find_incident_id(client, display_id)
    endpoint = ENDPOINTS['incident_by_id'].format(id=incident_id)
    return client.make_request('GET', endpoint)


def get_all_incident_details(config, params, **kwargs):
    client = InfraonClient(config)
    query_params = {
        "items_per_page": params.get('items_per_page', 50),
        "page": params.get('page', 1)
    }
    body = {"filters": params.get('filters', {})}
    endpoint = ENDPOINTS['incident']
    return client.make_request('GET', endpoint, params=query_params, json_data=body)


def update_incident(config, params, **kwargs):
    client = InfraonClient(config)
    display_id = params.get('display_id')
    if not display_id:
        raise ConnectorError("Missing required parameter: 'display_id'")

    incident_id = _find_incident_id(client, display_id)

    # Step 1: Fetch current data
    get_endpoint = ENDPOINTS['incident_by_id'].format(id=incident_id)
    incident_data = client.make_request('GET', get_endpoint)

    payload = incident_data.get('incident', {})
    if not payload:
        raise ConnectorError("Could not retrieve incident data to perform an update.")

    basic_info = payload.setdefault('basic_info', {})
    options = incident_data.get('options', {})

    # Step 2: Update fields (existing)
    if params.get('summary'):
        basic_info['summary'] = params['summary']
    if params.get('description'):
        basic_info['description'] = params['description']

    if params.get('status'):
        all_statuses = options.get('status', [])
        status_obj = _find_option_obj(all_statuses, params['status'], 'Status')
        if status_obj:
            basic_info['status'] = status_obj

    if params.get('urgency'):
        all_urgencies = options.get('urgency', [])
        urgency_obj = _find_option_obj(all_urgencies, params['urgency'], 'Urgency')
        if urgency_obj:
            basic_info['urgency'] = urgency_obj

    if params.get('severity'):
        all_severities = options.get('severity', [])
        severity_obj = _find_option_obj(all_severities, params['severity'], 'Severity')
        if severity_obj:
            basic_info['severity'] = severity_obj

    new_priority_name = params.get('priority')
    priority_change_reason = params.get('priority_change_reason')
    if new_priority_name:
        if not priority_change_reason:
            raise ConnectorError("A 'Priority Change Reason' is required when changing the priority.")

        priority_matrix = options.get('priority_matrix', {})
        priority_obj = _find_option_obj(priority_matrix, new_priority_name, 'Priority')
        if priority_obj:
            basic_info['priority'] = priority_obj
            payload['temp_priority'] = priority_obj
            payload['comment'] = {
                "description": f"<p>{priority_change_reason}</p>",
                "type": "Priority Change",
                "is_private": False
            }

    # --- Other fields (flatten inline) ---
    other_fields = params.get('other_fields')
    if other_fields:
        if not isinstance(other_fields, dict):
            logger.warning("Parameter 'other_fields' is not a valid JSON object and will be ignored.")
        else:
            for key, value in other_fields.items():
                # incident -> basic_info -> fields
                if key == "incident" and isinstance(value, dict):
                    bi = value.get("basic_info")
                    if isinstance(bi, dict):
                        basic_info.update(bi)

                # basic_info -> fields
                elif key == "basic_info" and isinstance(value, dict):
                    basic_info.update(value)

                # flat fields
                else:
                    basic_info[key] = value

    # --- Assignment merge ---
    team_name = params.get('team_name')
    team_id = params.get('team_id')
    assignee_name = params.get('assignee_name')
    assignee_profile_id = params.get('assignee_profile') or params.get('assignee_profile_id')
    assignee_email = params.get('assignee_email')

    if team_name or team_id or assignee_name or assignee_profile_id or assignee_email:
        assignment_payload = _resolve_team_and_user_for_update(
            incident_data,
            team_name=team_name,
            assignee_name=assignee_name,
            team_id=team_id,
            assignee_profile_id=assignee_profile_id,
            assignee_email=assignee_email
        )

        current_assignment = payload.setdefault('current_assignment_info', {})
        current_assignment.update(assignment_payload)

    # Step 3: Submit update
    payload['last_update_time'] = datetime.now(timezone.utc).isoformat()
    update_endpoint = ENDPOINTS['incident_by_id'].format(id=incident_id)
    update_result = client.make_request('PUT', update_endpoint, json_data=payload)

    if isinstance(update_result, dict) and update_result.get('status') == 'error':
        error_msg = update_result.get('msg', 'Unknown API error')
        raise ConnectorError(f"API Error: {error_msg}")

    return update_result


def add_comment(config, params, **kwargs):
    client = InfraonClient(config)
    display_id = params.get('display_id')
    comment_text = params.get('comment')
    if not display_id:
        raise ConnectorError("Missing required parameter: 'display_id'")
    if not comment_text:
        raise ConnectorError("Missing required parameter: 'comment'")

    incident_id = _find_incident_id(client, display_id)
    endpoint = ENDPOINTS['add_comment']

    payload = {
        "ref_id": incident_id,
        "rich_text_content": {
            "description": f"<p>{comment_text}</p>",
            "type": "Add Notes",
            "is_private": False,
            "work_duration": {}
        }
    }
    logger.info(f"Adding comment to incident with Display ID: {display_id}")
    return client.make_request('POST', endpoint, json_data=payload)


# --- Modified create_incident ---
def create_incident(config, params, **kwargs):
    client = InfraonClient(config)

    summary = params.get('summary')
    requester_email = params.get('requester_email')
    description = params.get('description', '')

    payload = {
        "summary": summary,
        "description": description,
        "requester_email": requester_email,
        "incident_type": {"id": 1, "name": "Incident", "prefix": "inci"}
    }

    if params.get('requester_name'):
        payload["requester_name"] = params["requester_name"]

    # Lookup fields using mapping
    def set_field_from_map(param_name, lookup_map, payload_key):
        value = params.get(param_name)
        if value:
            key = value.lower()
            if key not in lookup_map:
                raise ConnectorError(
                    f"Invalid value '{value}' for '{param_name}'. Valid: {list(lookup_map.keys())}"
                )
            payload[payload_key] = {"id": lookup_map[key], "name": value}

    set_field_from_map("urgency", urgency_map, "urgency")
    set_field_from_map("priority", priority_map, "priority")
    set_field_from_map("impact", impact_map, "impact")

    # Status (name-only)
    if params.get("status"):
        payload["status"] = {"name": params["status"]}

    # Severity (name-only)
    if params.get("severity"):
        payload["severity"] = {"name": params["severity"]}

    # Assignment (store-only)
    team_name = params.get("team_name")
    assignee_name = params.get("assignee_name")
    assignee_email = params.get("assignee_email")

    if team_name or assignee_name or assignee_email:
        assignment_info = {}

        if team_name:
            assignment_info["group_name"] = team_name

        if assignee_name or assignee_email:
            assignment_info["assignee_profile"] = {}
            if assignee_name:
                assignment_info["assignee_profile"]["full_name"] = assignee_name
            if assignee_email:
                assignment_info["assignee_profile"]["email"] = assignee_email

        payload["current_assignment_info"] = assignment_info

    # Other fields (flatten inline)
    other_fields = params.get("other_fields")
    if other_fields:
        if not isinstance(other_fields, dict):
            raise ConnectorError("Parameter 'other_fields' must be a JSON object")

        for key, value in other_fields.items():
            # Handle incident -> basic_info -> fields
            if key == "incident" and isinstance(value, dict):
                basic_info = value.get("basic_info")
                if isinstance(basic_info, dict):
                    payload.update(basic_info)

            # Handle basic_info -> fields
            elif key == "basic_info" and isinstance(value, dict):
                payload.update(value)

            # Flat fields (preferred)
            else:
                payload[key] = value

    endpoint = ENDPOINTS['incident']
    logger.info(f"Creating new incident with payload: {payload}")
    return client.make_request("POST", endpoint, json_data=payload)


def delete_incident(config, params, **kwargs):
    client = InfraonClient(config)
    display_id = params.get('display_id')
    if not display_id:
        raise ConnectorError("Missing required parameter: 'display_id'")

    incident_id = _find_incident_id(client, display_id)
    endpoint = ENDPOINTS['incident_by_id'].format(id=incident_id)

    logger.info(f"Deleting incident with Display ID: {display_id} (Internal ID: {incident_id})")
    return client.make_request('DELETE', endpoint)


def submit_file(config, params, **kwargs):
    client = InfraonClient(config)
    display_id = params.get('display_id') or params.get('issue_key')
    if not display_id:
        raise ConnectorError("Missing required parameter: 'display_id' or 'issue_key'")

    incident_id = _find_incident_id(client, display_id)
    iri_type = params.get('path')
    iri = params.get('value')
    if not iri_type or not iri:
        raise ConnectorError("Missing required file parameters: 'path' and 'value'")

    file_name, file_path = _get_file_data(iri_type, iri)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    with open(file_path, 'rb') as f:
        file_bytes = f.read()
        encoded_file = base64.b64encode(file_bytes).decode('utf-8')
        file_data = f"data:{mime_type};base64,{encoded_file}"
        formatted_size = f"{round(len(file_bytes) / 1024, 1)} KB"

    payload = {
        "incidentId": incident_id,
        "files": [
            {
                "file_data": file_data,
                "formatted_size": formatted_size,
                "file_name": file_name
            }
        ]
    }
    endpoint = ENDPOINTS['add_attachment']
    logger.info(f"Adding attachment '{file_name}' to incident Display ID: {display_id}")
    return client.make_request('POST', endpoint, json_data=payload)


operations = {
    'get_incident_details': get_incident_details,
    'get_all_incident_details': get_all_incident_details,
    'update_incident': update_incident,
    'add_comment': add_comment,
    'create_incident': create_incident,
    'delete_incident': delete_incident,
    'submit_file': submit_file
}
