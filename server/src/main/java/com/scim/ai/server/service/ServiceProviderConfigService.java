package com.scim.ai.server.service;

import com.scim.ai.server.model.ServiceProviderConfig;

import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class ServiceProviderConfigService {
    private final ServiceProviderConfig config;

    public ServiceProviderConfigService() {
        this.config = new ServiceProviderConfig();
    }

    public ServiceProviderConfig getConfig() {
        return config;
    }
}