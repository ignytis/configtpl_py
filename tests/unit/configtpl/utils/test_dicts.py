import unittest

from configtpl.utils.dicts import dict_deep_merge, dict_init_dicts_from_list


class TestDictUtils(unittest.TestCase):
  def test_dict_deep_merge_empty(self) -> None:
    # Test merging empty dictionaries
    assert dict_deep_merge() == {}
    assert dict_deep_merge({}, {}) == {}
    assert dict_deep_merge({}, {"a": 1}) == {"a": 1}
    assert dict_deep_merge({"a": 1}, {}) == {"a": 1}

  def test_dict_deep_merge_simple(self) -> None:
    # Test merging simple dictionaries with no overlapping keys
    d1 = {"a": 1, "b": 2}
    d2 = {"c": 3, "d": 4}
    expected = {"a": 1, "b": 2, "c": 3, "d": 4}
    assert dict_deep_merge(d1, d2) == expected

    # Test merging simple dictionaries with overlapping keys
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    expected = {"a": 1, "b": 3, "c": 4}
    assert dict_deep_merge(d1, d2) == expected

  def test_dict_deep_merge_nested(self) -> None:
    # Test merging nested dictionaries with no overlapping keys
    d1 = {"a": {"x": 1}, "b": 2}
    d2 = {"c": {"y": 3}, "d": 4}
    expected = {"a": {"x": 1}, "b": 2, "c": {"y": 3}, "d": 4}
    assert dict_deep_merge(d1, d2) == expected

    # Test merging nested dictionaries with overlapping keys
    d1 = {"a": {"x": 1, "z": 5}, "b": 2}
    d2 = {"a": {"y": 3, "z": 6}, "c": 4}
    expected = {"a": {"x": 1, "y": 3, "z": 6}, "b": 2, "c": 4}
    assert dict_deep_merge(d1, d2) == expected

    # Test merging deeper nested dictionaries
    d1 = {"a": {"b": {"c": 1}}}
    d2 = {"a": {"b": {"d": 2}}}
    expected = {"a": {"b": {"c": 1, "d": 2}}}
    assert dict_deep_merge(d1, d2) == expected

  def test_dict_deep_merge_multiple_dicts(self) -> None:
    # Test merging more than two dictionaries
    d1 = {"a": 1, "b": {"x": 10}}
    d2 = {"c": 3, "b": {"y": 20}}
    d3 = {"a": 5, "d": 4, "b": {"z": 30}}
    expected = {"a": 5, "b": {"x": 10, "y": 20, "z": 30}, "c": 3, "d": 4}
    assert dict_deep_merge(d1, d2, d3) == expected

  def test_dict_deep_merge_type_overwriting(self) -> None:
    # Test cases where a dict value is overwritten by a non-dict value and vice-versa
    d1 = {"a": {"x": 1}, "b": 2}
    d2 = {"a": 10, "b": {"y": 20}}  # 'a' becomes int, 'b' becomes dict
    expected = {"a": 10, "b": {"y": 20}}
    assert dict_deep_merge(d1, d2) == expected

    d1 = {"a": 10, "b": {"y": 20}}
    d2 = {"a": {"x": 1}, "b": 2}  # 'a' becomes dict, 'b' becomes int
    expected = {"a": {"x": 1}, "b": 2}
    assert dict_deep_merge(d1, d2) == expected

  def test_dict_init_dicts_from_list(self) -> None:
    # Test with all None inputs
    assert dict_init_dicts_from_list(None, None, None) == ({}, {}, {})

    # Test with mixed None and dict inputs
    d1 = {"a": 1}
    d2 = {"b": 2}
    assert dict_init_dicts_from_list(d1, None, d2) == (d1, {}, d2)

    # Test with all dict inputs
    d3 = {"c": 3}
    assert dict_init_dicts_from_list(d1, d2, d3) == (d1, d2, d3)

    # Test with no inputs
    assert dict_init_dicts_from_list() == ()

    # Test with empty dict
    assert dict_init_dicts_from_list({}, None) == ({}, {})
