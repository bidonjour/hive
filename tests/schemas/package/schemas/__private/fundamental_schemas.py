from typing import Any, Dict, List, Optional

import jsonschema


class Schema:
    def __init__(self, options: Dict[str, Any]):
        self._options = options

    def validate(self, instance) -> None:
        jsonschema.validate(
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
