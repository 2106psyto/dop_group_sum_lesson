import pydash as _
import json
from jinja2 import Environment, FileSystemLoader
import os


def aggregate_by_div(divs):
    aggregated = _.group_by(divs, ['div_code'])
    sum_by_div = _.map_(aggregated,
                lambda o, k: {
                    'div_code': k,
                    'actual': _.sum_by(o, ['actual']),
                    'planned': _.sum_by(o, ['plan'])})
    return sum_by_div


if __name__ == '__main__':
    import argparse as ap

    parser = ap.ArgumentParser()
    parser.add_argument('infile', help='Input JSON file')
    args = parser.parse_args()

    env = Environment(loader=FileSystemLoader('./templates'), autoescape = True)
    template = env.get_template('page.html')

    build_dir = 'dist'
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)

    with open(args.infile) as w:
        jj = json.load(w)

    results = aggregate_by_div(jj)
    print(results)
    data = {'results':results}
    parse_html = template.render(data)

    path = F'{build_dir}/result.html'
    with open(path, 'w') as file:
        file.write(parse_html)