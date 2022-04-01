from jsonschema.exceptions import ValidationError
import pytest

from schemas.predefined import *


@pytest.mark.parametrize(
    'schema, instance', [
        # Any
        (Any(), True),
        (Any(), 128),
        (Any(), 'example'),

        # Array
        (Array(), []),
        (Array(), [0, True, 'everything-in-the-array']),
        (Array(Float()), [1.01, 1.02, 1.03]),
        (Array(Int()), ['0', 1, '2', 3]),
        (Array(Int(), Bool()), [False, 1, '1']),
        (Array(Int(enum=['0'])), ['0']),
        (Array(Int(), minItems=1), [0, 1]),
        (Array(Int(), maxItems=3), [0, 1, 2]),
        (Array(Int(), minItems=2, maxItems=3), [0, 1, 2]),

        # ArrayStrict
        (ArrayStrict(Int(), Float(), Bool(), String(), maxItems=5), [0, 1.2, True, 'string']),

        # Bool
        (Bool(), True),

        # Date
        (Date(), '1970-01-01T00:00:00'),

        # Float
        (Float(), 3.141593),
        (Float(), 128),  # Ints are also floats

        # Int
        (Int(), 1),
        (Int(), '1'),  # Ints can also be saved as string

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
        # Array
        (Array(), {}),
        (Array(Int()), ['its-string-not-int']),
        (Array(Int(enum=[0])), [1]),
        (Array(Int(enum=[0])), [0, 1]),
        (Array(Int(), minItems=2), [0]),  # not-enough-elements-in-the-list, parameter minItems
        (Array(Int(), maxItems=1), [0, 1]),  # too-many-elements-in-the-list, parameter maxItems
        (Array(Int(), minItems=2, maxItems=3), [0]),
        (Array(Int(), minItems=2, maxItems=3), [0, 1, 2, 3]),

        # ArrayStrict
        (ArrayStrict({}), []),
        (ArrayStrict(Int(), Float(), Bool()), [1, 1.1, 'its-not-a-bool']),
        (ArrayStrict(Int(), Float(), Bool()), [1, 1.1, True, 'too-many-elements-in-the-list']),
        (ArrayStrict(Int(), Float(), String()), [1, 'not-enough-elements-in-the-list']),

        # Bool
        (Bool(), 0),
        (Bool(), 1),
        (Bool(), 'False'),
        (Bool(), 'True'),

        # Date
        (Date(), 128),
        (Date(), True),
        (Date(), '1970/01/01T00:00:00'),
        (Date(), '1970-01-01-00:00:00'),
        (Date(), '1970-01-01T00:64:00'),  # Too many minutes
        (Date(), '1970-01-32T00:64:00'),  # Too many days
        (Date(), '1970-13-01T00:64:00'),  # Too many months


        # Float
        (Float(), None),
        (Float(), True),
        (Float(), '3.141593'),

        # Int
        (Int(), True),
        (Int(), 3.141593),
        (Int(), 'example-string'),

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
