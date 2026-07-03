## DictExpect - New Assertion Methods:
- `to_be(expected)` – Basic equality assertion (actual == expected).
- `to_equal(expected)` – Deep equality assertion (actual == expected, alias).
- `to_be_strictly_equal_to(expected)` – Type-strict equality assertion (type and value must match).
- `to_be_close_to(expected, delta)` – Numeric values within delta, others must match exactly.
- `to_have_the_same_properties_as_snapshot()` – Assert that the dictionary has the same keys as the stored snapshot.
- `to_have_property(property_path)` – Assert that the dictionary contains a property path (dot separated).
- `to_be_truthy()` – Assert that the dictionary evaluates to True.
- `to_be_falsy()` – Assert that the dictionary evaluates to False.
- `ignore_keys(keys)` – Exclude the given keys from subsequent comparisons and snapshots.

## ObjectExpect – Assertion Methods

- `to_be(expected)` – Basic equality assertion.
- `to_equal(expected)` – Deep equality assertion.
- `to_be_strictly_equal_to(expected)` – Type-strict equality assertion.
- `to_be_truthy()` / `to_be_falsy()` – Truthiness assertions.
- `to_be_instance_of(expected_type)` – Type checking assertion.
- `to_have_attribute(attribute_name)` – Single attribute existence check.
- `to_have_attributes(*attribute_names)` – Multiple attributes existence check.
- `to_be_none()` / `to_not_be_none()` – None value assertions.

## StringExpect – Assertion Methods

- `to_be(expected)` / `to_equal(expected)` – String equality.
- `to_contain(substring)` / `to_not_contain(substring)` – Substring checks.
- `to_start_with(prefix)` / `to_end_with(suffix)` – Prefix/suffix checks.
- `to_have_length(expected_length)` – Length validation.
- `to_be_empty()` / `to_not_be_empty()` – Empty string checks.
- `to_match_regex(pattern)` / `to_not_match_regex(pattern)` – Regex matching.
- `to_be_uppercase()` / `to_be_lowercase()` / `to_be_title_case()` – Case checks.
- `to_be_numeric()` / `to_be_alphabetic()` / `to_be_alphanumeric()` – Character type checks.
- `to_contain_any_of(substrings)` / `to_contain_all_of(substrings)` – Multiple substring checks.
- `to_fuzzy_match(expected, similarity)` – Fuzzy string matching with configurable similarity threshold.
- `to_be_truthy()` / `to_be_falsy()` – Truthiness assertions.

## ListExpect – Assertion Methods

- `to_be(expected)` / `to_equal(expected)` – List equality.
- `to_contain(item)` / `to_not_contain(item)` – Item presence checks.
- `to_have_length(expected_length)` – Length validation.
- `to_be_empty()` / `to_not_be_empty()` – Empty list checks.
- `to_contain_all_of(items)` / `to_contain_any_of(items)` – Multiple item checks.
- `to_start_with(prefix)` / `to_end_with(suffix)` – Prefix/suffix list checks.
- `to_be_sorted(reverse=False)` – Sorted order validation.
- `to_have_unique_elements()` – Uniqueness validation.
- `to_be_truthy()` / `to_be_falsy()` – Truthiness assertions.

## BytesExpect – Assertion Methods

- `to_be(expected)` / `to_equal(expected)` – Bytes equality.
- `to_contain(subsequence)` / `to_not_contain(subsequence)` – Subsequence checks.
- `to_start_with(prefix)` / `to_end_with(suffix)` – Prefix/suffix checks.
- `to_have_length(expected_length)` – Length validation.
- `to_be_empty()` / `to_not_be_empty()` – Empty bytes checks.
- `to_decode_as(expected_string, encoding="utf-8")` – Decoding validation.
- `to_match_regex_when_decoded(pattern, encoding="utf-8")` – Regex matching on decoded content.
- `to_contain_any_of(subsequences)` / `to_contain_all_of(subsequences)` – Multiple subsequence checks.
- `to_be_truthy()` / `to_be_falsy()` – Truthiness assertions.

