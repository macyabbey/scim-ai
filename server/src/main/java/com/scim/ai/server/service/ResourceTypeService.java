package com.scim.ai.server.service;

import jakarta.enterprise.context.ApplicationScoped;

import com.scim.ai.server.model.ResourceType;

import java.util.List;

@ApplicationScoped
public class ResourceTypeService {
  private final String type;

  public ResourceTypeService() {
    this.type = "User";
  }

  public List<ResourceType> getResourceTypes() {
    return List.of(

    );
  }
}
