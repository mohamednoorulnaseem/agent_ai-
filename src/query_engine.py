"""
Advanced query filtering and sorting for API endpoints.

Supports complex filtering, pagination, sorting, and search.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import re


@dataclass
class FilterCondition:
    """Single filter condition."""
    field: str
    operator: str  # "eq", "ne", "gt", "gte", "lt", "lte", "contains", "in", "regex"
    value: Any


@dataclass
class QueryFilter:
    """Advanced query filter."""
    conditions: List[FilterCondition]
    logical_operator: str = "and"  # "and" or "or"
    sort_by: Optional[str] = None
    sort_order: str = "asc"  # "asc" or "desc"
    limit: int = 100
    offset: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "conditions": [
                {
                    "field": c.field,
                    "operator": c.operator,
                    "value": c.value,
                }
                for c in self.conditions
            ],
            "logical_operator": self.logical_operator,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
            "limit": self.limit,
            "offset": self.offset,
        }


class QueryFilterBuilder:
    """Build complex query filters."""

    def __init__(self):
        """Initialize filter builder."""
        self.conditions: List[FilterCondition] = []
        self.logical_operator = "and"
        self.sort_by = None
        self.sort_order = "asc"
        self.limit = 100
        self.offset = 0

    def eq(self, field: str, value: Any) -> "QueryFilterBuilder":
        """Add equality condition."""
        self.conditions.append(FilterCondition(field, "eq", value))
        return self

    def ne(self, field: str, value: Any) -> "QueryFilterBuilder":
        """Add not-equal condition."""
        self.conditions.append(FilterCondition(field, "ne", value))
        return self

    def gt(self, field: str, value: Any) -> "QueryFilterBuilder":
        """Add greater-than condition."""
        self.conditions.append(FilterCondition(field, "gt", value))
        return self

    def gte(self, field: str, value: Any) -> "QueryFilterBuilder":
        """Add greater-than-or-equal condition."""
        self.conditions.append(FilterCondition(field, "gte", value))
        return self

    def lt(self, field: str, value: Any) -> "QueryFilterBuilder":
        """Add less-than condition."""
        self.conditions.append(FilterCondition(field, "lt", value))
        return self

    def lte(self, field: str, value: Any) -> "QueryFilterBuilder":
        """Add less-than-or-equal condition."""
        self.conditions.append(FilterCondition(field, "lte", value))
        return self

    def contains(self, field: str, value: str) -> "QueryFilterBuilder":
        """Add contains condition."""
        self.conditions.append(FilterCondition(field, "contains", value))
        return self

    def in_list(self, field: str, values: List[Any]) -> "QueryFilterBuilder":
        """Add in-list condition."""
        self.conditions.append(FilterCondition(field, "in", values))
        return self

    def regex(self, field: str, pattern: str) -> "QueryFilterBuilder":
        """Add regex condition."""
        self.conditions.append(FilterCondition(field, "regex", pattern))
        return self

    def and_operator(self) -> "QueryFilterBuilder":
        """Use AND for combining conditions."""
        self.logical_operator = "and"
        return self

    def or_operator(self) -> "QueryFilterBuilder":
        """Use OR for combining conditions."""
        self.logical_operator = "or"
        return self

    def sort(self, field: str, order: str = "asc") -> "QueryFilterBuilder":
        """Add sorting."""
        self.sort_by = field
        self.sort_order = order
        return self

    def paginate(self, limit: int, offset: int = 0) -> "QueryFilterBuilder":
        """Add pagination."""
        self.limit = limit
        self.offset = offset
        return self

    def build(self) -> QueryFilter:
        """Build query filter."""
        return QueryFilter(
            conditions=self.conditions,
            logical_operator=self.logical_operator,
            sort_by=self.sort_by,
            sort_order=self.sort_order,
            limit=self.limit,
            offset=self.offset,
        )


class QueryExecutor:
    """Execute query filters on data."""

    @staticmethod
    def apply_filter(
        data: List[Dict[str, Any]],
        query_filter: QueryFilter
    ) -> List[Dict[str, Any]]:
        """Apply filter to data."""
        result = data

        # Apply conditions
        if query_filter.conditions:
            result = QueryExecutor._apply_conditions(
                result,
                query_filter.conditions,
                query_filter.logical_operator
            )

        # Apply sorting
        if query_filter.sort_by:
            reverse = query_filter.sort_order == "desc"
            result = sorted(
                result,
                key=lambda x: x.get(query_filter.sort_by, ""),
                reverse=reverse
            )

        # Apply pagination
        start = query_filter.offset
        end = start + query_filter.limit
        result = result[start:end]

        return result

    @staticmethod
    def _apply_conditions(
        data: List[Dict[str, Any]],
        conditions: List[FilterCondition],
        logical_operator: str
    ) -> List[Dict[str, Any]]:
        """Apply filter conditions."""
        result = []

        for item in data:
            if logical_operator == "and":
                # All conditions must match
                if all(
                    QueryExecutor._matches_condition(item, cond)
                    for cond in conditions
                ):
                    result.append(item)
            else:  # "or"
                # At least one condition must match
                if any(
                    QueryExecutor._matches_condition(item, cond)
                    for cond in conditions
                ):
                    result.append(item)

        return result

    @staticmethod
    def _matches_condition(item: Dict[str, Any], condition: FilterCondition) -> bool:
        """Check if item matches condition."""
        value = item.get(condition.field)

        if condition.operator == "eq":
            return value == condition.value
        elif condition.operator == "ne":
            return value != condition.value
        elif condition.operator == "gt":
            return value > condition.value
        elif condition.operator == "gte":
            return value >= condition.value
        elif condition.operator == "lt":
            return value < condition.value
        elif condition.operator == "lte":
            return value <= condition.value
        elif condition.operator == "contains":
            return condition.value in str(value)
        elif condition.operator == "in":
            return value in condition.value
        elif condition.operator == "regex":
            return bool(re.match(condition.value, str(value)))

        return False


class SearchEngine:
    """Full-text search across multiple fields."""

    def __init__(self, searchable_fields: List[str] = None):
        """
        Initialize search engine.

        Args:
            searchable_fields: Fields to search in
        """
        self.searchable_fields = searchable_fields or []

    def search(
        self,
        data: List[Dict[str, Any]],
        query: str,
        fields: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Search data by query."""
        if not query:
            return data

        search_fields = fields or self.searchable_fields or list(data[0].keys())
        query_lower = query.lower()

        results = []
        for item in data:
            for field in search_fields:
                value = str(item.get(field, "")).lower()
                if query_lower in value:
                    results.append(item)
                    break

        return results

    def faceted_search(
        self,
        data: List[Dict[str, Any]],
        query: str,
        facet_field: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Search with faceted results."""
        results = self.search(data, query)

        facets: Dict[str, List[Dict[str, Any]]] = {}
        for item in results:
            facet_value = item.get(facet_field, "unknown")

            if facet_value not in facets:
                facets[facet_value] = []

            facets[facet_value].append(item)

        return facets
