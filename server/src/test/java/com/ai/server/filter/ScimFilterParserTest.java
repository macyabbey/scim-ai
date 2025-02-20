package com.scim.ai.server.filter;

import org.junit.jupiter.api.Test;

import com.scim.ai.server.filter.ScimFilter;
import com.scim.ai.server.filter.ScimFilterParser;

import static org.junit.jupiter.api.Assertions.*;

public class ScimFilterParserTest {
    @Test
    void testSimpleEqualsFilter() {
        ScimFilter filter = ScimFilterParser.parse("userName eq \"john.doe\"");
        assertTrue(filter instanceof ScimFilter.AttributeFilter);
        ScimFilter.AttributeFilter af = (ScimFilter.AttributeFilter) filter;
        assertEquals("userName", af.getAttribute());
        assertEquals(ScimFilter.Operator.EQUALS, af.getOperator());
        assertEquals("john.doe", af.getValue());
    }

    @Test
    void testComplexAndFilter() {
        ScimFilter filter = ScimFilterParser.parse("userName eq \"john\" and active eq \"true\"");
        assertTrue(filter instanceof ScimFilter.AndFilter);
        ScimFilter.AndFilter and = (ScimFilter.AndFilter) filter;

        assertTrue(and.getLeft() instanceof ScimFilter.AttributeFilter);
        assertTrue(and.getRight() instanceof ScimFilter.AttributeFilter);

        ScimFilter.AttributeFilter left = (ScimFilter.AttributeFilter) and.getLeft();
        assertEquals("userName", left.getAttribute());
        assertEquals(ScimFilter.Operator.EQUALS, left.getOperator());
        assertEquals("john", left.getValue());
    }

    @Test
    void testNotFilter() {
        ScimFilter filter = ScimFilterParser.parse("not (active eq \"false\")");
        assertTrue(filter instanceof ScimFilter.NotFilter);
        ScimFilter.NotFilter not = (ScimFilter.NotFilter) filter;

        assertTrue(not.getFilter() instanceof ScimFilter.AttributeFilter);
        ScimFilter.AttributeFilter af = (ScimFilter.AttributeFilter) not.getFilter();
        assertEquals("active", af.getAttribute());
        assertEquals("false", af.getValue());
    }

    @Test
    void testNestedAttributeFilter() {
        ScimFilter filter = ScimFilterParser.parse("name.givenName co \"john\"");
        assertTrue(filter instanceof ScimFilter.AttributeFilter);
        ScimFilter.AttributeFilter af = (ScimFilter.AttributeFilter) filter;
        assertEquals("name.givenName", af.getAttribute());
        assertEquals(ScimFilter.Operator.CONTAINS, af.getOperator());
    }
}