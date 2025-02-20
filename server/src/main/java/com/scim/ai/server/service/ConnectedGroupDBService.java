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
import main.java.com.scim.ai.server.service.ConnectedDbListResult;

@Dependent
public class ConnectedGroupDBService {

  @Inject
  @Named("db")
  private DataSource ds;

  private final Map<String, ScimGroup> groups = new ConcurrentHashMap<>();

  public ScimGroup createGroup(ScimGroup group) {
    groups.put(group.getId(), group);
    return group;
  }

  public ScimGroup getGroup(String id) {
    return groups.get(id);
  }

  public ConnectedDbListResult listGroups(String filter, int startIndex, int count) {
    List<ScimGroup> filteredGroups = groups.values().stream()
        // .filter(group -> applyFilter(group, filter))
        .collect(Collectors.toList());

    int totalResults = filteredGroups.size();

    // Apply pagination
    List<ScimGroup> pagedGroups = filteredGroups.stream()
        .skip(startIndex - 1)
        .limit(count)
        .collect(Collectors.toList());

    return new ConnectedDbListResult<ScimGroup>(pagedGroups, totalResults);
  }

  public boolean deleteGroup(String id) {
    return groups.remove(id) != null;
  }

  public ScimGroup patchGroup(String id, ScimPatchOperation patch) {
    ScimGroup group = groups.get(id);
    if (group == null) {
      return null;
    }

    for (ScimPatchOperation.PatchOperation op : patch.getOperations()) {
      applyPatchOperation(group, op);
    }

    // Update version
    Meta meta = group.getMeta();
    meta.setLastModified(Instant.now().toString());
    meta.setVersion(String.valueOf(Integer.parseInt(meta.getVersion()) + 1));

    return group;
  }

  public ScimGroup replaceGroup(String id, ScimGroup group) {
    groups.put(id, group);
    return group;
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
