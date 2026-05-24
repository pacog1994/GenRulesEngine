[![pg github](https://img.shields.io/badge/GitHub-pacog1994-181717.svg?style=flat&logo=github)](https://github.com/pacog1994)
[![python](https://img.shields.io/badge/Python-3.1.4-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

# About

**GenRulesEngine** is a lightweight, generic rules-engine library designed to serve as a flexible skeleton for a wide range of rule-based use cases. It provides a consistent set of terminology and components—such as rules, conditions, and actions—to improve clarity and maintainability across different implementations.
Like all rules engines, the goal of GenRulesEngine is to cleanly separate business logic (“rules”) from application code. All rules are evaluated at runtime and produce a list of RuleResults to pass downstream. 

# Terminology

* Rule: A rule represents a single piece of business logic made up of:
  -  conditions: Boolean expressions that must evaluate to true
  -  actions: Functions or handlers when all conditions are satisfied
  -  depends_on: List of dependencies on other rules denoted by its unique, cap-insensitive label


* Condition: A condition is predicate that tests one or more inputs, evaluating to True or False:

	-  `userole == "admin"`
	- `token.ttl = 400
	-   `order.total > 100 AND customer.age >= 18`


* Action: An action is an extremely flexible event to be handled, emitted when a rule's condition passes:
	- modifying a value
	- appending to a list
	- calling a callback
	- returning a decision allow/deny
    - **NOTE:** Emitting Actions are the responsibility of the downstream service:


*  Context Data: A text are the runtime data objects passed into the engine during evaluation:
	- a client-server's or server-server's request payload
	- triggered transaction event
	- a data record meant to be validated


* Operator: operator is a reusable comparison function used inside conditions:
	
	Supported Operators:
	- Equality: `eq, ne`
	- Comparison: `gt, gte, lt, lte`
	- Membership: `opt_in, not_in, contains, contains_any, contains_all`


* Core Engine: Core runtime engine that:
	- loads rules
	- evaluates each rule’s conditions
	- resolves matching rules
	- aggregates results
	- returns a list of RuleResult objects

# Usage Documentation

Installation:

1. `pip install`

2. Create an instance of the engine

3. Load rules, GenRulesEngine currently supports JSON documents

Supported JSON Rules Format Example
```
{
    "rules": [
        {
            "id": 1,
            "label": "Working Adult",
            "conditions": {
                "all": [
                    {
                        "field": "age",
                        "operator": ">",
                        "value": 18
                    },
                    {
                        "field": "age",
                        "operator": "<",
                        "value": 65
                    }
                ],
                "any": [
                    {
                        "field": "occupation",
                        "operator": "=",
                        "value": "engineer"
                    },
                    {
                        "field": "location",
                        "operator": "=",
                        "value": "wa"
                    }
                ]
            },
            "actions": [
                {
                    type: "gmail.update_label,
                    parameters: {
                        "label: "Jobs
                    }, 
                    order: 1
                },
                {
                    type: "gmail.send_email,
                    parameters: {
                        "snippet": "Updated Gmail Labels"
                    },
                    order: 0
                 }
            ],
            "depends_on": [2]
        },
        {
            "id": 2,
            "label": "Acknowledge Active User",
            "conditions": {
                "all": [
                    {
                        "field": "account.status",
                        "operator": "=",
                        "value": "active"
                    }
                ],
                "any": []
            },
            "actions": [
                {
                    "type": "notification_service.send_welcome_message"
                    "parameters": {
                        "field": "account.name"
                    },
                    "order": 0
                }
            ],
            "depends_on": []
        }
    ]
}

```

4. Call engine.run(context), where context is your information to evaluate




RuleResult Object Response Example:
```
[
    RuleResult(label='Acknowledge Active User', triggered=True, skipped=False), 
    RuleResult(label='Working Adult', triggered=True, skipped=False), RuleResult(label='Determine Eligible Residency', triggered=True, skipped=False), RuleResult(label='Login User', triggered=True, skipped=False)
]
```

# Testing
    uv run pytest tests

