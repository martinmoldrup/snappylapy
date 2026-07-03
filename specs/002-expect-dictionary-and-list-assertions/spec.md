# Feature Specification: Expect Assertions for Dictionaries and Lists

**Feature Id**: 002-expect-dictionary-and-list-assertions  
**Feature Branch**: `features/add-speckit`  
**Created**: October 16, 2025  
**Status**: Draft  
**Input**: User request: "Add the spec for Dictionaries and Lists with the assertions for the expect handler. Make sure the full public API is described; list each public method exactly once."  

---

## Overview
Provide a comprehensive, explicit, and self-documenting assertion API for dictionaries and lists within the `expect` snapshot / assertion framework. The API favors clarity over brevity using phrases like "at least", "exactly and only", and "matching" to remove ambiguity. Configuration helpers allow fine‑grained control of partial comparisons and exclusion rules.

This specification covers ONLY dictionary and list expectations (assertions + configuration chain methods). Snapshot capabilities are assumed to exist (see Spec 001) and are referenced where needed.

---

## User Stories & Testing (Priority Ordered)

### User Story 1 – Assert Required Dictionary Keys (P1)
As a developer I want to assert that a dictionary contains at least a set of keys so missing structural elements are caught early.

Acceptance Scenarios:
1. Given a dict with keys superset of required, when calling `expect(data).to_have_at_least_keys('a','b')` then assertion passes.
2. Given a dict missing one required key, when calling method then assertion fails with message listing missing keys.
3. Given duplicate keys passed as arguments, then duplicates are internally de‑duplicated without failure.

### User Story 2 – Assert Exact Dictionary Key Set (P1)
As a developer I want to assert a dictionary has exactly and only a set of keys so no unexpected fields leak in.

Acceptance Scenarios:
1. Passes when actual keys == expected set (order irrelevant).
2. Fails listing unexpected and missing keys when mismatch.
3. Works when passing either splat args or a list via the overload.

### User Story 3 – Assert Key With Specific Value (P1)
As a developer I want to assert a dict contains a key with a precise value so I confirm business invariants.

Scenarios: pass when equality holds; fail showing actual value; support deep (serializable) values.

### User Story 4 – Subset Relationship Between Dicts (P1)
As a developer I want to assert my dict is a subset of another dict so I can validate partial structures sourced from a superset object.

Scenarios: passes when every (key,value) pair exists in other dict after applying ignore configurations; fails listing first differing pair or missing key.

### User Story 5 – Structural Schema Matching Between Dicts (P1)
As a developer I want to assert two dicts share identical key structure (ignoring values) to validate shape compatibility.

Scenarios: passes when key sets match recursively; fails with path to first difference; respects ignored key paths.

### User Story 6 – Conform to TypedDict Schema (P1)
As a developer I want to validate a dict conforms to a `TypedDict` schema for stronger static + runtime guarantees.

Scenarios: passes when required keys present and optional keys (if any) allowed; type mismatches reported per key.

### User Story 7 – Nested Key Path Existence and Value (P1)
As a developer I want to assert nested paths exist (optionally with value) using either a dot string or list of keys.

Scenarios: path existence passes if all segments present; value assertion compares leaf; invalid path fails listing existing deepest prefix.

### User Story 8 – Dictionary Key Snapshot Parity (P2)
As a developer I want to compare only the key set of my dict to a stored snapshot or another dict so I can detect structural drift.

Scenarios: passes when exact key sets match; fails with diff of added/removed keys; snapshot partial mode allows extra keys when configured.

### User Story 9 – JSON Serializability of Dict (P2)
As a developer I want to ensure a dict is JSON serializable so snapshotting or API payload emission will not fail downstream.

Scenarios: passes when `json.dumps` succeeds; fails with path to first non-serializable object.

### User Story 10 – List Content Presence Assertions (P1)
As a developer I want to assert lists contain certain items (any/all) so I can validate membership expectations.

Scenarios: `to_contain_item_at_least_once` passes if item appears >=1; `to_contain_all_items` requires every expected item present (order agnostic); `to_contain_at_least_one_item_of` passes if any expected item present.

### User Story 11 – Exact List Equality in Order (P1)
As a developer I want to assert a list has exactly and only specified items in order so subtle ordering regressions are caught.

