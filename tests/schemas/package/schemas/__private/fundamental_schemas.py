from typing import Any, Dict

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


class String(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_core_of_schema(self) -> Dict[str, Any]:
        return {'type': 'string'}
