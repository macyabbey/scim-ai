package com.scim.ai.server;

import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

import jakarta.enterprise.context.RequestScoped;

import com.scim.ai.server.model.ServiceProviderConfig;
import com.scim.ai.server.service.ServiceProviderConfigService;

@Path("/scim/v2/ServiceProviderConfig")
@RequestScoped
public class ServiceConfigResource {

  private final ServiceProviderConfigService serviceProviderConfigService;

  @Inject
  public ServiceConfigResource(ServiceProviderConfigService serviceProviderConfigService) {
    this.serviceProviderConfigService = serviceProviderConfigService;
  }

  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public ServiceProviderConfig getServiceProviderConfig() {
    return serviceProviderConfigService.getConfig();
  }
}
