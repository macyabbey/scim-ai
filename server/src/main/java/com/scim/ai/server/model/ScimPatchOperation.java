package com.scim.ai.server.model;

import java.util.List;

public class ScimPatchOperation {
    private String[] schemas = { "urn:ietf:params:scim:api:messages:2.0:PatchOp" };
    private List<PatchOperation> Operations;

    public static class PatchOperation {
        private String op; // add, remove, replace
        private String path; // attribute path
        private Object value; // new value

        public String getOp() {
            return op;
        }

        public void setOp(String op) {
            this.op = op;
        }

        public String getPath() {
            return path;
        }

        public void setPath(String path) {
            this.path = path;
        }

        public Object getValue() {
            return value;
        }

        public void setValue(Object value) {
            this.value = value;
        }
    }

    public String[] getSchemas() {
        return schemas;
    }

    public void setSchemas(String[] schemas) {
        this.schemas = schemas;
    }

    public List<PatchOperation> getOperations() {
        return Operations;
    }

    public void setOperations(List<PatchOperation> operations) {
        this.Operations = operations;
    }
}