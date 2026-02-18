## About the connector

Infraon ITSM is a cloud-ready, AI-powered IT Service Management (ITSM) platform that helps organizations manage, automate, and optimize their entire IT support and service lifecycle — from service requests and incidents to problems, changes, and compliance.

This document provides information about the Infraon ITSM Connector, which facilitates automated interactions, with a Infraon ITSM server using FortiSOAR&trade; playbooks. Add the Infraon ITSM Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with Infraon ITSM.

### Version information

Connector Version: 1.0.0

Authored By: SpryIQ.co

Contributor: Viveek96

Certified: No

## Installing the connector

Use the **Connector Store** to install the connector. For the detailed procedure to install a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector).

You can also use the following `yum` command to install connectors from an SSH session:

```
sudo yum install cyops-connector-infraon-itsm
```

## Prerequisites to configuring the connector

- You must have the URL of Infraon ITSM server to which you will connect and perform automated operations and
  credentials to access that server.

- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the Infraon ITSM server.

## Minimum Permissions Required

- N/A

## Configuring the connector

For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)

### Configuration parameters

In FortiSOAR™, on the Connectors page, click the **Infraon ITSM** connector row (if you are in the **Grid** view on the Connectors page) and in the **Configurations** tab enter the required configuration details:

| Parameter  | Description                                                                                                                   |
|------------|-------------------------------------------------------------------------------------------------------------------------------|
| Server URL | URL of the Infraon ITSM server to which you will connect and perform automated operations.                                    |
| Username   | Username or Email Address of the Infraon user account to connect and perform the automated operations.                        |
| Password   | Password the Infraon ITSM server to connect and perform the automated operations.                                             |
| Verify SSL | Specifies whether the SSL certificate for the server is to be verified or not.<br />By default, this option is set to `True`. |

## Actions supported by the connector

The following automated operations can be included in playbooks and you can also use the annotations to access operations:

| Function                 | Description                                                                                                                                            | Annotation and Category                     |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| Create Incident          | Creates a new incident on the server based on the specified summary, requester email, description, and other input parameters that you have specified. | create_incident<br />Remediation            |
| Get Incident Details     | Retrieves complete details of an incident from the Infraon API based on the incident's unique ID that you have specified.                              | get_incident_details<br />Investigation     |
| Get All Incident Details | Retrieves a list of all incidents based on the pagination and filtering criteria that you have specified.                                              | get_all_incident_details<br />Investigation |
| Update Incident          | Updates an existing incident using its ticket ID and other input parameters that you have specified.                                                   | update_incident<br />Remediation            |
| Delete Incident          | Deletes an incident using its display ID.                                                                                                              | delete_incident<br />Remediation            |
| Add Comment              | Adds a new comment to an existing incident.                                                                                                            | add_comment<br />Remediation                |
| Add Attachment           | Attaches a file from FortiSOAR to an existing Infraon ITSM ticket.                                                                                     | submit_file<br />Remediation                |

### operation: Create Incident

#### Input parameters

| Parameter       | Description                                                                                                                                     |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| Summary         | Specify a concise incident title when creating an incident in Infraon ITSM.                                                                     |
| Requester Email | Specify the email address of the requester who is reporting the incident.                                                                       |
| Description     | Provide a detailed description of the issue, including symptoms, error messages, and any relevant context.                                      |
| Team            | Specify the Infraon team responsible for handling this incident.                                                                                |
| Assignee Email  | Specify the email address of the user to whom the incident should be assigned.                                                                  |
| Urgency         | Indicate how urgently the incident needs to be addressed. Possible values are *High*, *Medium*, or *Low*.                                       |
| Priority        | Specify the priority level of the incident based on business importance. Possible values are *Critical*, *High*, *Medium*, *Low* or *Very Low*. |
| Impact          | Describe the impact scope of the incident on users or systems. Possible values are *Business*, *Location*, *Department*, *Group*, or *User*.    |
| Status          | Specify the current workflow status of the incident.                                                                                            |
| Severity        | Specify the severity level indicating how serious the incident is.                                                                              |
| Other Fields    | Specify any additional custom fields required for incident creation as a JSON object.                                                           |

#### Output

The output contains the following populated JSON schema:

```
{
    "status": "",
    "id": "",
    "message": "",
    "msg": "",
    "data": {
        "id": "",
        "display_id": "",
        "asset_id": "",
        "summary": "",
        "requester_email": "",
        "priority": "",
        "impact_service": "",
        "creation_time": "",
        "ci_name": ""
    }
}
```

