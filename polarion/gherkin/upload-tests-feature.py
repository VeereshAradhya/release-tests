from gherkin.token_scanner import TokenScanner
from gherkin.parser import Parser
import re
from prettytable import PrettyTable
from utility import create_or_update_test
import yaml
import argparse
import ssl

# fix to certificate issue
ssl._create_default_https_context = ssl._create_unverified_context
parser = argparse.ArgumentParser()

parser.add_argument('--file_path', type=str, help='path to the folder which contains test files',
                    required=True)
args = parser.parse_args()
file_path = args.file_path

# get configs
with open('config.yaml') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(e, flush=True)
        raise Exception

# set project_id and test_id
project_id = config.get('project_id')
if not project_id:
    raise Exception('Please add file project_id in config.yaml')

testcase_regex = config.get('testcase_regex')
if not testcase_regex:
    raise Exception('Please add field testcase_regex in config.yaml with valid regex')
else:
    try:
        compiled_testcase_id = re.compile(r'{}'.format(testcase_regex))
    except re.error as e:
        print('Invalid value for testcase_regex in config.yaml', flush=True)
        raise Exception

token_scanner = TokenScanner(file_path)
'/home/varadhya/test-ui/console/frontend/packages/pipelines-plugin/integration-tests/features/pipelines/create-from-add-options.feature'
parser = Parser()
content = parser.parse(token_scanner)
# print(len(content['feature']['children'][2]['scenario']['examples'][0]['tableBody']))

for children in content['feature']['children'][1:]:
    tc_title = children['scenario']['name']
    tc_id = compiled_testcase_id.match(tc_title)
    tc_id = tc_id.groups()[0]
    if tc_id:
        test_properties = {}
        test_properties['tags'] = ','.join(map(lambda x: x['name'], children['scenario']['tags']))
        if '@to-do' in test_properties['tags']:
            test_properties['caseautomation'] = 'notautomated'
        elif '@manual' in test_properties['tags']:
            test_properties['caseautomation'] = 'manualonly'
        else:
            test_properties['caseautomation'] = 'automated'

        # set defaults
        defaults = config.get('defaults')
        if defaults:
            # print('inside defaults')
            for default in defaults:
                test_properties[default['field_name_api']] = default['value']
                # print(test_properties[default['field_name_api']])
        tc_title = re.sub(r':.+', '', tc_title).strip()
        tc_description = map(
            lambda x: '<li>{}{}</li>'.format(x['keyword'], (x['text'].replace('<', '&lt;')).replace('>', '&gt;')),
            children['scenario']['steps'])
        tc_description = '<ul>\n ' + '\n '.join(tc_description) + '\n</ul>'
        if children['scenario']['examples']:
            i = 1
            for example in children['scenario']['examples']:
                for table_body in example['tableBody']:
                    table = PrettyTable()
                    table.field_names = map(lambda x: x['value'], example['tableHeader']['cells'])
                    table.add_row(list(map(lambda x: x['value'], table_body['cells'])))
                    new_tc_id = '{}-{}'.format(tc_id, ('{}'.format(i)).zfill(2))
                    table = '<br/>\n'.join(table.get_string().split('\n'))
                    test_properties['title'] = tc_title
                    test_properties['desc'] = '{}<br/>\n{}'.format(tc_description, table)
                    test_properties['description'] = test_properties['desc']
                    create_or_update_test(project_id, new_tc_id, test_properties)
                    i = i + 1
        else:
            test_properties['title'] = tc_title
            test_properties['desc'] = tc_description
            test_properties['description'] = tc_description
            create_or_update_test('VAradhyaExerciseAug30', tc_id, test_properties)