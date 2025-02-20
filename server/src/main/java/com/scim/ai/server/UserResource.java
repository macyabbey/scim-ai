package com.scim.ai.server;

import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.PATCH;
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
import com.scim.ai.server.model.ScimPatchOperation;
import com.scim.ai.server.model.ScimUser;
import com.scim.ai.server.service.ScimService;

@Path("/scim/v2/Users")
@RequestScoped
public class UserResource {

  private final ScimService scimService;

  @Inject
  public UserResource(ScimService scimService) {
    this.scimService = scimService;
  }

  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public ScimListResponse<ScimUser> listUsers(
      @QueryParam("filter") String filter,
      @DefaultValue("1") @QueryParam("startIndex") int startIndex,
      @DefaultValue("100") @QueryParam("count") int count,
      @QueryParam("sortBy") String sortBy,
      @QueryParam("sortOrder") String sortOrder) {
    ScimListResponse<ScimUser> response = scimService.listUsers(filter, startIndex, count);
    return response;
  }

  @GET
  @Path("/{id}")
  @Produces(MediaType.APPLICATION_JSON)
  public ScimUser getUser(
      @PathParam("id") String id) {
    return scimService.getUser(id);
  }

  @POST
  @Produces(MediaType.APPLICATION_JSON)
  public ScimUser createUser(
      @RequestBody(description = "User to create", required = true, content = @Content(mediaType = "application/json", schema = @Schema(implementation = ScimUser.class, type = SchemaType.OBJECT))) ScimUser user) {
    ScimUser created = scimService.createUser(user);
    return created;
  }

  @PUT
  @Path("/{id}")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  public ScimUser replaceUser(
      @PathParam("id") String id,
      @RequestBody(description = "User to replace", required = true, content = @Content(mediaType = "application/json", schema = @Schema(implementation = ScimUser.class, type = SchemaType.OBJECT))) ScimUser user) {
    ScimUser updated = scimService.updateUser(id, user);
    return updated;
  }

  @DELETE
  @Path("/{id}")
  @Produces(MediaType.APPLICATION_JSON)
  public Response deleteUser(
      @PathParam("id") String id) {
    if (scimService.deleteUser(id)) {
      return Response.status(Response.Status.NO_CONTENT).build();
    } else {
      return Response.status(Response.Status.NOT_FOUND).build();
    }
  }

  @PATCH
  @Path("/{id}")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  public ScimUser patchUser(
      @PathParam("id") String id,
      @RequestBody(description = "User patch operation", required = true, content = @Content(mediaType = "application/json", schema = @Schema(implementation = ScimUser.class, type = SchemaType.OBJECT))) ScimPatchOperation operation) {
    ScimUser updated = scimService.patchUser(id, operation);
    return updated;
  }
}