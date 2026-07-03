# Recommendation for clear API design

Recommendations
1. Use phrases like "at least," "exactly and only," and "matching" to clarify the scope of the assertions.
2. Add "dict" or "dictionary" where necessary to avoid ambiguity about the type of object being compared.
3. Ensure method names explicitly describe their behavior, even if they become longer.
4. Explicit is better than implicit; avoid assumptions about default behaviors.
5. Avoiding generic terms like "another" in favor of more specific terms like "dict" improves clarity.
6. Use consistent terminology across across the API.
   - dictionaries => dicts, contains items that has keys and values
   - lists => lists, contains items

### **Dictionaries**  
Usage example: expect({'key1': 'value1', 'key2': 2}).to_contain_keys('key1', 'key2')

- **Has keys:** `to_have_at_least_keys(*keys)`
- **Has keys (overload):** `to_have_at_least_keys(keys: list)`
- **Has key-value:** `to_have_key_with_value(key, value)`  
- **Is subset of:** `to_be_subset_of_another_dict(other_dict)`  
- **Matches schema of another dict:** `to_have_same_key_structure_as_dict(other_dict)`
- **Matches typeddict schema:** `to_conform_to_typeddict_schema(TypedDictClass)`
- **Has exactly provided keys:** `to_have_exactly_and_only_keys(*keys)`
- **Has same keys as snapshot:** `to_have_keys_matching_snapshot_exactly()`
- **Has same keys as dict:** `to_have_keys_matching_dict_exactly(other_dict)`
- **Has nested key path (dot separated path in nested dict, or a list of keys):** `to_have_nested_key_path(path: list | str)`
- **Has nested key path with value:** `to_have_nested_key_path_with_value(path, value)`
- **To be serializable to JSON:** `to_be_json_serializable()`


Configurations:
- `configure_to_ignore_keys_in_comparison(keys)` – Exclude the given keys from subsequent comparisons and snapshots.
- `configure_to_ignore_nested_key_paths_in_comparison(paths)` – Exclude the given nested key paths from subsequent comparisons and snapshots.
- `configure_to_treat_as_partial_snapshot()` – Treat the dictionary as a partial snapshot, allowing extra keys in actual data.
---  
  
### **Lists**
Usage example: expect([1, 2, 3]).to_contain_items(2, 3)
expect([1, 2, 3]).to_all_match(lambda x: x > 0)  # Passes

Assertions:
- **Has length:** `to_have_length(n)`  
- **Contains item:** `to_contain_item_at_least_once(item)`
- **To contain all of:** `to_contain_all_items(items)`
- **To contain any of the items:** `to_contain_at_least_one_item_of(items)`
- **Contains exactly:** `to_have_exactly_and_only_items_in_order(items)`  or to_equal_list(list)
- **Is sorted (with optional inputs):** `to_be_sorted(key=None, reverse=False)`
- **Match unordered snapshot saved to disk:** `to_match_snapshot_ignoring_item_order()`
- **Is subset of another list:** `to_be_subset_of_items(other_items: list[Any])`

- **To have unique items:** `to_have_unique_items()`
- **To be serializable to JSON:** `to_be_json_serializable()`
- **Assert all items satisfy a condition:** `to_all_items_satisfy(predicate)`
- **Assert any item satisfies a condition:** `to_any_item_satisfies(predicate)`
- **Assert no items satisfy a condition:** `to_no_items_satisfy(predicate)`
- **All items are instances of a type:** `to_all_items_be_instances_of(cls)`
- **Any item is an instance of a type:** `to_any_item_be_instance_of(cls)`


Configurations:
- `configure_to_treat_as_partial_snapshot()` – Treat the list as a partial snapshot, allowing extra items in actual data.
- `configure_to_ignore_items_in_comparison(items)` – Exclude the given items from subsequent comparisons and snapshots.
- `configure_to_ignore_items_at_indices_in_comparison(indices)` – Exclude items at the given indices from subsequent comparisons and snapshots.
- `configure_to_ignore_items_matching_predicate_in_comparison(predicate)` – Exclude items matching the given predicate from subsequent comparisons and snapshots.
- `configure_to_ignore_nested_items_in_comparison()` – Exclude nested items from subsequent comparisons and snapshots.
- `configure_to_ignore_items_with_value_in_comparison(value)` – Exclude items with the given value from subsequent comparisons and snapshots.

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