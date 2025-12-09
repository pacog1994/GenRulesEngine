import json

from genrulesengine.models.conditions.conditions import Condition
from genrulesengine.models.rule import Rule
""" Supported Rules Engine config file
{
    "rules": [{
        // metadata support ---------------
        "id",
        "label",
        "description",
        "version",
        "priority",
        ...,
        //--------------------
        "conditions": {
            "any": [
                        {
                            "field": "",
                            "operator": "",
                            "value": ""
                        },
                        {...}
                    ],
            "all": [
                        {...}
                   ]
        },
        "actions": ["", "..."]
    }, {...}],
    // do later alongside metadata ------------------------------------
    "ruleset": {
        ....   
    }
    // do later -------------------------------------
    "options": {
    
    }
}
"""

""" Supported Rules Engine input file
    
"""

txt = ('{"rules": [{"id": 1, "label": "Working Adult", "conditions":['
       '{"any": [{"field":"age", "operator": ">", "value": 18}, {"field":"age", "operator": "<", "value": 65}], '
       '"all": [{"field":"occupation", "operator":"=", "value": "false"}, {"field":"location", "operator":"=", "value": "wa"}]}],'
       ' "actions": ["approve"]}]}')

python_object = json.loads(txt)

# print(python_object["rules"][0]["conditions"][0]["all"])

python_object["rules"]

json_output_string = json.dumps(python_object, indent=4)

print(json_output_string)

rules = python_object["rules"]

for rule in rules:
    label = rule["label"]
    conditions = rule["conditions"]
    list_condition = []
    for condition in conditions:
        field = condition["any"][0]["field"]
        operator = condition["all"][0]["operator"]
        value = condition["all"][0]["value"]
        list_condition.append(Condition(field, operator, value))
    newRule = Rule(label, list_condition, rule["actions"])
    print(newRule)



# we want to parse the json into rules and then use internal rules class