## Summary of what was general Across All Expect Classes
- `to_be(expected)` / `to_equal(expected)` – Basic equality assertion.
- `to_be_truthy()` / `to_be_falsy()` – Truthiness assertions.
- `to_be_none()` / `to_not_be_none()` – None value assertions.

# Experiment what does AI models suggest.
Prompt:
Please suggest what assertion methods you would expect in a snapshot testing library, for pytest in python. The library defines an expect fixture that can be used in tests to make assertions on various data types.

Example usage:
```python
def test_snapshot_dict(expect: Expect):
    """Test snapshot with dictionary data."""
    expect.dict({
        "name": "John Doe",
        "age": 31
    }).to_match_snapshot()

```

We have the following data types:
expect.dict()
expect.list()
expect.string()
expect.bytes()
expect.object()  # for any other python object
expect.dataframe()  # pandas dataframe if pandas is installed

Please suggest what other assertion methods (other than .to_match_snapshot()) you would expect for each data type.

## GPT-5-Codex suggestions
Common to all types
    .to_match_snapshot()
    .to_diff_snapshot() for comparing and returning diff info
    .to_raise_on_change() ensuring snapshot change triggers failure
    .to_match_named("...") for alternate snapshot names

expect.dict()
    .to_have_keys([...]) verifying expected keys
    .to_have_subset({...}) checking partial structure
    .to_match_schema(schema) for structural validation


expect.list()
    .to_have_length(n) asserting list size
    .to_contain(item) / .to_contain_subset([...])
    .to_match_ordered_snapshot() forcing order-sensitive comparison

expect.string()
    .to_match_regex(pattern)
    .to_contain(substring)
    .to_match_normalized_snapshot() ignoring whitespace or casing

expect.bytes()
    .to_match_hex_snapshot() storing hex dumps
    .to_have_length(n)
    .to_match_base64_snapshot() for readable serialization

expect.object()
    .to_match_repr_snapshot() capturing repr only
    .to_match_attrs_snapshot([...]) limiting to selected attributes
    .to_match_serialized_snapshot(serializer=...) allowing custom serialization

expect.dataframe()
    .to_match_schema_snapshot() tracking column metadata
    .to_match_values_snapshot(indexed=True) comparing values with index control
    .to_match_profile_snapshot() leveraging summary stats

# Copilot suggestions


### **General (All Types)**
These could be available across all types:
- `.not_to_match_snapshot()` – Assert that the current value does **not** match the stored snapshot.
- `.to_match_snapshot(name="...")` – Support named snapshots for multiple assertions in one test.
- `.to_match_serialized_snapshot(serializer=...)` – Allow custom serialization (e.g., for objects or complex types).
- `.to_match_partial_snapshot(fields=[...])` – Only compare specific fields or keys.

---

### **`expect.dict()`**
- `.to_have_keys(*keys)` – Assert that the dictionary contains specific keys.
- `.to_have_key_value(key, value)` – Assert that a key maps to a specific value.
- `.to_match_schema(schema: dict)` – Validate structure against a schema (e.g., types, required keys).
- `.to_be_subset_of(other_dict)` – Assert that the dict is a subset of another.

---

### **`expect.list()`**
- `.to_have_length(n)` – Assert list length.
- `.to_contain(item)` – Assert that an item is in the list.
- `.to_match_ordered_snapshot()` – Snapshot with order sensitivity.
- `.to_match_unordered_snapshot()` – Snapshot ignoring order.
- `.to_all_match(predicate)` – Assert all elements satisfy a condition.

---

### **`expect.string()`**
- `.to_match_regex(pattern)` – Assert string matches a regex.
- `.to_contain(substring)` – Assert substring is present.
- `.to_start_with(prefix)` / `.to_end_with(suffix)` – Assert string boundaries.
- `.to_be_equal_ignoring_case()` – Case-insensitive comparison.

---

### **`expect.bytes()`**
- `.to_have_length(n)` – Assert byte length.
- `.to_match_base64_snapshot()` – Snapshot after base64 encoding.
- `.to_match_hex_snapshot()` – Snapshot after hex encoding.

---

### **`expect.object()`**
- `.to_have_attributes(**kwargs)` – Assert object has attributes with expected values.
- `.to_be_instance_of(cls)` – Assert object type.
- `.to_match_repr_snapshot()` – Snapshot of `repr(obj)`.
- `.to_match_str_snapshot()` – Snapshot of `str(obj)`.

