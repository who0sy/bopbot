import pytest
from mock import Mock, patch

from bopbot.dom.elements import (
    BaseSelector,
    LabeledSelector,
    flatten_selector_hierarchy,
    create_labeled_selector,
    validate_label_name,
    add_selector_to,
)
from bopbot.dom.exceptions import SelectorError


class TestBaseSelector:
    def test_pop_syncs_to_str(self):
        selector = BaseSelector(dom_hierarchy=["body", "div", "div", "button"])
        initial_path = selector.to_str()
        selector.pop()
        assert initial_path != selector.to_str()
        assert selector.to_str() == selector._str

    def test_hierarchy_must_be_populated(self):
        selector = BaseSelector(dom_hierarchy=[])
        with pytest.raises(SelectorError):
            selector.to_str()

        selector.set_hierarchy(dom_hierarchy=1)
        with pytest.raises(SelectorError):
            selector.to_query()


def test_flatten_selector_hierarchy():
    expected = "my > name > is > bobby"
    hierarchy = [
        BaseSelector(dom_hierarchy=["my"]),
        LabeledSelector(label="bob_button", dom_hierarchy=["name", "is"]),
        [],
        "bobby",
    ]
    selector = BaseSelector(
        dom_hierarchy=flatten_selector_hierarchy(selector_hierarchy=hierarchy)
    )
    assert expected == selector.to_str()


class TestCreateLabeledSelector:
    def test_validates_dom_hierarchy(self):
        validate_mock = Mock()
        hierarchy = ["body", "button"]
        with patch(
            target="bopbot.dom.elements.validate_dom_hierarchy", new=validate_mock
        ):
            create_labeled_selector(label="signup_button", selector_hierarchy=hierarchy)
            validate_mock.assert_called_with(dom_hierarchy=hierarchy)

    def test_does_not_validate_label(self):
        validate_mock = Mock()
        with patch(target="bopbot.dom.elements.validate_label_name", new=validate_mock):
            create_labeled_selector(
                label="signup_button", selector_hierarchy=["body", "button"]
            )
        failure_msg = (
            "validate_Label_name should only be called when add_selector_to is called"
        )
        assert not validate_mock.called, failure_msg


class TestAddSelectorTo:
    def test_rasies_selector_error_with_invalid_label(self):
        with pytest.raises(SelectorError):
            add_selector_to(obj=self, label=" _catdog", selector_hierarchy=["a"])

        with pytest.raises(SelectorError):
            add_selector_to(obj=self, label=" catdog", selector_hierarchy=["a"])

        with pytest.raises(SelectorError):
            add_selector_to(obj=self, label="cat dog!", selector_hierarchy=["a"])

        with pytest.raises(SelectorError):
            add_selector_to(obj=self, label="catdog!", selector_hierarchy=["a"])

    def test_selector_added_to_attr(self):
        label_name = "billy_jenkins_selector"
        add_selector_to(self, label=label_name, selector_hierarchy=["a"])

        assert hasattr(self, label_name)
