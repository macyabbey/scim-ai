package com.scim.ai.server.model;

import java.util.List;

public class ScimListResponse<T> {
    private List<T> Resources;
    private int totalResults;
    private int startIndex;
    private int itemsPerPage;
    private String[] schemas = { "urn:ietf:params:scim:api:messages:2.0:ListResponse" };

    public List<T> getResources() {
        return Resources;
    }

    public void setResources(List<T> resources) {
        this.Resources = resources;
    }

    public int getTotalResults() {
        return totalResults;
    }

    public void setTotalResults(int totalResults) {
        this.totalResults = totalResults;
    }

    public int getStartIndex() {
        return startIndex;
    }

    public void setStartIndex(int startIndex) {
        this.startIndex = startIndex;
    }

    public int getItemsPerPage() {
        return itemsPerPage;
    }

    public void setItemsPerPage(int itemsPerPage) {
        this.itemsPerPage = itemsPerPage;
    }

    public String[] getSchemas() {
        return schemas;
    }

    public void setSchemas(String[] schemas) {
        this.schemas = schemas;
    }
}