Scenarios: passes when lengths and ordered equality match; fails with first differing index plus summary of extra/missing tail.

### User Story 12 – List Sorting and Order Checks (P2)
As a developer I want to assert a list is sorted (optionally by key and direction) to enforce ordering semantics.

Scenarios: default ascending; with key function and reverse flag; failure shows first index where order breaks plus offending pair.

### User Story 13 – Unordered Snapshot Matching for Lists (P2)
As a developer I want to match a list to a stored snapshot ignoring item order so I can snapshot sets represented as lists.

Scenarios: passes when multiset (bag) equality holds; fails showing counts for differing items.

### User Story 14 – List Subset Relationship (P2)
As a developer I want to check my list is a subset of another list so I can ensure no unexpected elements appear.

Scenarios: pass when every item of subject appears in superset (respecting configured ignores); handle unhashable elements gracefully using linear search.

### User Story 15 – Uniqueness of List Items (P1)
As a developer I want to assert that all items are unique so duplication bugs surface.

Scenarios: passes when len == len(set) (fallback to O(n^2) for unhashables); failure shows first duplicate and count.

### User Story 16 – Predicate Satisfaction Across List Items (All/Any/None) (P1)
As a developer I want to assert all / any / no items satisfy a predicate for flexible semantic checks.

Scenarios: provide failing indices and sample values; support capturing exceptions thrown by predicate and treat as failure with traceback snippet.

### User Story 17 – Type Instance Assertions Over List Items (P1)
As a developer I want to assert all or any items are instances of a class to enforce structural invariants.

Scenarios: failures list offending indices and actual types.

### User Story 18 – JSON Serializability of List (P2)
As a developer I want to ensure a list is JSON serializable so snapshotting or network operations are safe.

Scenarios: same behavior as dict serializability with index path reporting.

### User Story 19 – Configurable Partial & Ignore Behavior (P1)
As a developer I want to configure exclusions (keys, nested key paths, list items, indices, predicates) and partial snapshot matching so assertions are adaptable to evolving data.

Scenarios: configuration chain methods return the expectation object for fluent chaining; ignore precedence: explicit nested path > key > global partial mode.

---

## Public API (Dictionary & List Expectations)
Each method name below appears exactly once. Signatures may include representative parameter names; additional keyword-only options may be added as long as semantics remain.

### Factory / Entry Points
- `expect(data)` – Auto-detect type and return appropriate expectation handler (dict/list among others).  
- `expect.dict(data: dict)` – Explicit dictionary expectation.  
- `expect.list(data: list)` – Explicit list expectation.

### Dictionary Assertion Methods
- `to_have_at_least_keys(*keys: str)`
- `to_have_at_least_keys(keys: list[str])` (overload – same behavior)
- `to_have_key_with_value(key: str, value: object)`
- `to_be_subset_of_another_dict(other_dict: dict)`
- `to_have_same_key_structure_as_dict(other_dict: dict)`
- `to_conform_to_typeddict_schema(typed_dict_cls: type)`
- `to_have_exactly_and_only_keys(*keys: str)`  (supports list overload implicitly similar to at least)
- `to_have_keys_matching_snapshot_exactly()`
- `to_have_keys_matching_dict_exactly(other_dict: dict)`
- `to_have_nested_key_path(path: str | list[str])`
- `to_have_nested_key_path_with_value(path: str | list[str], value: object)`
- `to_be_json_serializable()`

### Dictionary Configuration Chain Methods
- `configure_to_ignore_keys_in_comparison(keys: list[str])`
- `configure_to_ignore_nested_key_paths_in_comparison(paths: list[str | list[str]])` (string dot paths or list form)
- `configure_to_treat_as_partial_snapshot()`

### List Assertion Methods
- `to_have_length(n: int)`
- `to_contain_item_at_least_once(item: object)`
- `to_contain_all_items(items: list[object])`
- `to_contain_at_least_one_item_of(items: list[object])`
- `to_have_exactly_and_only_items_in_order(items: list[object])`
- `to_be_sorted(key: callable | None = None, reverse: bool = False)`
- `to_match_snapshot_ignoring_item_order()`
- `to_be_subset_of_items(other_items: list[object])`
- `to_have_unique_items()`
- `to_be_json_serializable()`
- `to_all_items_satisfy(predicate: callable)`
- `to_any_item_satisfies(predicate: callable)`
- `to_no_items_satisfy(predicate: callable)`
- `to_all_items_be_instances_of(cls: type)`
- `to_any_item_be_instance_of(cls: type)`

