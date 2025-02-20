package com.scim.ai.server;

import java.util.Map;

import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

import jakarta.enterprise.context.RequestScoped;

import com.scim.ai.server.service.SchemaService;

@Path("/scim/v2/Schemas")
@RequestScoped
public class SchemaResource {

  private final SchemaService schemaService;

  @Inject
  public SchemaResource(SchemaService schemaService) {
    this.schemaService = schemaService;
  }

  @GET
  @Path("/Users")
  @Produces(MediaType.APPLICATION_JSON)
  public Map<String, Object> getUserSchema() {
    return schemaService.getUserSchema();
  }

  @GET
  @Path("/Groups")
  @Produces(MediaType.APPLICATION_JSON)
  public Map<String, Object> getGroupSchema() {
    return schemaService.getGroupSchema();
  }
}
