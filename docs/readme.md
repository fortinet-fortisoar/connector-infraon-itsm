## About the connector

Infraon ITSM is a cloud-ready, AI-powered IT Service Management (ITSM) platform that helps organizations manage,
automate, and optimize their entire IT support and service lifecycle — from service requests and incidents to problems,
changes, and compliance.
<p>This document provides information about the Infraon ITSM Connector, which facilitates automated interactions, with a Infraon ITSM server using FortiSOAR&trade; playbooks. Add the Infraon ITSM Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with Infraon ITSM.</p>

### Version information

Connector Version: 1.0.0

Authored By: SpryIQ.co

Contributor: Viveek96

Certified: No

## Installing the connector

<p>Use the <strong>Connector Store</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.<br>You can also use the following <code>yum</code> command to install connectors from an SSH session:</p>

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

For the procedure to configure a connector,
click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)

### Configuration parameters

<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>Infraon ITSM</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations&nbsp;</strong> tab enter the required configuration details:&nbsp;</p>
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Server URL<br></td><td>URL of the Infraon ITSM server to which you will connect and perform automated operations.<br>
<tr><td>Username<br></td><td>Username or Email Address of the Infraon user account to connect and perform the automated operations.<br>
<tr><td>Password<br></td><td>Password the Infraon ITSM server to connect and perform the automated operations.<br>
<tr><td>Verify SSL<br></td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set as True.<br></td></tr>
</tbody></table>

## Actions supported by the connector

The following automated operations can be included in playbooks and you can also use the annotations to access
operations:
<table border=1><thead><tr><th>Function<br></th><th>Description<br></th><th>Annotation and Category<br></th></tr></thead><tbody><tr><td>Create Incident<br></td><td>Create a new incident in the server using the specified summary, requester email, description, and other input parameters that you have specified.<br></td><td>create_incident <br/>Remediation<br></td></tr>
<tr><td>Get Incident Details<br></td><td>Retrieves the full details of a specific incident from the Infraon API using its unique ID.<br></td><td>get_incident_details <br/>Investigation<br></td></tr>
<tr><td>Get All Incident Details<br></td><td>Retrieves a list of all incidents with pagination and filtering from the Infraon.<br></td><td>get_all_incident_details <br/>Investigation<br></td></tr>
<tr><td>Update Incident<br></td><td>Updates an existing incident using its ticket ID and other input parameters that you have specified.<br></td><td>update_incident <br/>Remediation<br></td></tr>
<tr><td>Delete Incident<br></td><td>Deletes an incident using its display ID.<br></td><td>delete_incident <br/>Remediation<br></td></tr>
<tr><td>Add Comment<br></td><td>Adds a new comment to an existing incident.<br></td><td>add_comment <br/>Remediation<br></td></tr>
<tr><td>Add Attachment<br></td><td>Attach a file from FortiSOAR to an existing Infraon ITSM ticket.<br></td><td>submit_file <br/>Remediation<br></td></tr>
</tbody></table>

### operation: Create Incident

