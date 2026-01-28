LOGGER_NAME = 'infraon-itsm'

# API Endpoints
ENDPOINTS = {
    'auth': '/ux/api-token-auth/',
    'incident': '/ux/sd/inci/incident/',
    'incident_by_id': '/ux/sd/inci/incident/{id}/',
    'add_comment': '/ux/sd/inci/incident/save-rich-text/',
    'add_attachment': '/ux/sd/inci/incident/add-attachment/'
}