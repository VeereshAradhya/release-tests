import re
import os
from pylero.work_item import TestCase
from pylero.exceptions import PyleroLibException
import argparse
import mistune
import yaml

# project id = VAradhyaExerciseAug30
# Testcase = P-01-TC02

parser = argparse.ArgumentParser()

parser.add_argument('--folder_path', type=str, help='path to the folder which contains test files',
                    required=True)

args = parser.parse_args()

folder_path = args.folder_path
extension = 'spec'

# get configs
with open('config.yaml') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(e)
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
        print('Invalid value for testcase_regex in config.yaml')
        raise Exception

field_name_api_regex = config['field_name_api_regex']


def extract_value(string, pattern):
    match = re.search(pattern, string)
    if match:
        return match.groups()[0], re.sub(pattern, '', string)
    return False, string


def create_or_update_test(test_case):
    test = re.match('.+', test_case)
    test_title = test.group(0)

    # Extract test case ID
    test_id = compiled_testcase_id.match(test_title)

    # If test case ID is present then only create/update tests
    if test_id:
        test_properties = {}
        test_id = test_id.groups()[0]
        # print('Found test case {}'.format(test_case))
        test_title = test_title.replace(': ' + test_id, '')

        # Extract test case properties
        for item in field_name_api_regex:
            match, test_case = extract_value(test_case, item['regex'])
            if match:
                match_updated = match.lower()
                if match_updated in ['true', 'yes']:
                    test_properties[item['field_name_api']] = True
                elif match_updated in ['false', 'no']:
                    test_properties[item['field_name_api']] = False
                else:
                    test_properties[item['field_name_api']] = match_updated
        description_list = test_case.split('\n')
        description_list = description_list[1:]
        description = ''
        for line in description_list:
            if line != '':
                description = description + line + '<br/>\n'
        test_properties['title'] = test_title
        test_properties['description'] = mistune.html(description)
        test_properties['desc'] = test_properties['description']

        # update automation status
        if 'manualonly' in test_properties['tags']:
            test_properties['caseautomation'] = 'manualonly'
        elif 'to-do' in test_properties['tags']:
            test_properties['caseautomation'] = 'notautomated'
        else:
            test_properties['caseautomation'] = 'automated'

        try:
            t = TestCase(project_id=project_id, work_item_id=test_id)
            for item in test_properties:
                setattr(t, item, test_properties[item])
            print('Updating test case {}'.format(test_id))
            t.update()
        except PyleroLibException:
            t = TestCase(project_id=project_id)
            print('Creating test case {}'.format(test_id))
            t.create(project_id=project_id, work_item_id=test_id, **test_properties)


for root, dirs, files in os.walk(folder_path):
    for name in files:
        if name.endswith(".{}".format(extension)):
            with open(os.path.join(root, name)) as f:
                content = f.read()
                testCases = content.split("## ")
                testCases = testCases[1:]
                for testCase in testCases:
                    create_or_update_test(testCase)