---

### **`expect.dataframe()`** (if `pandas` is installed)
- `.to_match_shape(rows, cols)` – Assert shape.
- `.to_have_columns(*cols)` – Assert presence of columns.
- `.to_match_schema(schema: dict)` – Validate column types.
- `.to_match_sorted_snapshot(by=..., ascending=True)` – Snapshot after sorting.
- `.to_match_filtered_snapshot(filter_fn)` – Snapshot after filtering rows.

# Grok suggestions


| Data Type          | Method                  | Description |
|--------------------|-------------------------|-------------|
| `expect.dict()`   | `.to_have_key(key)`    | Asserts that the dictionary contains the given key (supports nested keys via dot notation, e.g., `'user.name'`). |
|                    | `.to_have_keys(keys)`  | Asserts that the dictionary contains all specified keys (accepts a list of keys; supports partial matching). |
|                    | `.to_have_value(key, value)` | Asserts that the value for the given key equals the expected value (supports nested access). |
|                    | `.to_have_length(n)`   | Asserts that the dictionary has exactly `n` keys. |
|                    | `.to_have_only_keys(keys)` | Asserts that the dictionary has exactly the specified keys (no extras). |
| `expect.list()`   | `.to_have_length(n)`   | Asserts that the list has exactly `n` elements. |
|                    | `.to_contain(item)`    | Asserts that the list contains the given item (uses `in` operator; supports custom matchers for complex items). |
|                    | `.to_contain_exactly(items)` | Asserts that the list matches the given items in order (ignores duplicates unless specified). |
|                    | `.to_be_sorted(key=None, reverse=False)` | Asserts that the list is sorted (optionally by a key function; useful for snapshot diffs). |
| `expect.string()` | `.to_equal(expected)`  | Asserts that the string equals the expected value (exact match). |
|                    | `.to_contain(substring)` | Asserts that the string contains the given substring. |
|                    | `.to_match(pattern)`   | Asserts that the string matches the given regex pattern (accepts compiled regex or string). |
|                    | `.to_start_with(prefix)` | Asserts that the string starts with the given prefix. |
|                    | `.to_end_with(suffix)` | Asserts that the string ends with the given suffix. |
|                    | `.to_be_empty()`       | Asserts that the string is empty. |
| `expect.bytes()`  | `.to_equal(expected)`  | Asserts that the bytes equal the expected bytes object (exact match). |
|                    | `.to_contain(subbytes)` | Asserts that the bytes contain the given sub-bytes sequence. |
|                    | `.to_have_length(n)`   | Asserts that the bytes have exactly `n` bytes. |
|                    | `.to_be_empty()`       | Asserts that the bytes are empty. |
| `expect.object()` | `.to_be_instance_of(cls)` | Asserts that the object is an instance of the given class (or subclass). |
|                    | `.to_satisfy(predicate)` | Asserts that the object satisfies a custom callable predicate (e.g., a function returning True/False). |
|                    | `.to_have_attribute(attr, value=None)` | Asserts that the object has the given attribute (optionally equals a value). |
|                    | `.to_be_truthy()` / `.to_be_falsy()` | Asserts that the object evaluates to True/False in a boolean context. |
| `expect.dataframe()` | `.to_have_shape(rows, cols=None)` | Asserts that the DataFrame has the expected shape (rows and optional columns). |
|                    | `.to_have_columns(columns)` | Asserts that the DataFrame has exactly the specified columns (order-insensitive). |
|                    | `.to_have_index(index_type=None)` | Asserts that the index matches the expected type or values (e.g., RangeIndex). |
|                    | `.to_equal(other_df)`  | Asserts that the DataFrame equals another (compares data, index, and columns; ignores dtypes unless specified). |
|                    | `.to_have_dtypes(dtypes)` | Asserts that specified columns have the expected dtypes (accepts dict of column: dtype). |

# GPT-4.1 with custom prompt:


