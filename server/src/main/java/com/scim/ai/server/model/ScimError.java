package com.scim.ai.server.model;

public class ScimError {
    private String status;
    private String detail;
    private String schemas = "urn:ietf:params:scim:api:messages:2.0:Error";

    public ScimError(String status, String detail) {
        this.status = status;
        this.detail = detail;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getDetail() {
        return detail;
    }

    public void setDetail(String detail) {
        this.detail = detail;
    }

    public String getSchemas() {
        return schemas;
    }

    public void setSchemas(String schemas) {
        this.schemas = schemas;
    }
}