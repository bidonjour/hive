from jsonschema.exceptions import ValidationError
import pytest

from schemas.predefined import *


@pytest.mark.parametrize(
    'schema, instance', [
        # Any
        (Any(), True),
        (Any(), 128),
        (Any(), 'example'),

        # Bool
        (Bool(), True),

        # Float
        (Float(), 3.141593),
        (Float(), 128),  # Ints are also floats

        # Map
        (Map({}), {}),
        (Map({'k1': String(), 'k2': Float()}), {'k1': '1', 'k2': 1}),
        (Map({'k1': Map({'k2': Map({'k3': Bool()})})}), {'k1': {'k2': {'k3': False}}}),  # Nested mapping
        (Map({
            'name': String(),
            'email': String(),
            'telephone': Float()},
             required_keys=['name', 'email']),
         {
             'name': 'Josh',
             'email': "josh@josh.com",
             'telephone': 12.12
         }),
        (Map({'key-0': String()},
             allow_additional_properties=True),
         {
             'key-0': '0',
             'key-1': 1,
         }),
        (Map({'key-0': String()},
             required_keys=['key-0'],
             allow_additional_properties=True),
         {
             'key-0': '0',
             'key-1': 1,
         }),

        # Null
        (Null(), None),

        # String
        (String(), 'example-string'),
        (String(minLength=3), '012'),
    ]
)
def test_validation_of_correct_type(schema, instance):
    schema.validate(instance)


@pytest.mark.parametrize(
    'schema, instance', [
        # Bool
        (Bool(), 0),
        (Bool(), 1),
        (Bool(), 'False'),
        (Bool(), 'True'),

        # Float
        (Float(), None),
        (Float(), True),
        (Float(), '3.141593'),

        # Map
        (Map({}), 5),
        (Map({'key-0': String()}), 1),
        (Map({'key-0': String()}), 'example-string'),
        (Map({'key-0': String()}), {'key-0': 1}),
        (Map({'key-0': String()}), {'key-0': '0', 'key-1': '1'}),  # The number of keys does not match
        (Map({
            'name': String(),
            'email': String(),
            'telephone': Float()},
            required_keys=['name', 'email', 'telephone']),
         {
             'name': 'Josh',
             'email': "josh@josh.com",
         }),  # One of the required_keys 'telephone', is not included in the instance
        (Map({'key-0': String()},
             required_keys=['key-0'],
             ),
         {
             'key-0': '0',
             'key-1': 1,
         }),  # The schema does not allow the addition of keys not included in the schema

        # Null
        (Null(), 0),
        (Null(), ''),

        # String
        (String(), 1),
        (String(minLength=3), ''),
    ]
)
def test_validation_of_incorrect_type(schema, instance):
    with pytest.raises(ValidationError):
        schema.validate(instance)