### operation: Get Incident Details

#### Input parameters

| Parameter | Description                                                                                                   |
|-----------|---------------------------------------------------------------------------------------------------------------|
| Ticket ID | Specify the unique internal Infraon incident identifier for which detailed information needs to be retrieved. |

#### Output

The output contains the following populated JSON schema:

```
{
  "incident": {},
  "options": {},
  "status": {},
  "transition_status": {},
  "stage_state_option_map": {}
}
```

### operation: Get All Incident Details

#### Input parameters

| Parameter      | Description                                                                               |
|----------------|-------------------------------------------------------------------------------------------|
| Items Per Page | Specify the number of incidents to be returned per page in the paginated response.        |
| Page Number    | Specify the page number of the incident list to retrieve.                                 |
| Filters        | Provide filtering criteria to narrow down the list of incidents based on specific fields. |

#### Output

The output contains the following populated JSON schema:

```
{
  "count": "",
  "next": "",
  "previous": "",
  "results": [],
  "max_page_limit": ""
}
```

### operation: Update Incident

#### Input parameters

| Parameter              | Description                                                                                                                                  |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| Ticket ID              | Specify the Infraon display ID of an existing incident to update.                                                                            |
| Summary                | Specify an incident summary to update on this incident.                                                                                      |
| Description            | Specify the detailed description to update on this incident.                                                                                 |
| Status                 | Specify the current workflow status to update on this incident. (For example: *Open*, *In Progress*, *On Hold*, *Resolved*, *Closed*).       |
| Urgency                | Specify the urgency level to update on this incident. Typical values include *High*, *Medium*, or *Low*.                                     |
| Severity               | Specify the severity level to update on this incident.                                                                                       |
| Priority               | Specify the priority level to update on this incident. Possible values include *Critical*, *High*, *Medium*, *Low*, or *Very Low*.           |
| Priority Change Reason | Specify a justification for changes made to the priority level of the incident.                                                              |
| Team Name              | Specify the name of the assigned Infraon team to update on this incident.                                                                    |
| Team ID                | Specify the Infraon team ID corresponding to the team assigned to update on this incident.                                                   |
| Assignee Name          | Specify the name of the assigned user to update on this incident.                                                                            |
| Assignee Profile       | Specify the assigned profile to update on this incident. The profile defines the role or access level of the user assigned to this incident. |
| Assignee Profile ID    | Specify the unique profile ID to update on this incident.                                                                                    |
| Assignee Email         | Specify the email address of the user to update on this incident.                                                                            |
| Other Fields           | Specify any additional or custom fields, with values in JSON format to update on this incident.                                              |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "id": "",
  "message": "",
  "msg": ""
}
```

### operation: Delete Incident

#### Input parameters

| Parameter | Description                                                                          |
|-----------|--------------------------------------------------------------------------------------|
| Ticket ID | Specify the Infraon display ID of the incident that needs to be permanently deleted. |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "id": "",
  "message": "",
  "msg": ""
}
```

### operation: Add Comment

#### Input parameters

| Parameter    | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Ticket ID    | Specify the Infraon display ID of the incident on which to add the comment. |
| Comment Text | Specify text to add to the comment.                                         |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "id": "",
  "message": "",
  "msg": "",
  "data": {
    "comment": "",
    "display_id": "",
    "ref_id": ""
  }
}
```

### operation: Add Attachment

#### Input parameters

| Parameter    | Description                                                                                                                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ticket ID    | Specify the Infraon display ID of the incident to which the file should be attached.                                                                                                                         |
| Issue Key    | Specify the Infraon issue key of the incident to which the file should be attached.                                                                                                                          |
| Type         | Select the type of file to submit to Infraon for analysis. The file type can be an *Attachment ID* or a *File IRI*.                                                                                          |
| Reference ID | Specify the reference ID to access the attachment metadata from the FortiSOAR **Attachments** module. In the playbook, this defaults to the `{{vars.attachment_id}}` value or the `{{vars.file_iri}}` value. |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "id": "",
  "message": "",
  "msg": ""
}
```

## Included playbooks

The *`Sample - Infraon ITSM - 1.0.0`* playbook collection comes bundled with the Infraon ITSM connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR after importing the Infraon ITSM connector.

- Create Incident
- Get Incident Details
- Get All Incident Details
- Update Incident
- Delete Incident
- Add Comment
- Add Attachment

____
**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those
playbooks and move them to a different collection, since the sample playbook collection gets deleted during connector
upgrade and delete.
____
