package com.scim.ai.server.model;

import java.util.List;

public class ServiceProviderConfig {
    private final String[] schemas = { "urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig" };
    private final String documentationUri = "http://example.com/help/scim.html";
    private final Patch patch = new Patch(true);
    private final Bulk bulk = new Bulk(true, 1000, 1000);
    private final Filter filter = new Filter(true, 200);
    private final ChangePassword changePassword = new ChangePassword(true);
    private final Sort sort = new Sort(true);
    private final Etag etag = new Etag(true);
    private final AuthenticationScheme[] authenticationSchemes = {
            new AuthenticationScheme(
                    "Bearer Token",
                    "Bearer",
                    "OAuth2 Bearer Token",
                    "http://example.com/help/oauth.html",
                    "oauth2")
    };

    public static class Patch {
        private final boolean supported;

        public Patch(boolean supported) {
            this.supported = supported;
        }

        public boolean isSupported() {
            return supported;
        }
    }

    public static class Bulk {
        private final boolean supported;
        private final int maxOperations;
        private final int maxPayloadSize;

        public Bulk(boolean supported, int maxOperations, int maxPayloadSize) {
            this.supported = supported;
            this.maxOperations = maxOperations;
            this.maxPayloadSize = maxPayloadSize;
        }

        public boolean isSupported() {
            return supported;
        }

        public int getMaxOperations() {
            return maxOperations;
        }

        public int getMaxPayloadSize() {
            return maxPayloadSize;
        }
    }

    public static class Filter {
        private final boolean supported;
        private final int maxResults;

        public Filter(boolean supported, int maxResults) {
            this.supported = supported;
            this.maxResults = maxResults;
        }

        public boolean isSupported() {
            return supported;
        }

        public int getMaxResults() {
            return maxResults;
        }
    }

    public static class ChangePassword {
        private final boolean supported;

        public ChangePassword(boolean supported) {
            this.supported = supported;
        }

        public boolean isSupported() {
            return supported;
        }
    }

    public static class Sort {
        private final boolean supported;

        public Sort(boolean supported) {
            this.supported = supported;
        }

        public boolean isSupported() {
            return supported;
        }
    }

    public static class Etag {
        private final boolean supported;

        public Etag(boolean supported) {
            this.supported = supported;
        }

        public boolean isSupported() {
            return supported;
        }
    }

    public static class AuthenticationScheme {
        private final String name;
        private final String description;
        private final String specUri;
        private final String documentationUri;
        private final String type;

        public AuthenticationScheme(String name, String description, String specUri,
                String documentationUri, String type) {
            this.name = name;
            this.description = description;
            this.specUri = specUri;
            this.documentationUri = documentationUri;
            this.type = type;
        }

        public String getName() {
            return name;
        }

        public String getDescription() {
            return description;
        }

        public String getSpecUri() {
            return specUri;
        }

        public String getDocumentationUri() {
            return documentationUri;
        }

        public String getType() {
            return type;
        }
    }

    // Getters
    public String[] getSchemas() {
        return schemas;
    }

    public String getDocumentationUri() {
        return documentationUri;
    }

    public Patch getPatch() {
        return patch;
    }

    public Bulk getBulk() {
        return bulk;
    }

    public Filter getFilter() {
        return filter;
    }

    public ChangePassword getChangePassword() {
        return changePassword;
    }

    public Sort getSort() {
        return sort;
    }

    public Etag getEtag() {
        return etag;
    }

    public AuthenticationScheme[] getAuthenticationSchemes() {
        return authenticationSchemes;
    }
}