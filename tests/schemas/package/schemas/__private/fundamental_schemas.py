from typing import Any, Dict, List, Optional

from schemas.__private import custom_validate


class Schema:
    def __init__(self, options: Dict[str, Any]):
        self._options = options

    def validate(self, instance) -> None:
        custom_validate.custom_validate(
            instance=instance,
            schema=self._create_schema(),
        )

    def _create_core_of_schema(self) -> Dict[str, Any]:
        """
        This function create the core of the schema. Core is not a complete schema, it can't be validated.
        To passed validation, _create_schema adds basic schema parts and optional parameters (e.g 'enum', 'minItems'),
        creating a complete schema prepared for validation.
        """
        raise NotImplemented

    def _create_schema(self) -> Dict[str, Any]:
        return {**self._create_core_of_schema(), **self._options}


class Any_(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_core_of_schema(self) -> Dict[str, Any]:
        return {}


class Array(Schema):
    def __init__(self, *items, unique_items: bool = False, **options: Any):
        super().__init__(options)
        self.__items = list(items)
        self.__unique_items = unique_items

    def _create_core_of_schema(self) -> Dict[str, Any]:
        items_as_list = []
        for schema in self.__items:
            if isinstance(schema, Schema):
                items_as_list.append(schema._create_schema())
        if len(items_as_list) > 1:
            return {
                'type': 'array',
                'items': {
                    'oneOf': items_as_list
                },
                'uniqueItems': self.__unique_items,
            }
        elif len(items_as_list) == 0:
            return {
                'type': 'array',
            }
        return {
            'type': 'array',
            'items': items_as_list[0],
            'uniqueItems': self.__unique_items,
        }


class ArrayStrict(Schema):
    def __init__(self, *prefix_items, unique_items: bool = False, **options: Any):
        """ArrayStrict is useful when the array is a collection of items,
        where each has a different schema and the ordinal index of each item is meaningful."""
        super().__init__(options)
        self.__prefix_items = list(prefix_items)
        self.__unique_items = unique_items

    def _create_core_of_schema(self) -> Dict[str, Any]:
        prefix_items_as_list = self.__prefix_items
        for index, schema in enumerate(prefix_items_as_list):
            if isinstance(schema, Schema):
                prefix_items_as_list[index] = schema._create_schema()

        return {
            'type': 'array',
            'prefixItems': prefix_items_as_list,
            'uniqueItems': self.__unique_items,
            "minItems": len(prefix_items_as_list),
            'maxItems': len(prefix_items_as_list),
        }


class Bool(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_core_of_schema(self) -> Dict[str, Any]:
        return {'type': 'boolean'}


class Float(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_core_of_schema(self) -> Dict[str, Any]:
        return {'type': 'number'}


class Int(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_core_of_schema(self) -> [str, Any]:
        return {
            'anyOf': [
                {'type': 'integer'},
                {'type': 'string', 'pattern': r'^\d+$'},
            ]
        }


class Null(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_core_of_schema(self) -> Dict[str, Any]:
        return {'type': 'null'}


class Map(Schema):
    def __init__(self, properties: Dict, required_keys: Optional[List[str]] = None,
                 allow_additional_properties: bool = False, **options: Any):
        """
        :param properties: A set of rules included in the schema. Takes dictionary (key-value) values.
        key: -> key in schema, value: -> rule of key.
        :param required_keys: It takes the form of a list.
        The list should include the keys that are required for valid validation.
        :param allow_additional_properties: By default, all keys are required.
        Additional number of keys will lead to incorrect validation,
        unless you use the `allow_additional_properties parameter`.
        Takes the value of True, False. It allows for successful validation of keys,
        that are not included in the schema.
        :param options: Other options that can be given in the form of a dictionary
        """
        super().__init__(options)
        self.__allow_additional_properties: bool = allow_additional_properties
        self.__properties = properties
        self.__required_keys: List[str] = list(self.__properties.keys()) if required_keys is None else required_keys

    def _create_core_of_schema(self) -> Dict[str, Any]:
        properties_as_dicts = self.__properties.copy()
        for key, schema in self.__properties.items():
            if isinstance(schema, Schema):
                properties_as_dicts[key] = schema._create_schema()
        return {
            'type': 'object',
            'properties': properties_as_dicts,
            'required': self.__required_keys,
            'additionalProperties': self.__allow_additional_properties
        }


class String(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_core_of_schema(self) -> Dict[str, Any]:
        return {'type': 'string'}
