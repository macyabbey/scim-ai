package com.scim.ai.server.service;

import javax.sql.DataSource;

import com.scim.ai.server.model.ScimUser;
import com.scim.ai.server.model.ScimListResponse;
import com.scim.ai.server.model.ScimGroup;
import com.scim.ai.server.model.ScimGroup.Member;
import com.scim.ai.server.model.ScimBulkRequest;
import com.scim.ai.server.model.Meta;
import com.scim.ai.server.model.ScimPatchOperation;
import com.scim.ai.server.model.ScimPatchOperation.PatchOperation;

import java.lang.reflect.Field;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

import jakarta.enterprise.context.Dependent;
import jakarta.inject.Inject;
import jakarta.inject.Named;

@Dependent
public class ConnectedUserDBService {

  @Inject
  @Named("db")
  private DataSource ds;

  private final Map<String, ScimUser> users = new ConcurrentHashMap<>();

  public ScimUser createUser(ScimUser user) {
    users.put(user.getId(), user);
    return user;
  }

  public ScimUser getUser(String id) {
    return users.get(id);
  }

  public ConnectedDbListResult listUsers(String filter, int startIndex, int count) {
    List<ScimUser> filteredUsers = users.values().stream()
        .filter(user -> applyFilter(user, filter))
        .collect(Collectors.toList());

    int totalResults = filteredUsers.size();

    // Apply pagination
    List<ScimUser> pagedUsers = filteredUsers.stream()
        .skip(startIndex - 1)
        .limit(count)
        .collect(Collectors.toList());

    return new ConnectedDbListResult(pagedUsers, totalResults);
  }

  public boolean deleteUser(String id) {
    return users.remove(id) != null;
  }

  public ScimUser patchUser(String id, ScimPatchOperation patch) {
    ScimUser user = users.get(id);
    if (user == null) {
      return null;
    }

    for (ScimPatchOperation.PatchOperation op : patch.getOperations()) {
      applyPatchOperation(user, op);
    }

    // Update version
    Meta meta = user.getMeta();
    meta.setLastModified(Instant.now().toString());
    meta.setVersion(String.valueOf(Integer.parseInt(meta.getVersion()) + 1));

    return user;
  }

  public ScimUser replaceUser(String id, ScimUser user) {
    users.put(id, user);
    return user;
  }

  private void applyPatchOperation(ScimUser user, ScimPatchOperation.PatchOperation op) {
    try {
      String[] pathParts = op.getPath().split("\\.");
      Object target = user;

      // Navigate to the target object
      for (int i = 0; i < pathParts.length - 1; i++) {
        Field field = target.getClass().getDeclaredField(pathParts[i]);
        field.setAccessible(true);
        target = field.get(target);
      }

      // Get the target field
      Field field = target.getClass().getDeclaredField(pathParts[pathParts.length - 1]);
      field.setAccessible(true);

      switch (op.getOp().toLowerCase()) {
        case "add":
        case "replace":
          field.set(target, op.getValue());
          break;
        case "remove":
          field.set(target, null);
          break;
        default:
          break;
      }
    } catch (Exception e) {
      throw new RuntimeException("Failed to apply patch operation: " + e.getMessage());
    }
  }
}
