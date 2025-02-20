package com.scim.ai.server.model;

/**
 * Represents the SCIM Meta attribute complex type as defined in RFC 7643.
 * This class contains metadata about SCIM resources.
 */
public class Meta {
    private String resourceType;
    private String created;
    private String lastModified;
    private String location;
    private String version;

    // Getters and Setters
    public String getResourceType() {
        return resourceType;
    }

    public void setResourceType(String resourceType) {
        this.resourceType = resourceType;
    }

    public String getCreated() {
        return created;
    }

    public void setCreated(String created) {
        this.created = created;
    }

    public String getLastModified() {
        return lastModified;
    }

    public void setLastModified(String lastModified) {
        this.lastModified = lastModified;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    @Override
    public String toString() {
        return "Meta{" +
                "resourceType='" + resourceType + '\'' +
                ", created='" + created + '\'' +
                ", lastModified='" + lastModified + '\'' +
                ", location='" + location + '\'' +
                ", version='" + version + '\'' +
                '}';
    }
} 