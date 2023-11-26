# -*- coding: utf-8 -*-
import json
import os
from jsonschema import validate, ValidationError
import pydash as _


def aggregate_by_div(divs):
    schema_file_dir = os.path.dirname(__file__)
    with open(os.path.join(schema_file_dir, 'input_data_schema.json')) as schema_file:
        schema = json.load(schema_file)
        validate(instance=divs, schema=schema)

    aggregated = _.group_by(divs, ['div_code'])
    sum_by_div = _.map_(aggregated,
                lambda o, k:
                    {
                        'div_code': k,
                        'actual': _.sum_by(o, ['actual']),
                        'planned': _.sum_by(o, ['plan'])
                    })
    return sum_by_div
