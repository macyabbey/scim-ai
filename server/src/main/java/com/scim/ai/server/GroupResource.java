package com.scim.ai.server;

import jakarta.inject.Inject;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.DefaultValue;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import jakarta.enterprise.context.RequestScoped;

import org.eclipse.microprofile.openapi.annotations.enums.SchemaType;
import org.eclipse.microprofile.openapi.annotations.media.Content;
import org.eclipse.microprofile.openapi.annotations.media.Schema;
import org.eclipse.microprofile.openapi.annotations.parameters.RequestBody;

import com.scim.ai.server.model.ScimListResponse;
import com.scim.ai.server.model.ScimGroup;
import com.scim.ai.server.service.ScimService;

@Path("/scim/v2/Groups")
@RequestScoped
public class GroupResource {

  private final ScimService scimService;

  @Inject
  public GroupResource(ScimService scimService) {
    this.scimService = scimService;
  }

  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public ScimListResponse<ScimGroup> listGroups(
      @QueryParam("filter") String filter,
      @DefaultValue("1") @QueryParam("startIndex") int startIndex,
      @DefaultValue("100") @QueryParam("count") int count,
      @QueryParam("sortBy") String sortBy,
      @QueryParam("sortOrder") String sortOrder) {
    ScimListResponse<ScimGroup> response = scimService.listGroups(filter, startIndex, count);
    return response;
  }

  @GET
  @Path("/{id}")
  @Produces(MediaType.APPLICATION_JSON)
  public ScimGroup getGroup(
      @PathParam("id") String id) {
    return scimService.getGroup(id);
  }

  @POST
  @Produces(MediaType.APPLICATION_JSON)
  public ScimGroup creatGroup(
      @RequestBody(description = "Group to create", required = true, content = @Content(mediaType = "application/json", schema = @Schema(implementation = ScimGroup.class, type = SchemaType.OBJECT))) ScimGroup group) {
    ScimGroup created = scimService.createGroup(group);
    return created;
  }

  @PUT
  @Path("/{id}")
  @Produces(MediaType.APPLICATION_JSON)
  public ScimGroup updateGroup(
      @PathParam("id") String id,
      @RequestBody(description = "Group to create", required = true, content = @Content(mediaType = "application/json", schema = @Schema(implementation = ScimGroup.class, type = SchemaType.OBJECT))) ScimGroup group) {
    ScimGroup updated = scimService.replaceGroup(id, group);
    return updated;
  }

  @DELETE
  @Path("/{id}")
  @Produces(MediaType.APPLICATION_JSON)
  public Response deleteGroup(
      @PathParam("id") String id) {
    if (scimService.deleteGroup(id)) {
      return Response.status(Response.Status.NO_CONTENT).build();
    } else {
      return Response.status(Response.Status.NOT_FOUND).build();
    }
  }
}