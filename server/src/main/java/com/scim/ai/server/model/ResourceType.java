package com.scim.ai.server.model;

import java.util.List;

public class ResourceType {

  private String id;
  private String name;
  private String description;
  private String endpoint;
  private List<String> schemas;

  public ResourceType() {
  }

  public ResourceType(String id, String name, String description, String endpoint, List<String> schemas) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.endpoint = endpoint;
    this.schemas = schemas;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public String getEndpoint() {
    return endpoint;
  }

  public void setEndpoint(String endpoint) {
    this.endpoint = endpoint;
  }

  public List<String> getSchemas() {
    return schemas;
  }

  public void setSchemas(List<String> schemas) {
    this.schemas = schemas;
  }
}