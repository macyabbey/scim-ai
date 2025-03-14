package com.scim.ai.server.persistence;

import com.scim.ai.server.model.ScimGroup;
import com.scim.ai.server.model.ScimPatchOperation;
import com.scim.ai.server.service.PersistedListResult;

public interface GroupPersistenceService {

  ScimGroup createGroup(ScimGroup user);

  ScimGroup getGroup(String id);

  PersistedListResult<ScimGroup> listGroups(String filter, int startIndex, int count);

  boolean deleteGroup(String id);

  ScimGroup patchGroup(String id, ScimPatchOperation patch);

  ScimGroup replaceGroup(String id, ScimGroup group);
}
