"""
Regression tests for nested mapping types.
Bug: nested Dict sub-fields had key_field left as None,
causing AttributeError during validation.
"""
from typing import Dict, List, Optional

from pydantic import BaseModel


# ---- FAIL_TO_PASS: tests that fail with bug, pass after fix ----


class NestedDictModel(BaseModel):
    data: Dict[str, Dict[str, int]]


def test_nested_dict_validation():
    """Dict[str, Dict[str, int]] should validate successfully."""
    m = NestedDictModel(data={"a": {"b": 42}})
    assert m.data == {"a": {"b": 42}}


def test_nested_dict_with_multiple_inner_keys():
    """Nested dict with multiple inner keys."""
    m = NestedDictModel(data={"a": {"b": 42, "c": 99}})
    assert m.data == {"a": {"b": 42, "c": 99}}


class ListOfDictModel(BaseModel):
    items: List[Dict[str, int]]


def test_list_of_dict_validation():
    """List[Dict[str, int]] should validate successfully."""
    m = ListOfDictModel(items=[{"key": 123}])
    assert m.items == [{"key": 123}]


def test_list_of_dict_multiple():
    """List[Dict[str, int]] with multiple items."""
    m = ListOfDictModel(items=[{"a": 1}, {"b": 2}, {"c": 3}])
    assert m.items == [{"a": 1}, {"b": 2}, {"c": 3}]


class OptionalNestedDictModel(BaseModel):
    data: Optional[Dict[str, Dict[str, int]]] = None


def test_optional_nested_dict_with_value():
    """Optional[Dict[str, Dict[str, int]]] with a value should validate."""
    m = OptionalNestedDictModel(data={"x": {"y": 1}})
    assert m.data == {"x": {"y": 1}}


class NestedDictWithFloatValue(BaseModel):
    metrics: Dict[str, Dict[int, float]]


def test_nested_dict_with_different_types():
    """Dict[str, Dict[int, float]] — key and value types differ across levels."""
    m = NestedDictWithFloatValue(metrics={"cpu": {0: 95.5, 1: 87.2}})
    assert m.metrics == {"cpu": {0: 95.5, 1: 87.2}}


# ---- PASS_TO_PASS: tests that pass regardless ----


class SimpleDictModel(BaseModel):
    data: Dict[str, int]


def test_simple_dict_still_works():
    """Simple Dict[str, int] without nesting should continue to work."""
    m = SimpleDictModel(data={"a": 1, "b": 2})
    assert m.data == {"a": 1, "b": 2}


def test_simple_dict_serialization():
    """Serialization of models with simple dict should work."""
    m = SimpleDictModel(data={"x": 10})
    assert m.dict() == {"data": {"x": 10}}


def test_simple_dict_json():
    """JSON serialization of simple dict models."""
    m = SimpleDictModel(data={"x": 10})
    assert m.json() == '{"data": {"x": 10}}'


def test_simple_dict_copy():
    """Copy of model with simple dict should work."""
    m = SimpleDictModel(data={"x": 10})
    m2 = m.copy()
    assert m2.data == {"x": 10}


def test_optional_nested_dict_default_none():
    """Optional[Dict[str, Dict[str, int]]] with default None should work."""
    m = OptionalNestedDictModel()
    assert m.data is None
