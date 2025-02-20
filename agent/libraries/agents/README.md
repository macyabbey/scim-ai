## SCIM agent flows

```mermaid
flow
  TASK-DISCOVERY --"initial SCIM AI setup"-->  "INITIAL-SETUP"
  TASK-DISCOVERY --"new server"-->             "NEW-SERVER"
  TASK-DISCOVERY --"edit server"-->            "EDIT-SERVER"
  TASK-DISCOVERY --"test server"-->            "TEST-SERVER"
  TASK-DISCOVERY --"troubleshoot server"-->    "TROUBLESHOOT-SERVER"
```

### NEW-SERVER

```mermaid
flow
  NEED-DOMAIN           --"got domain"-->               NEED-CONNECTION-TYPE
  NEED-CONNECTION-TYPE  --"connection-type=sql"-->      SETUP-SQL-CONNECTION
  NEED-CONNECTION-TYPE  --"connection-type=nosql"-->    SETUP-NOSQL-CONNECTION
  NEED-CONNECTION-TYPE  --"connection-type=file"-->     SETUP-FILE-CONNECTION
  NEED-CONNECTION-TYPE  --"connection-type=rest-api"--> SETUP-REST-API-CONNECTION
  NEED-CONNECTION-TYPE  --"connection-type=soap-api"--> SETUP-SOAP-API-CONNECTION
```

### SETUP-SQL-CONNECTION

```mermaid
SETUP-DATABASE-CONNECTION              --"got valid connection string"-->              FIND_CORE_SCIM_OBJECTS
FIND-CORE-SCIM-OBJECTS                 --"feedback on core scim objects"-->            MAP_CORE_OBJECT_ATTRIBUTES
MAP-CORE-OBJECT-ATTRIBUTES             --"feedback on core object mappings"-->         FIND_RELATED_OBJECTS
FIND_RELATED_OBJECTS                   --"feedback on related objects"-->              DETERMINE_CORE_SCIM_OBJECT_OPERATIONS
DETERMINE_CORE_SCIM_OBJECT_OPERATIONS  --"feedback on core SCIM object operations"-->  GENERATE_OPERATION_CODE
GENERATE_OPERATION_CODE                --"compile operation code"-->                   TEST-SERVER
```

### TEST-SERVER

```mermaid
```