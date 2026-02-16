"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""

LOGGER_NAME = 'infraon-itsm'

# API Endpoints
ENDPOINTS = {
    'auth': '/ux/api-token-auth/',
    'incident': '/ux/sd/inci/incident/',
    'incident_by_id': '/ux/sd/inci/incident/{id}/',
    'add_comment': '/ux/sd/inci/incident/save-rich-text/',
    'add_attachment': '/ux/sd/inci/incident/add-attachment/'
}

# Static maps
urgency_map = {
    "low": 3,
    "medium": 2,
    "high": 1
}

priority_map = {
    "very low": 5,
    "low": 4,
    "medium": 3,
    "high": 2,
    "critical": 1
}

impact_map = {
    "business": 1,
    "location": 2,
    "department": 3,
    "group": 4,
    "user": 5
}