| Data Type   | Useful Assertion Methods                                                                                   |  
|-------------|----------------------------------------------------------------------------------------------------------|  
| dict        | to_contain_keys, to_have_key_with_value, to_match_schema, to_match_snapshot_ignoring, ...                |  
| list        | to_contain, to_have_length, to_match_ordered_snapshot, to_match_unordered_snapshot, ...                  |  
| string      | to_match_regex, to_contain, to_start_with, to_end_with, to_match_lines_snapshot, ...                     |  
| bytes       | to_have_length, to_match_bytes_snapshot                                                                  |  
| object      | to_have_attribute, to_match_attrs, to_match_repr_snapshot                                                |  
| dataframe   | to_match_dataframe_snapshot, to_match_dataframe_schema, to_match_dataframe_shape, to_match_dataframe_head|  
  
---  

# Summary of suggestions
Here’s an overview summarizing the different suggestions for assertion and snapshot methods across various data types, as proposed by the different sources:  
  
---  
  
## 1. **General/All Types**  
- **Snapshot Testing:** Methods to compare current values to stored snapshots, with options for named snapshots, partial snapshots (comparing only certain fields), and custom serialization.  
- **Diff and Change Detection:** Methods to return diffs or fail tests if snapshots change unexpectedly.  
- **Negation:** Ability to assert that a value does *not* match a snapshot.  
  
---  
  
## 2. **Dictionaries (`expect.dict()`)**  
- **Key Presence:** Assert that specific keys (or only those keys) are present, including support for nested keys.  
- **Key-Value Assertions:** Check that certain keys map to expected values.  
- **Subset/Schema:** Assert that a dict is a subset of another, or matches a given schema (structure, types, required keys).  
- **Length:** Assert the number of keys.  
  
---  
  
## 3. **Lists (`expect.list()`)**  
- **Length:** Assert the number of elements.  
- **Containment:** Check for presence of items or subsets.  
- **Order:** Assert order (ordered/unordered snapshot comparisons).  
- **Content Matching:** Assert all elements satisfy a predicate, or that the list contains exactly certain items (optionally in order).  
- **Sorting:** Assert that the list is sorted (optionally by a key).  
  
---  
  
## 4. **Strings (`expect.string()`)**  
- **Equality/Containment:** Assert exact match or substring presence.  
- **Regex:** Assert that the string matches a regex pattern.  
- **Boundaries:** Assert start/end with specific substrings.  
- **Case/Whitespace Insensitivity:** Compare ignoring case or whitespace.  
- **Empty Check:** Assert that the string is empty.  
  
---  
  
## 5. **Bytes (`expect.bytes()`)**  
- **Equality/Containment:** Assert exact match or presence of sub-bytes.  
- **Length:** Assert number of bytes.  
- **Encoding Snapshots:** Store and compare base64 or hex representations.  
- **Empty Check:** Assert that the bytes object is empty.  
  
---  
  
## 6. **Objects (`expect.object()`)**  
- **Type/Instance:** Assert object is an instance of a class.  
- **Attributes:** Assert presence and values of attributes.  
- **Custom Predicates:** Assert object satisfies a callable predicate.  
- **Snapshot Representations:** Compare `repr`, `str`, or custom-serialized snapshots.  
- **Truthiness:** Assert object is truthy or falsy.  
  
---  
  
## 7. **DataFrames (`expect.dataframe()`)**  
- **Shape/Columns:** Assert number of rows/columns and presence of specific columns.  
- **Schema/Types:** Assert column types or match a schema.  
- **Index:** Assert index type or values.  
- **Equality:** Assert equality with another DataFrame.  
- **Snapshot Variants:** Compare sorted, filtered, or profiled snapshots (summary stats).  
  
---  
  
## **Summary Table**  
  
| Data Type   | Key Assertion/Snapshot Methods                                                                 |  
|-------------|-----------------------------------------------------------------------------------------------|  
| All Types   | Snapshot matching, diffing, named/partial/custom snapshots, negation                          |  
| dict        | Key presence, key-value, subset, schema, length                                               |  
| list        | Length, containment, order, all-match, sorting                                                |  
| string      | Equality, containment, regex, boundaries, case/whitespace, empty                              |  
| bytes       | Equality, containment, length, base64/hex snapshots, empty                                    |  
| object      | Instance/type, attributes, custom predicates, repr/str/custom snapshots, truthiness           |  
| dataframe   | Shape, columns, schema/types, index, equality, sorted/filtered/profiled snapshots             |  
  