### List Configuration Chain Methods
- `configure_to_treat_as_partial_snapshot()`
- `configure_to_ignore_items_in_comparison(items: list[object])`
- `configure_to_ignore_items_at_indices_in_comparison(indices: list[int])`
- `configure_to_ignore_items_matching_predicate_in_comparison(predicate: callable)`
- `configure_to_ignore_nested_items_in_comparison()`  (exclude nested list/dict items from deep comparisons; exact semantics TBD – could treat nested items opaquely)
- `configure_to_ignore_items_with_value_in_comparison(value: object)`

### Legacy / Example Names (Not Part of Canonical API)
The design discussions and examples referenced provisional or illustrative names such as `to_contain_keys`, `to_contain_items`, and the alias `to_equal_list`. These are intentionally NOT included in the canonical Public API list above to keep a single authoritative method per behavior. Implementations MAY provide backwards compatible aliases internally, but they MUST NOT be documented as first‑class going forward. Renaming efforts should focus only on the canonical names listed once in the Public API section.

---

## Functional Requirements
Identifier prefix: FR-DL-

### Dictionary Assertions
- **FR-DL-001**: `to_have_at_least_keys` MUST validate presence of all specified keys; order irrelevant; provide list of missing keys on failure.
- **FR-DL-002**: Overload accepting list MUST behave identically to splat variant.
- **FR-DL-003**: `to_have_key_with_value` MUST fail when key missing OR value inequality; show actual value (repr) and key.
- **FR-DL-004**: `to_be_subset_of_another_dict` MUST ensure every (key,value) pair in subject exists (==) in other dict after ignores applied.
- **FR-DL-005**: `to_have_same_key_structure_as_dict` MUST compare recursive key topology ignoring values; mismatches report first divergent path.
- **FR-DL-006**: `to_conform_to_typeddict_schema` MUST validate required keys and optional keys as defined by the TypedDict; value type mismatches reported using `isinstance` or `typing.get_type_hints` expansions for unions.
- **FR-DL-007**: `to_have_exactly_and_only_keys` MUST fail if any unexpected or missing keys; error enumerates both sets separately.
- **FR-DL-008**: `to_have_keys_matching_snapshot_exactly` MUST load snapshot for the dict under current test context and compare key set only.
- **FR-DL-009**: `to_have_keys_matching_dict_exactly` MUST compare key set equality with provided dict.
- **FR-DL-010**: `to_have_nested_key_path` MUST traverse path segments; supports dot string or list; failure shows deepest existing partial path.
- **FR-DL-011**: `to_have_nested_key_path_with_value` MUST assert both existence and equality of leaf value.
- **FR-DL-012**: `to_be_json_serializable` MUST attempt `json.dumps`; first non-serializable object path reported; success returns self for chaining.

### Dictionary Configuration
- **FR-DL-013**: Ignored keys via `configure_to_ignore_keys_in_comparison` MUST be excluded from all subsequent dictionary comparisons (including snapshot key comparisons) within the expectation context.
- **FR-DL-014**: Ignored nested key paths MUST override simple key ignores and exclude entire substructures.
- **FR-DL-015**: Partial snapshot mode MUST allow subject dict to have a superset of keys compared to snapshot when performing snapshot or key set matching operations.

