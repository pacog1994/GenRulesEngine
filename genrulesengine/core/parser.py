from dataclasses import dataclass
from typing import Any, Dict

from genrulesengine.models.conditions.condition import Condition, ConditionGroup, ConditionTree
from genrulesengine.models.rules.rule import Rule

@dataclass
class Parser:
    def parse_condition(self, data: Dict[str, Any]) -> Condition:
        try:
           return Condition(
               field=data["field"],
               operator=data["operator"],
               value=data["value"]
           )
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")

    def parse_condition_group(self, data: Dict[str, Any]) -> ConditionGroup:
        try:
            return ConditionGroup(
                all=[self.parse_node(node) for node in data.get("all", [])],
                any=[self.parse_node(node) for node in data.get("any", [])]
            )
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")

    def parse_node(self, data: Dict[str, Any]):
        if "field" in data:
            return self.parse_condition(data)
        return self.parse_condition_group(data)

    def parse_condition_tree(self, data: Dict[str, Any]) -> ConditionTree:
        try:
            return ConditionTree(root=self.parse_condition_group(data["conditions"]))
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")

    def parse_rule(self, lookup: Dict[str, int], data: Dict[str, Any]) -> Rule:
        """
        Parse data into internal Rule representation.
        :param lookup: dependency labels that are mapped to ids for internal use
        :param data: Rule Object
        :return: The Rule Class Object
        """
        try:
            # create an array of ids that the rule depends on based off labels
            dep_ids = []
            deps_labels = data.get("depends_on", [])
            for label in deps_labels:
                label = label.strip().lower()
                if label not in lookup:
                    raise ValueError(
                        f"Rule '{data["label"]}' depends on unknown rule '{label}'"
                    )
                dep_ids.append(lookup[label])


            return Rule(
                id=data["id"],
                label=data["label"],
                conditions=self.parse_condition_tree(data),
                action_names=data["actions"],
                depends_on=dep_ids
            )
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")

    def parse_rules(self, data: Dict[str, Any]) -> list[Rule]:
        """
        Parse Rules into a list of internal Rule Objects
        :param data: Rules Object
        :return: An array of rules
        """
        try:
            # construct dependency lookup table
            deps_label_to_id = {}
            for rule in data["rules"]:
                label = rule["label"].strip().lower()
                if label in deps_label_to_id:
                    raise ValueError(f"Duplicate rule label detected: '{label}'")
                deps_label_to_id[label] =  rule["id"]

            return list([self.parse_rule(deps_label_to_id, rule) for rule in data["rules"]])
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")



