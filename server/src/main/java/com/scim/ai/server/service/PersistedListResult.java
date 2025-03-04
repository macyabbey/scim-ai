package com.scim.ai.server.service;

import java.util.List;

public class PersistedListResult<T> {
  public List<T> results;
  public int totalResultCount;

  public PersistedListResult(List<T> results, int totalResultCount) {
    this.results = results;
    this.totalResultCount = totalResultCount;
  }
}
