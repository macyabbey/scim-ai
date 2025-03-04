package com.scim.ai.server.service;

import com.scim.ai.server.model.ScimUser;
import com.scim.ai.server.model.ScimPatchOperation;

public interface UserPersistenceService {

  ScimUser createUser(ScimUser user);

  ScimUser getUser(String id);

  PersistedListResult<ScimUser> listUsers(String filter, int startIndex, int count);

  boolean deleteUser(String id);

  ScimUser patchUser(String id, ScimPatchOperation patch);

  ScimUser replaceUser(String id, ScimUser user);
}
