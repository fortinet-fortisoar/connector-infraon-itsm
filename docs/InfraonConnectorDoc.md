## About the connector
Connector for the Infraon ITSM API to manage incidents and tickets.
<p>This document provides information about the Infraon ITSM Connector, which facilitates automated interactions, with a Infraon ITSM server using FortiSOAR&trade; playbooks. Add the Infraon ITSM Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with Infraon ITSM.</p>

### Version information

Connector Version: 1.0.1


Authored By: Community

Certified: No

## Installing the connector
<p>Use the <strong>Content Hub</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.</p><p>You can also use the <code>yum</code> command as a root user to install the connector:</p>
<pre>yum install cyops-connector-infraon</pre>

## Prerequisites to configuring the connector
- You must have the credentials of Infraon ITSM server to which you will connect and perform automated operations.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the Infraon ITSM server.

## Minimum Permissions Required
- Not applicable

## Configuring the connector
For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)
### Configuration parameters
<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>Infraon ITSM</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations</strong> tab enter the required configuration details:</p>
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Server URL</td><td>The base API endpoint of your Infraon ITSM instance. This URL is provided by Infraon and is unique to each customer environment.
</td>
</tr><tr><td>Username</td><td>Username or email address of the Infraon user account that FortiSOAR will use to authenticate and perform ticket operations.
</td>
</tr><tr><td>Password</td><td>Password associated with the Infraon user account. This value is stored securely by FortiSOAR and is used only for authentication.
</td>
</tr><tr><td>Verify SSL</td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set to True.</td></tr>
</tbody></table>

## Actions supported by the connector
The following automated operations can be included in playbooks and you can also use the annotations to access operations from FortiSOAR&trade; release 4.10.0 and onwards:
<table border=1><thead><tr><th>Function</th><th>Description</th><th>Annotation and Category</th></tr></thead><tbody><tr><td>Create Incident</td><td>Creates a new incident in Infraon ITSM.</td><td>create_incident <br/>Remediation</td></tr>
<tr><td>Get Incident Details</td><td>Retrieves the full details of a specific incident from the Infraon API using its unique ID.</td><td>get_incident_details <br/>Investigation</td></tr>
<tr><td>Get All Incident Details</td><td>Retrieves a list of all incidents with pagination and filtering.</td><td>get_all_incident_details <br/>Investigation</td></tr>
<tr><td>Update Incident</td><td>Updates an existing incident using its Display ID.</td><td>update_incident <br/>Remediation</td></tr>
<tr><td>Add Comment</td><td>Adds a new comment to an existing incident.</td><td>add_comment <br/>Remediation</td></tr>
<tr><td>Delete Incident</td><td>Deletes an incident using its Display ID.</td><td>delete_incident <br/>Remediation</td></tr>
<tr><td>Add Attachment</td><td>Attach a file from FortiSOAR to an existing Infraon ITSM ticket.</td><td>submit_file <br/>Remediation</td></tr>
</tbody></table>

### operation: Create Incident
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Summary</td><td>Short title of the incident. Example: VPN connection failed
</td></tr><tr><td>Requester Email</td><td>Email address of the requester. Example: user@example.com
</td></tr><tr><td>Description</td><td>Detailed issue description.
</td></tr><tr><td>Team</td><td>Infraon team name.
</td></tr><tr><td>Assignee Email</td><td>Email of the assignee.
</td></tr><tr><td>Urgency</td><td>Urgency level. Examples: High, Medium, Low
</td></tr><tr><td>Priority</td><td>Priority level. Examples: Critical, High, Medium, Low
</td></tr><tr><td>Impact</td><td>Impact category.
</td></tr><tr><td>Status</td><td>Workflow status.
</td></tr><tr><td>Severity</td><td>Severity level.
</td></tr><tr><td>Other Fields</td><td>Additional fields as JSON.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
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
}</pre>

### operation: Get Incident Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Ticket Id</td><td>Internal Infraon incident ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "incident": {},
    "options": {},
    "status": {},
    "transition_status": {},
    "stage_state_option_map": {}
}</pre>

### operation: Get All Incident Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Items Per Page</td><td>Number of incidents per page.
</td></tr><tr><td>Page Number</td><td>Page number to retrieve.
</td></tr><tr><td>Filters</td><td>Filter incidents.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "count": 0,
    "next": "",
    "previous": null,
    "results": [],
    "max_page_limit": 0
}</pre>

### operation: Update Incident
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Ticket Id</td><td>Infraon display ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "status": "",
    "id": "",
    "message": "",
    "msg": ""
}</pre>

### operation: Add Comment
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Ticket Id</td><td>Enter the Display ID of the ticket.
</td></tr><tr><td>Comment Text</td><td>Enter the comment text.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "status": "",
    "id": "",
    "message": "",
    "msg": "",
    "data": {
        "comment": "",
        "display_id": "",
        "ref_id": ""
    }
}</pre>

### operation: Delete Incident
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Ticket Id</td><td>Infraon display ID of the ticket to delete.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "status": "",
    "id": "",
    "message": "",
    "msg": ""
}</pre>

### operation: Add Attachment
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Ticket Id</td><td>Infraon display ID.
</td></tr></tbody></table>

#### Output
The output contains the following populated JSON schema:

<pre>{
    "status": "",
    "id": "",
    "message": "",
    "msg": ""
}</pre>
## Included playbooks
The `Sample - infraon - 1.0.1` playbook collection comes bundled with the Infraon ITSM connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR&trade; after importing the Infraon ITSM connector.

- Create Incident
- Get Incident Details
- Get All Incident Details
- Update Incident
- Add Comment
- Delete Incident
- Add Attachment

**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and move them to a different collection since the sample playbook collection gets deleted during connector upgrade and delete.
