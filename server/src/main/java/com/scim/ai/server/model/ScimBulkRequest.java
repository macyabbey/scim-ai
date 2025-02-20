package com.scim.ai.server.model;

import java.util.List;

public class ScimBulkRequest {
    private String[] schemas = { "urn:ietf:params:scim:api:messages:2.0:BulkRequest" };
    private List<BulkOperation> Operations;
    private Integer failOnErrors;

    public static class BulkOperation {
        private String method; // POST, PUT, PATCH, DELETE
        private String bulkId; // Client-defined identifier
        private String path; // Resource path
        private Object data; // Resource data

        public String getMethod() {
            return method;
        }

        public void setMethod(String method) {
            this.method = method;
        }

        public String getBulkId() {
            return bulkId;
        }

        public void setBulkId(String bulkId) {
            this.bulkId = bulkId;
        }

        public String getPath() {
            return path;
        }

        public void setPath(String path) {
            this.path = path;
        }

        public Object getData() {
            return data;
        }

        public void setData(Object data) {
            this.data = data;
        }
    }

    public String[] getSchemas() {
        return schemas;
    }

    public void setSchemas(String[] schemas) {
        this.schemas = schemas;
    }

    public List<BulkOperation> getOperations() {
        return Operations;
    }

    public void setOperations(List<BulkOperation> operations) {
        this.Operations = operations;
    }

    public Integer getFailOnErrors() {
        return failOnErrors;
    }

    public void setFailOnErrors(Integer failOnErrors) {
        this.failOnErrors = failOnErrors;
    }
}