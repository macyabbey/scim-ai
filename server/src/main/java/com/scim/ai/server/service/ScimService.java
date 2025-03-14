package com.scim.ai.server.service;

import com.scim.ai.server.model.ScimUser;
import com.scim.ai.server.persistence.GroupPersistenceService;
import com.scim.ai.server.persistence.UserPersistenceService;
import com.scim.ai.server.model.ScimListResponse;
import com.scim.ai.server.model.ScimGroup;
import com.scim.ai.server.model.ScimBulkRequest;
import com.scim.ai.server.model.Meta;
import com.scim.ai.server.model.ScimPatchOperation;
import java.time.Instant;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

import com.scim.ai.server.service.PersistedListResult;

@ApplicationScoped
public class ScimService {

    UserPersistenceService userPersistenceService;
    GroupPersistenceService groupPersistenceService;

    @Inject
    public ScimService(
        UserPersistenceService userPersistenceService,
        GroupPersistenceService groupPersistenceService) {
        this.userPersistenceService = userPersistenceService;
        this.groupPersistenceService = groupPersistenceService;
    }

    public ScimUser createUser(ScimUser user) {
        user.setId(UUID.randomUUID().toString());

        // Set meta information
        Meta meta = new Meta();
        meta.setResourceType("User");
        meta.setCreated(Instant.now().toString());
        meta.setLastModified(Instant.now().toString());
        meta.setVersion("1");
        meta.setLocation("/scim/v2/Users/" + user.getId());
        user.setMeta(meta);

        userPersistenceService.createUser(user);
        return user;
    }

    public ScimUser getUser(String id) {
        return userPersistenceService.getUser(id);
    }

    public ScimListResponse<ScimUser> listUsers(String filter, int startIndex, int count) {
        PersistedListResult<ScimUser> result = userPersistenceService.listUsers(filter, startIndex, count);

        ScimListResponse<ScimUser> response = new ScimListResponse<>();
        response.setResources(result.results);
        response.setTotalResults(result.totalResultCount);
        response.setStartIndex(startIndex);
        response.setItemsPerPage(count);

        return response;
    }

    public ScimUser updateUser(String id, ScimUser user) {

        ScimUser existing = userPersistenceService.getUser(id);

        // Update meta information
        Meta meta = existing.getMeta();
        meta.setLastModified(Instant.now().toString());
        meta.setVersion(String.valueOf(Integer.parseInt(meta.getVersion()) + 1));
        user.setMeta(meta);

        userPersistenceService.replaceUser(id, user);
        return user;
    }

    public ScimUser patchUser(String id, ScimPatchOperation patch) {
        return userPersistenceService.patchUser(id, patch);
    }

    public boolean deleteUser(String id) {
        return userPersistenceService.deleteUser(id);
    }

    public ScimGroup createGroup(ScimGroup group) {
        group.setId(UUID.randomUUID().toString());

        Meta meta = new Meta();
        meta.setResourceType("Group");
        meta.setCreated(Instant.now().toString());
        meta.setLastModified(Instant.now().toString());
        meta.setVersion("1");
        meta.setLocation("/scim/v2/Groups/" + group.getId());
        group.setMeta(meta);

        return groupPersistenceService.createGroup(group);
    }

    public ScimGroup getGroup(String groupId) {
        return groupPersistenceService.getGroup(groupId);
    }

    public ScimGroup replaceGroup(String groupId, ScimGroup newGroup) {
        return groupPersistenceService.replaceGroup(groupId, newGroup);
    }

    public boolean deleteGroup(String groupId) {
        return groupPersistenceService.deleteGroup(groupId);
    }

    public ScimGroup patchGroup(String groupId, ScimPatchOperation patch) {
        return groupPersistenceService.patchGroup(groupId, patch);
    }

    public ScimListResponse<ScimGroup> listGroups(String filter, int startIndex, int count) {
        PersistedListResult<ScimGroup> result = groupPersistenceService.listGroups(filter, startIndex, count);

        ScimListResponse<ScimGroup> response = new ScimListResponse<>();
        response.setResources(result.results);
        response.setTotalResults(result.totalResultCount);
        response.setStartIndex(startIndex);
        response.setItemsPerPage(count);

        return response;
    }

    public Map<String, Object> processBulkOperations(ScimBulkRequest bulkRequest) {
        List<Map<String, Object>> results = new ArrayList<>();
        Map<String, String> bulkIdMap = new HashMap<>();

        for (ScimBulkRequest.BulkOperation op : bulkRequest.getOperations()) {
            try {
                Map<String, Object> result = new HashMap<>();
                result.put("bulkId", op.getBulkId());

                switch (op.getMethod().toUpperCase()) {
                    case "POST":
                        if (op.getPath().contains("/Users")) {
                            ScimUser user = createUser((ScimUser) op.getData());
                            bulkIdMap.put(op.getBulkId(), user.getId());
                            result.put("status", "201");
                        } else if (op.getPath().contains("/Groups")) {
                            ScimGroup group = createGroup((ScimGroup) op.getData());
                            bulkIdMap.put(op.getBulkId(), group.getId());
                            result.put("status", "201");
                        }
                        break;
                    // ... Handle other methods (PUT, PATCH, DELETE) ...
                    default:
                        break;
                }

                results.add(result);
            } catch (Exception e) {
                if (bulkRequest.getFailOnErrors() != null &&
                        results.size() >= bulkRequest.getFailOnErrors()) {
                    throw new RuntimeException("Bulk operation failed: " + e.getMessage());
                }
            }
        }

        Map<String, Object> response = new HashMap<>();
        response.put("schemas", new String[] { "urn:ietf:params:scim:api:messages:2.0:BulkResponse" });
        response.put("Operations", results);

        return response;
    }
}