#### Input parameters

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Summary<br></td><td>Specify a concise incident title when creating an incident in Infraon ITSM.<br>
</td></tr><tr><td>Requester Email<br></td><td>Specify the email address of the requester who is reporting the incident.<br>
</td></tr><tr><td>Description<br></td><td>Provide a detailed description of the issue, including symptoms, error messages, and any relevant context.<br>
</td></tr><tr><td>Team<br></td><td>Specify the Infraon team responsible for handling this incident.<br>
</td></tr><tr><td>Assignee Email<br></td><td>Specify the email address of the user to whom the incident should be assigned.<br>
</td></tr><tr><td>Urgency<br></td><td>Indicate how urgently the incident needs to be addressed. Possible values are High, Medium, or Low.<br>
</td></tr><tr><td>Priority<br></td><td>Specify the priority level of the incident based on business importance. Possible values are Critical, High, Medium, Low or Very Low.<br>
</td></tr><tr><td>Impact<br></td><td>Describe the impact scope of the incident on users or systems. Possible values are Business, Location, Department, Group, or User.<br>
</td></tr><tr><td>Status<br></td><td>Define the current workflow status of the incident.<br>
</td></tr><tr><td>Severity<br></td><td>Specify the severity level indicating how serious the incident is.<br>
</td></tr><tr><td>Other Fields<br></td><td>Provide any additional custom fields required for incident creation as a JSON object.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Ticket ID<br></td><td>Specify the unique internal Infraon incident identifier for which detailed information needs to be retrieved.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Items Per Page<br></td><td>Specify the number of incidents to be returned per page in the paginated response.<br>
</td></tr><tr><td>Page Number<br></td><td>Specify the page number of the incident list to retrieve.<br>
</td></tr><tr><td>Filters<br></td><td>Provide filtering criteria to narrow down the list of incidents based on specific fields.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Ticket ID<br></td><td>Provide the Infraon display ID of the existing incident that you want to update.<br>
</td></tr><tr><td>Summary<br></td><td>Update the incident summary with a clear and concise title that reflects the current nature or scope of the issue.<br>
</td></tr><tr><td>Description<br></td><td>Update the detailed description of the incident.<br>
</td></tr><tr><td>Status<br></td><td>Update the current workflow status of the incident (e.g., Open, In Progress, On Hold, Resolved, Closed) based on the latest progress.<br>
</td></tr><tr><td>Urgency<br></td><td>Update the urgency level based on how quickly the incident needs to be addressed. Typical values include High, Medium, or Low.<br>
</td></tr><tr><td>Severity<br></td><td>Update the severity level to reflect the current technical impact or extent of service degradation caused by the incident.<br>
</td></tr><tr><td>Priority<br></td><td>Update the priority level based on business impact and urgency. Possible values include Critical, High, Medium, Low, or Very Low.<br>
</td></tr><tr><td>Priority Change Reason<br></td><td>Provide a justification for any change made to the incident priority, explaining the business or technical reason for the update.<br>
</td></tr><tr><td>Team Name<br></td><td>Update the name of the Infraon team currently responsible for handling or owning the incident.<br>
</td></tr><tr><td>Team ID<br></td><td>Update the Infraon team ID corresponding to the team assigned to manage the incident.<br>
</td></tr><tr><td>Assignee Name<br></td><td>Update the name of the user to whom the incident is assigned for investigation or resolution.<br>
</td></tr><tr><td>Assignee Profile<br></td><td>Update the assignee profile that defines the role or access level of the user assigned to this incident.<br>
</td></tr><tr><td>Assignee Profile ID<br></td><td>Update the unique profile ID associated with the user assigned to the incident.<br>
</td></tr><tr><td>Assignee Email<br></td><td>Update the email address of the user currently assigned to the incident.<br>
</td></tr><tr><td>Other Fields<br></td><td>Provide any additional or custom fields required for updating the incident in Infraon as a valid JSON object with key-value pairs.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Ticket ID<br></td><td>Specify the Infraon display ID of the incident that needs to be permanently deleted.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Ticket ID<br></td><td>Specify the Infraon display ID of the incident to which the comment should be added.<br>
</td></tr><tr><td>Comment Text<br></td><td>Provide the comment content to be added to the specified incident.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Ticket ID<br></td><td>Specify the Infraon display ID of the incident to which the file should be attached.<br>
</td></tr><tr><td>Issue Key<br></td><td>Specify the Infraon issue key of the incident to which the file should be attached.<br>
</td></tr><tr><td>Type<br></td><td>Type of file that you want to submit to Infraon for analysis. Type can be an Attachment ID or a File IRI.<br>
</td></tr><tr><td>Reference ID<br></td><td>Reference ID that is used to access the attachment metadata from the FortiSOAR™ Attachments module. In the playbook, this defaults to the{{vars.attachment_id}} value or the {{vars.file_iri}} value.<br>
</td></tr></tbody></table>

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

The `Sample - Infraon ITSM - 1.0.0` playbook collection comes bundled with the Infraon ITSM connector. These playbooks
contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > *
*Playbooks** section in FortiSOAR<sup>TM</sup> after importing the Infraon ITSM connector.

- Create Incident
- Get Incident Details
- Get All Incident Details
- Update Incident
- Delete Incident
- Add Comment
- Add Attachment

----
**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those
playbooks and move them to a different collection, since the sample playbook collection gets deleted during connector
upgrade and delete.
----
