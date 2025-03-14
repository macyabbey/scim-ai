# Summary

SCIM AI enables you to rapidly build a SCIM 2.0 compliant server and instantly connect it to any of your application(s) or identity provider(s).

# How it works

SCIM AI is comprised of two main components:

- SCIM server
- SCIM AI agent

## SCIM server

This is the server which:

- Implements the SCIM protocol for N applications.
- Connect to your application(s) using agent assisted code
- Connect to your identity provider using agent assisted code

## SCIM AI agent

This is the AI agent which:

- Performs reasoning against existing database schemas to determine compatibility with SCIM protocol.
- Implements database connection from SCIM 2.0 server to provided database
- Tests and verifies the implementation works


# How to use SCIM AI

1. Chat with the SCIM AI agent to:

  a. Bootstrap your SCIM server
  b. Generate code to connect your SCIM server to your application(s)
  c. Generate and run test scenarios to ensure the SCIM server works as you expect.
  d. Connect your SCIM server to your preferred identity provider
  
# Relevant SCIM 2.0 specifications

- [Core Schema](https://datatracker.ietf.org/doc/html/rfc7643)
- [Protocol](https://datatracker.ietf.org/doc/html/rfc7644)
- [Definitions, Overview, Concepts, and Requirements](https://datatracker.ietf.org/doc/html/rfc7644)  


# TODOs

- POC
  + Create server agent
    + Give Server agent tools to create SCIM server code for user crud operations
      + Inputs:
        - Database connection string
        - List of database operations
          - Array of mappings from SCIM schema to database table(s) and columns
  + Create IDP connection agent
    + Give agent tool to create a SCIM 2.0 integration in Okta
    + Configure to hit ngrok endpoints
  + DONE - Minimal SCIM server thats runnable
    + DONE - Has place to put agent generated SCIM code for sql connection
    + Hardcodes domain to use for new scim connection
    + Use ngrok to give public domain to local scim server domain started up
  + Minimal UX (mb just the console is fine for now)

## Hardening

- Test `sql_read_schema` tool more thoroughly with more example Dbs from SQL Alchemy
  + Handle dialect variations, or don't, by translating to SQLAlchemy's intermediary representations upon reflection instead of being close to dialogs