---  
  
**In summary:**    
The suggestions cover a comprehensive set of assertion and snapshot methods for common Python data types, focusing on flexible, expressive, and robust testing—especially for structural, content, and serialization-based comparisons. Each data type has tailored methods, with a strong emphasis on snapshot testing and schema validation.

# Design summerized from suggestions:
Certainly! Here’s a concise list of recommended API function names for each assertion, based on the most common and intuitive suggestions:  
  
---  
  
### **General / All Types**  
- **Match snapshot:** `to_match_snapshot()`  
- **Not match snapshot:** `not_to_match_snapshot()`  
- **Match named snapshot:** `to_match_snapshot(name=...)`  
- **Match partial snapshot:** `to_match_partial_snapshot(fields=...)`  
- **Match with custom serializer:** `to_match_serialized_snapshot(serializer=...)`  
- **Raise on change:** `to_raise_on_change()`  
- **Return diff:** `to_diff_snapshot()`  
  
---  
  
### **Dictionaries**  
- **Has keys:** `to_have_keys(*keys)`  
- **Has key-value:** `to_have_key_value(key, value)`  
- **Is subset of:** `to_be_subset_of(other_dict)`  
- **Matches schema:** `to_match_schema(schema)`  
- **Has length:** `to_have_length(n)`  
- **Has only keys:** `to_have_only_keys(*keys)`  
  
---  
  
### **Lists**  
- **Has length:** `to_have_length(n)`  
- **Contains item:** `to_contain(item)`  
- **Contains exactly:** `to_contain_exactly(items)`  
- **All match predicate:** `to_all_match(predicate)`  
- **Is sorted:** `to_be_sorted(key=None, reverse=False)`  
- **Match ordered snapshot:** `to_match_ordered_snapshot()`  
- **Match unordered snapshot:** `to_match_unordered_snapshot()`  
  
---  
  
### **Strings**  
- **Equals:** `to_equal(expected)`  
- **Contains substring:** `to_contain(substring)`  
- **Matches regex:** `to_match_regex(pattern)`  
- **Starts with:** `to_start_with(prefix)`  
- **Ends with:** `to_end_with(suffix)`  
- **Equals ignoring case:** `to_be_equal_ignoring_case()`  
- **Is empty:** `to_be_empty()`  
  
---  
  
### **Bytes**  
- **Equals:** `to_equal(expected)`  
- **Contains subbytes:** `to_contain(subbytes)`  
- **Has length:** `to_have_length(n)`  
- **Is empty:** `to_be_empty()`  
- **Match base64 snapshot:** `to_match_base64_snapshot()`  
- **Match hex snapshot:** `to_match_hex_snapshot()`  
  
---  
  
### **Objects**  
- **Is instance of:** `to_be_instance_of(cls)`  
- **Has attributes:** `to_have_attributes(**kwargs)`  
- **Has attribute:** `to_have_attribute(attr, value=None)`  
- **Satisfies predicate:** `to_satisfy(predicate)`  
- **Match repr snapshot:** `to_match_repr_snapshot()`  
- **Match str snapshot:** `to_match_str_snapshot()`  
- **Is truthy:** `to_be_truthy()`  
- **Is falsy:** `to_be_falsy()`  
  
---  
  
### **DataFrames**  
- **Has shape:** `to_have_shape(rows, cols=None)`  
- **Has columns:** `to_have_columns(*cols)`  
- **Has index:** `to_have_index(index_type=None)`  
- **Equals another DataFrame:** `to_equal(other_df)`  
- **Has dtypes:** `to_have_dtypes(dtypes)`  
- **Match schema:** `to_match_schema(schema)`  
- **Match sorted snapshot:** `to_match_sorted_snapshot(by=..., ascending=True)`  
- **Match filtered snapshot:** `to_match_filtered_snapshot(filter_fn)`  
- **Match profile snapshot:** `to_match_profile_snapshot()`  
  
---  
  
These function names are clear, consistent, and reflect the most widely suggested or intuitive API designs.