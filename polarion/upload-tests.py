import re
import os
from pylarion.work_item import TestCase
from pylarion.exceptions import PylarionLibException
import argparse

# project id = VAradhyaExerciseAug30
# Testcase = P-01-TC02

parser = argparse.ArgumentParser()

parser.add_argument('--folder_path', type=str, help='path to the folder which contains test files',
                    required=True)
parser.add_argument('--file_extension', type=str, help='Extension of the test file', required=True)
parser.add_argument('--project_ID', type=str, help='Project ID of the project', required=True)

args = parser.parse_args()

folder_path = args.folder_path
extension = args.file_extension
projectID = args.project_ID

field_name_api_regex = [{'field_name_ui': 'Level', 'regex': r'Level: (.+)', 'field_name_api': 'caselevel'},
                        {'field_name_ui': 'Component', 'regex': r'Component: (.+)', 'field_name_api': 'casecomponent'},
                        {'field_name_ui': 'Subcomponent', 'regex': r'Subcomponent: (.+)',
                         'field_name_api': 'subcomponent'},
                        {'field_name_ui': 'CustomerScenario', 'regex': r'CustomerScenario: (.+)',
                         'field_name_api': 'customerscenario'},
                        {'field_name_ui': 'Multi-ProductCustomerScenario',
                         'regex': r'Multi-ProductCustomerScenario: (.+)',
                         'field_name_api': 'multiproduct'},
                        {'field_name_ui': 'Type', 'regex': r'Type: (.+)', 'field_name_api': 'testtype'},
                        {'field_name_ui': 'Subtype1', 'regex': r'Subtype1: (.+)', 'field_name_api': 'subtype1'},
                        {'field_name_ui': 'Subtype2', 'regex': r'Subtype2: (.+)', 'field_name_api': 'subtype2'},
                        {'field_name_ui': 'LegacyTestCase', 'regex': r'LegacyTestCase: (.+)',
                         'field_name_api': 'legacytest'},
                        {'field_name_ui': 'Pos/Neg', 'regex': r'Pos/Neg: (.+)', 'field_name_api': 'caseposneg'},
                        {'field_name_ui': 'Importance', 'regex': r'Importance: (.+)',
                         'field_name_api': 'caseimportance'},
                        {'field_name_ui': 'Automation', 'regex': r'Automation: (.+)',
                         'field_name_api': 'caseautomation'},
                        {'field_name_ui': 'Upstream', 'regex': r'Upstream: (.+)', 'field_name_api': 'upstream'},
                        {'field_name_ui': 'CasePositiveOrNegative', 'regex': r'CasePositiveOrNegative: (.+)',
                         'field_name_api': 'caseposneg'},
                        {'field_name_ui': 'Tags', 'regex': r'Tags: (.+)', 'field_name_api': 'tags'},
                        ]


def extract_value(string, pattern):
    match = re.search(pattern, string)
    if match:
        return match.groups()[0], re.sub(pattern, '', string)
    return False, string


def create_or_update_test(test_case):
    test = re.match('.+', test_case)
    test_title = test.group(0)

    # Extract test case ID
    test_id = re.match(r".+:\s*(P-\d+-TC\d+)", test_title)

    # If test case ID is present then only create/update tests
    if test_id:
        test_properties = {}
        test_id = test_id.groups()[0]
        print('Found test case {}'.format(test_case))
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
        test_properties['desc'] = description
        test_properties['description'] = description

        try:
            t = TestCase(project_id=projectID, work_item_id=test_id)
            for item in test_properties:
                setattr(t, item, test_properties[item])
            print('Updating test case {}'.format(test_id))
            t.update()
        except PylarionLibException:
            t = TestCase(projectID)
            print('Creating test case {}'.format(test_id))
            t.create(project_id=projectID, work_item_id=test_id, **test_properties)


for root, dirs, files in os.walk(folder_path):
    for name in files:
        if name.endswith(".{}".format(extension)):
            with open(os.path.join(root, name)) as f:
                content = f.read()
                testCases = content.split("## ")
                testCases = testCases[1:]
                for testCase in testCases:
                    create_or_update_test(testCase)
