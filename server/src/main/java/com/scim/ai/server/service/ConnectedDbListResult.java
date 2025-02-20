package com.scim.ai.server.service;

import java.util.List;

public class ConnectedDbListResult<T> {
  public List<T> results;
  public int totalResultCount;

  public ConnectedDbListResult(List<T> results, int totalResultCount) {
    this.results = results;
    this.totalResultCount = totalResultCount;
  }
}