### List Assertions
- **FR-DL-016**: `to_have_length` MUST compare len(list) to n and report actual length on failure.
- **FR-DL-017**: `to_contain_item_at_least_once` MUST use equality semantics; failure shows repr(list) truncated if large.
- **FR-DL-018**: `to_contain_all_items` MUST verify every expected item is present at least once (no multiplicity requirement) reporting missing items.
- **FR-DL-019**: `to_contain_at_least_one_item_of` MUST pass when any expected present; failure lists all expected items.
- **FR-DL-020**: `to_have_exactly_and_only_items_in_order` MUST assert positional equality; failure message includes index of first diff and summary of expected vs actual lengths.
- **FR-DL-021**: `to_be_sorted` MUST verify ordering using optional key and reverse; failure shows first unsorted pair indices and values.
- **FR-DL-022**: `to_match_snapshot_ignoring_item_order` MUST treat subject and snapshot as multisets; differences reported as counts for items added/removed.
- **FR-DL-023**: `to_be_subset_of_items` MUST confirm every subject item occurs in other_items (>=1) respecting ignores and using element-wise scanning for unhashables.
- **FR-DL-024**: `to_have_unique_items` MUST detect duplicates; for unhashables fallback to slower comparison; error lists duplicate value with count.
- **FR-DL-025**: `to_be_json_serializable` MUST behave analogous to dict variant with index-based path reporting.
- **FR-DL-026**: `to_all_items_satisfy` MUST apply predicate to each item; failure aggregates first N (configurable, default 5) failing indices.
- **FR-DL-027**: `to_any_item_satisfies` MUST pass if predicate true for any; failure shows sample of items (up to N) evaluated.
- **FR-DL-028**: `to_no_items_satisfy` MUST fail if any item returns truthy; message lists first offending indices.
- **FR-DL-029**: `to_all_items_be_instances_of` MUST fail listing first N indices where `isinstance` false.
- **FR-DL-030**: `to_any_item_be_instance_of` MUST pass when at least one item is instance; failure lists actual unique types present.

### List Configuration
- **FR-DL-031**: Partial snapshot mode for lists MUST allow extra items in actual when comparing to snapshot (order-preserving equality otherwise still strict unless using ignoring order method).
- **FR-DL-032**: `configure_to_ignore_items_in_comparison` MUST exclude listed items (by equality) from subsequent content / subset / snapshot comparisons.
- **FR-DL-033**: `configure_to_ignore_items_at_indices_in_comparison` MUST exclude indices (bounds checked) from comparisons.
- **FR-DL-034**: Predicate-based ignore MUST test every item and exclude those returning True.
- **FR-DL-035**: Nested item ignore MUST treat nested list/dict elements as opaque (excluded from deep comparisons and diffs) – exact serialization still possible.
- **FR-DL-036**: Value-based ignore MUST skip items equal to provided value.

### General Behavior
- **FR-DL-037**: All assertion and configuration methods MUST return the expectation instance (fluent API) unless logically they should return a computed result (none in this spec).
- **FR-DL-038**: Error messages MUST be deterministic and include method name.
- **FR-DL-039**: Large structures MUST have diff-friendly truncation (configurable: show first 20 items / keys by default with summary). 
- **FR-DL-040**: Methods MUST be fully type hinted for IDE support.
- **FR-DL-041**: Configuration state MUST NOT leak across separate expectation instances.
- **FR-DL-042**: Snapshot-related key/item comparisons MUST integrate with ignore and partial configurations.

---

## Non-Functional Requirements
- Performance: Operations should be O(n) or O(n log n) where feasible; multiset comparison may use hashing with fallback to O(n^2) for unhashables.
- Memory: Avoid full deep copies of large structures; streaming traversal for JSON serializability checks.
- Extensibility: Adding future assertion types (e.g., numerical tolerance) should not require breaking existing method contracts.
- Error Clarity: Messages must highlight expectation, actual observation, and remediation clue (e.g., "Use configure_to_ignore_keys_in_comparison(['timestamp']) if this field is volatile").

---

## Edge Cases
- Empty dict / list with assertions requiring presence (should fail with clear message listing expected elements/keys).
- Duplicate expected keys or items in input parameters (should be de-duplicated before processing expectations, not causing false failures).
- Deeply nested dict path where intermediate value is not a dict (fail with type info at offending segment).
- Non-string keys in dict when using dot path string (fail instructing to use list path form).
- Unhashable list items in uniqueness or multiset snapshot ignore order comparisons (fallback algorithm engaged).
- Predicate raising exception (capture and include short exception message / type in failure details).
- TypedDict with forward references (resolve using `get_type_hints` to ensure accurate runtime types).
- Large lists where ordering diff occurs late (truncate diff with summary of remaining mismatches count).
- JSON serialization failure for custom object inside list/dict (report JSON path using array index or key chain).
- Overlapping ignore rules (nested path ignore supersedes key ignore; index ignore supersedes item value ignore for that position).
- Partial snapshot + exact key/item assertion (exact assertions override partial mode and still require strict match; document precedence).

