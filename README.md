[![pg github](https://img.shields.io/badge/GitHub-pacog1994-181717.svg?style=flat&logo=github)](https://github.com/pacog1994)
[![python](https://img.shields.io/badge/Python-3.1.4-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

# About

**GenRulesEngine** is a lightweight, generic rules-engine abstraction designed to serve as a flexible skeleton for a wide range of rule-based use cases. It provides a consistent set of terminology and components—such as rules, rule sets, conditions, and actions—to improve clarity and maintainability across different implementations.

Like all rules engines, the goal of GenRulesEngine is to cleanly separate business logic (“rules”) from application code. All rules and rule sets are evaluated at runtime, and actions are triggered automatically when their conditions are met.


# Terminology

* Rule  
  A rule represents a single piece of business logic made up of:
	-  Conditions: Boolean expressions that must evaluate to true
	-  Actions: Functions or handlers when all conditions are satisfied 

* Condition  
	A condition is predicate that tests one or more inputs, evaluating to True or False
	
	Examples:
	-  `userole == "admin"`
	- `token.ttl = 400
	-   `order.total > 100 AND customer.age >= 18`

* Action  
	An action is an operation triggered when a rule's conditions pass
	
	Examples:
	- modifying a value
	- appending to a list
	- calling a callback
	- returning a decision allow/deny

* Rule Set  
	A rule set is a collection of rules evaluated together

* Input Data  
	Inputs are the runtime data objects passed into the engine during evaluation.
	
	Examples:
	- a client-server's or server-server's request payload
	- triggered transaction event
	- a data record meant to be validated

* Operator  
	An operator is a reusable comparison function used inside conditions
	 
	Supported Operators:
	- Equality: `eq, ne`
	- Comparison: `gt, gte, lt, lte`
	- Membership: `in, contains`

* Evaluation Engine  
	The core runtime engine that:
	- loads rule sets
	- evaluates each rule’s conditions
	- resolves matching rules
	- executes corresponding actions
	- aggregates results
	- returns a consistent decision object

* Decision  
	The final output of a rule set evaluation.
	
	Examples:
	- a decision, i.e. allow, deny, etc.
	- set of triggered actions results

# API Documentation
Subject-To-Change

`POST /genrulesengine/evaluate`

JSON-Formatted Body
```
{
  "ruleSet": "discountRules",
  "inputs": {
    "order": {
      "total": 150,
      "items": 3,
      "customerType": "regular"
    },
    "user": {
      "id": "12345",
      "isMember": true
    }
  },
  "options": {
    "stopOnFirstMatch": false,
    "includeRuleMetadata": true
  }
}
```

**Response:**  
200 OK: 

Minimal Response:
```
{
  "allow": true
}
```

Complex Response:
```
{
  "ruleSet": "discountRules",
  "evaluationId": "efb2c0c0-f509-4b16-9d8e-21d5a981be49",
  "results": {
    "triggeredRules": [
      {
        "id": "discount_10pct_large_order",
        "description": "Apply 10% discount for orders over $100",
        "conditionsPassed": true,
        "actionResult": {
          "discount": 0.10,
          "newTotal": 135
        }
      },
      {
        "id": "member_bonus_discount",
        "description": "Additional 5% off for members",
        "conditionsPassed": true,
        "actionResult": {
          "discount": 0.05,
          "newTotal": 128.25
        }
      }
    ],
    "finalOutput": {
      "totalDiscount": 0.15,
      "finalAmount": 128.25
    }
  },
  "metadata": {
    "ruleCount": 2,
    "evaluationTimeMs": 3
  }

```

500 Server Error:
```
{
  "error": {
    "code": "RULESET_NOT_FOUND",
    "message": "The specified ruleSet 'discountRules' does not exist.",
    "details": {
      "timestamp": "2025-02-14T12:45:30Z",
      "path": "/api/evaluate",
      "ruleSet": "discountRules",
      "evaluationId": "b18e8805-8d33-4b05-8a72-0980cb2732b7"
    }
  }
}
```



