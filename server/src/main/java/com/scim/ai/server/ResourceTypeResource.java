package com.scim.ai.server;

import java.util.List;

import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

import jakarta.enterprise.context.RequestScoped;

import com.scim.ai.server.model.ResourceType;
import com.scim.ai.server.service.ResourceTypeService;

@Path("/scim/v2/ResourceTypes")
@RequestScoped
public class ResourceTypeResource {

  private final ResourceTypeService resourceTypeService;

  @Inject
  public ResourceTypeResource(ResourceTypeService resourceTypeService) {
    this.resourceTypeService = resourceTypeService;
  }

  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public List<ResourceType> getResourceTypes() {
    return resourceTypeService.getResourceTypes();
  }
}
