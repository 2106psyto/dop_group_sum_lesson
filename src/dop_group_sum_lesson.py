import argparse as ap
import datetime
import json
import os
from jinja2 import Environment, FileSystemLoader
from jsonschema import validate, ValidationError
from expence import aggregate_by_div


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

    with open(args.infile) as w:
        jj = json.load(w)

    try:
        now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        results = {'calcdate':now,'results':aggregate_by_div(jj)}
        template = get_html_template()
        parse_html = template.render(results)

        path = build_output_path('result.html')
        with open(path, 'w') as file:
            file.write(parse_html)

    except ValidationError:
        print('Input data is ill-formed')