---

## Entities
- `DictionaryExpectation` – Holds subject dict, configuration state (ignored keys, ignored nested paths, partial flag), assertion methods.
- `ListExpectation` – Holds subject list, configuration state (ignored items, indices, predicate, nested ignore flag, value ignore, partial flag), assertion methods.
- `IgnoreRuleSet` – Internal structure encapsulating ignore logic for normalization and reuse across snapshot + manual assertions.
- `PredicateResult` – Internal optional helper for storing predicate evaluation results (value, index, success, error info).

---

## Success Criteria
- **SC-DL-001**: All listed Public API methods are implemented with passing unit tests exercising both success and failure paths.
- **SC-DL-002**: 100% of dictionary/list assertions produce deterministic, readable failure messages under repeated runs.
- **SC-DL-003**: Performance baseline: 100k-item list uniqueness assertion completes under 0.5s on modern laptop (reference hardware to be documented) when items hashable.
- **SC-DL-004**: JSON serializability checks identify first failing path for nested structures at depth up to at least 10.
- **SC-DL-005**: Configuration chaining works in any order without state loss (`expect(data).configure_to_ignore_keys_in_comparison([...]).to_have_at_least_keys('a')`).
- **SC-DL-006**: Partial snapshot mode does not cause false negatives for additional keys/items while still detecting missing required ones.
- **SC-DL-007**: All methods have complete type hints and appear in IDE autocomplete.
- **SC-DL-008**: Unordered snapshot matching correctly identifies multiplicity differences (e.g., one extra duplicate) in failure message.
- **SC-DL-009**: TypedDict schema validation reports at least the first 3 mismatches (or all if <3) in failure output.
- **SC-DL-010**: No configuration state leakage between different expectation instances (verified via separate tests).

---

## Open Questions / TBD
- Should `configure_to_ignore_nested_items_in_comparison` accept a predicate or depth parameter for finer control? (Currently boolean semantics.)
- Should multiset comparison for unordered snapshot allow a tolerance threshold? (Not in initial scope.)
- Provide global configuration for truncation limits? (Likely in a core settings object – future spec.)

---

## Out of Scope
- Numeric tolerance assertions (future feature).
- Regex or pattern-based ignoring for dict keys (future feature).
- Order-insensitive exact equality for lists outside snapshot context (could add dedicated method later).

---

## Traceability Matrix (Excerpt)
| User Story | Requirement IDs |
|------------|-----------------|
| 1 | FR-DL-001, FR-DL-013 |
| 2 | FR-DL-007 |
| 3 | FR-DL-003 |
| 4 | FR-DL-004, FR-DL-013..015 |
| 5 | FR-DL-005, FR-DL-013..015 |
| 6 | FR-DL-006 |
| 7 | FR-DL-010, FR-DL-011 |
| 8 | FR-DL-008, FR-DL-009, FR-DL-015 |
| 9 | FR-DL-012 |
| 10 | FR-DL-017..019, FR-DL-032..036 |
| 11 | FR-DL-020, FR-DL-031 |
| 12 | FR-DL-021 |
| 13 | FR-DL-022, FR-DL-031 |
| 14 | FR-DL-023, FR-DL-032..036 |
| 15 | FR-DL-024 |
| 16 | FR-DL-026..028 |
| 17 | FR-DL-029, FR-DL-030 |
| 18 | FR-DL-025 |
| 19 | FR-DL-013..016, FR-DL-031..036, FR-DL-037..042 |

---

## Implementation Notes (Informative)
- Method implementations should raise custom assertion exception (library-defined) to integrate with pytest introspection.
- Overloads can be implemented via accepting `*keys_or_list` then normalizing if single list argument provided.
- JSON serializability path tracking can be done with a DFS capturing key/index chain; bail early on first failure.
- Multiset comparison: try hashing; if any unhashable -> fallback to element removal approach.
- TypedDict validation: use `get_type_hints` to resolve runtime types and handle `Required` / `NotRequired` attributes.

---

End of Spec.
