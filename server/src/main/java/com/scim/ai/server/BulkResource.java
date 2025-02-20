package com.scim.ai.server;

import java.util.Map;

import org.eclipse.microprofile.openapi.annotations.parameters.RequestBody;

import com.scim.ai.server.model.ScimBulkRequest;
import com.scim.ai.server.service.ScimService;

import jakarta.enterprise.context.RequestScoped;

import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.core.MediaType;

@Path("/scim/v2/Bulk")
@RequestScoped
public class BulkResource {

  private final ScimService scimService;

  @Inject
  public BulkResource(ScimService scimService) {
    this.scimService = scimService;
  }

  @POST
  @Produces(MediaType.APPLICATION_JSON)
  @Consumes(MediaType.APPLICATION_JSON)
  public Map<String, Object> doBulkOperation(
      @RequestBody(description = "Bulk operation request", required = true) ScimBulkRequest bulkRequest) {
    return scimService.processBulkOperations(bulkRequest);
  }
}
