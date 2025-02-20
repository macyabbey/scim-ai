package com.scim.ai.server.service;

import java.util.Map;
import java.util.HashMap;

import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class SchemaService {
    private final Map<String, Object> userSchema;
    private final Map<String, Object> groupSchema;

    public SchemaService() {
        userSchema = createUserSchema();
        groupSchema = createGroupSchema();
    }

    public Map<String, Object> getUserSchema() {
        return userSchema;
    }

    public Map<String, Object> getGroupSchema() {
        return groupSchema;
    }

    private Map<String, Object> createUserSchema() {
        Map<String, Object> schema = new HashMap<>();
        schema.put("id", "urn:ietf:params:scim:schemas:core:2.0:User");
        schema.put("name", "User");
        schema.put("description", "User Account");

        // Add attributes definition here
        // This is a simplified version - you should add more attributes
        Map<String, Object> attributes = new HashMap<>();
        attributes.put("userName", Map.of(
                "type", "string",
                "required", true,
                "caseExact", false,
                "mutability", "readWrite"));

        schema.put("attributes", attributes);
        return schema;
    }

    private Map<String, Object> createGroupSchema() {
        Map<String, Object> schema = new HashMap<>();
        schema.put("id", "urn:ietf:params:scim:schemas:core:2.0:Group");
        schema.put("name", "Group");
        schema.put("description", "Group");

        // Add attributes definition here
        Map<String, Object> attributes = new HashMap<>();
        attributes.put("displayName", Map.of(
                "type", "string",
                "required", true,
                "caseExact", false,
                "mutability", "readWrite"));

        schema.put("attributes", attributes);
        return schema;
    }
}