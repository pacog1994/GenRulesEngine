from typing import Any, Dict

from genrulesengine.registry.actions.action import actions

def test_builtin():
    assert "approve" in actions.registry
    assert "deny" in actions.registry
    assert "login" in actions.registry
    assert "logout" in actions.registry

def test_approve():
    result = actions.dispatch("approve")
    assert result == "approved"
def test_deny():
    result = actions.dispatch("deny")
    assert result == "deny"

def test_login():
    context = {"name": "bill"}
    result = actions.dispatch("login", context)
    assert result == "bill is logged in"

def test_custom_registration():
    @actions.register("test")
    def test(context: Dict[str, Any]):
        return f"hello {context["name"]}"

    context = {"name": "bill"}
    result = actions.dispatch("test", context)
    assert result == "hello bill"