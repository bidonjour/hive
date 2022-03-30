import jsonschema

from schemas.__private.custom_checkers import datetime_checker


def custom_validate(schema, instance):
    """
    It allows to add your own types. To do this you should extend `definitions`,
    with another dictionary key-value. Where key is the name of the new type,
    and value is a `checker` function. Checker should return True, False depending on the expected result.
    """
    default_validator = jsonschema.validators.validator_for({})
    # Build a new type checkers
    custom_types = default_validator.TYPE_CHECKER.redefine_many(
        definitions={
            'date': datetime_checker.check_date,
        })
    # Build a validator with the new type checkers
    custom_validator = jsonschema.validators.extend(default_validator, type_checker=custom_types)
    # Run the new Validator
    custom_validator(schema=schema).validate(instance)
