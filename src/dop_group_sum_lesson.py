import argparse as ap
import json
import os
from jinja2 import Environment, FileSystemLoader
from jsonschema import validate, ValidationError
import pydash as _


def aggregate_by_div(divs):
    aggregated = _.group_by(divs, ['div_code'])
    sum_by_div = _.map_(aggregated,
                lambda o, k:
                    {
                        'div_code': k,
                        'actual': _.sum_by(o, ['actual']),
                        'planned': _.sum_by(o, ['plan'])
                    })
    return sum_by_div

def get_html_template():
    env = Environment(loader=FileSystemLoader('./templates'), autoescape = True)
    return env.get_template('page.html')

def build_output_path(filename):
    build_dir = 'dist'
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)
    return os.path.join(build_dir, filename)


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('infile', help='Input JSON file')
    args = parser.parse_args()

    with open(os.path.join(os.getcwd(),'src', 'input_data_schema.json')) as schema_file:
        schema = json.load(schema_file)

    with open(args.infile) as w:
        jj = json.load(w)

    try:
        validate(instance=jj, schema=schema)
        import datetime
        now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        results = {'calcdate':now,'results':aggregate_by_div(jj)}
        template = get_html_template()
        parse_html = template.render(results)

        path = build_output_path('result.html')
        with open(path, 'w') as file:
            file.write(parse_html)

    except ValidationError:
        print('Input data is ill-formed')