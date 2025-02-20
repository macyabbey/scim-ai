package com.scim.ai.server.filter;

public interface ScimFilter {
    enum Operator {
        EQUALS("eq"),
        NOT_EQUALS("ne"),
        CONTAINS("co"),
        STARTS_WITH("sw"),
        ENDS_WITH("ew"),
        GREATER_THAN("gt"),
        GREATER_EQUALS("ge"),
        LESS_THAN("lt"),
        LESS_EQUALS("le"),
        PRESENT("pr");

        private final String value;

        Operator(String value) {
            this.value = value;
        }

        public static Operator fromString(String value) {
            for (Operator op : values()) {
                if (op.value.equalsIgnoreCase(value)) {
                    return op;
                }
            }
            throw new IllegalArgumentException("Unknown operator: " + value);
        }
    }

    class AttributeFilter implements ScimFilter {
        private final String attribute;
        private final Operator operator;
        private final String value;

        public AttributeFilter(String attribute, Operator operator, String value) {
            this.attribute = attribute;
            this.operator = operator;
            this.value = value;
        }

        public String getAttribute() {
            return attribute;
        }

        public Operator getOperator() {
            return operator;
        }

        public String getValue() {
            return value;
        }
    }

    class AndFilter implements ScimFilter {
        private final ScimFilter left;
        private final ScimFilter right;

        public AndFilter(ScimFilter left, ScimFilter right) {
            this.left = left;
            this.right = right;
        }

        public ScimFilter getLeft() {
            return left;
        }

        public ScimFilter getRight() {
            return right;
        }
    }

    class OrFilter implements ScimFilter {
        private final ScimFilter left;
        private final ScimFilter right;

        public OrFilter(ScimFilter left, ScimFilter right) {
            this.left = left;
            this.right = right;
        }

        public ScimFilter getLeft() {
            return left;
        }

        public ScimFilter getRight() {
            return right;
        }
    }

    class NotFilter implements ScimFilter {
        private final ScimFilter filter;

        public NotFilter(ScimFilter filter) {
            this.filter = filter;
        }

        public ScimFilter getFilter() {
            return filter;
        }
    }
}