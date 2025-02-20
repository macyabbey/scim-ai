package com.scim.ai.server.filter;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ScimFilterParser {
    private static final Pattern FILTER_PATTERN = Pattern.compile(
            "(?:not\\s+)?\\(?" +
                    "(\\w+(?:\\.\\w+)*(?:\\[(?:\\d+|[^\\]]+)\\])*)\\s+" +
                    "(eq|ne|co|sw|ew|gt|ge|lt|le|pr)\\s*" +
                    "(?:\"([^\"]+)\")?\\)?" +
                    "(?:\\s+(and|or)\\s+(.+))?",
            Pattern.CASE_INSENSITIVE);

    public static ScimFilter parse(String filterString) {
        if (filterString == null || filterString.trim().isEmpty()) {
            return null;
        }

        filterString = filterString.trim();

        // Handle NOT operator
        if (filterString.toLowerCase().startsWith("not")) {
            return new ScimFilter.NotFilter(
                    parse(filterString.substring(3).trim()));
        }

        Matcher matcher = FILTER_PATTERN.matcher(filterString);
        if (!matcher.find()) {
            throw new IllegalArgumentException("Invalid filter syntax: " + filterString);
        }

        String attribute = matcher.group(1);
        String operator = matcher.group(2).toLowerCase();
        String value = matcher.group(3);
        String logicalOp = matcher.group(4);
        String remainingFilter = matcher.group(5);

        ScimFilter filter = createAttributeFilter(attribute, operator, value);

        if (logicalOp != null && remainingFilter != null) {
            ScimFilter nextFilter = parse(remainingFilter);
            return logicalOp.toLowerCase().equals("and") ? new ScimFilter.AndFilter(filter, nextFilter)
                    : new ScimFilter.OrFilter(filter, nextFilter);
        }

        return filter;
    }

    private static ScimFilter createAttributeFilter(String attribute, String operator, String value) {
        return new ScimFilter.AttributeFilter(attribute, ScimFilter.Operator.fromString(operator), value);
    }
}