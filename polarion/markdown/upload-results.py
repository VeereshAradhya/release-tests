import xml.etree.ElementTree as ET
import re

from pylarion.exceptions import PylarionLibException
from pylarion.test_record import TestRecord
from pylarion.test_run import TestRun
import argparse
import yaml
import ssl

# fix to certificate issue
ssl._create_default_https_context = ssl._create_unverified_context

# project_id = 'VAradhyaExerciseAug30'
parser = argparse.ArgumentParser()

parser.add_argument('--path_to_xml_report', type=str, help='path to xml report',
                    required=True)
parser.add_argument('--testrun-template-id', type=str, help='testrun template id', required=True)
parser.add_argument('--build_number', type=str, help='build number of the operator', required=True)
parser.add_argument('--milestone_id', type=str, help='Milestone ID of the release plan', required=True)
parser.add_argument('--testrun_name_prefix', type=str, help='testrun name prefix', required=True)
location = '/home/varadhya/workspace/src/github.com/release-tests/reports/xml-report/result.xml'

args = parser.parse_args()

xml_report_location = args.path_to_xml_report
build_number = args.build_number
testrun_template_id = args.testrun_template_id
testrun_name_prefix = args.testrun_name_prefix
milestone_id = args.milestone_id

tree = ET.parse(location)
test_suites = tree.getroot()
test_run_id = '{}-{}'.format(testrun_name_prefix, build_number)

# get configs
with open('config.yaml') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(e)

# validate project_id
project_id = config.get('project_id')
if not project_id:
    raise Exception('Please add file project_id in config.yaml')

# validate testcase_regex
testcase_regex = config.get('testcase_regex')
if not testcase_regex:
    raise Exception('Please add field testcase_regex in config.yaml with valid regex')
else:
    try:
        compiled_testcase_id = re.compile(r'{}'.format(testcase_regex))
    except re.error as e:
        print('Invalid value for testcase_regex in config.yaml')
        raise Exception

# Create/Get testrun
try:
    tr = TestRun(project_id=project_id, test_run_id=test_run_id)
except PylarionLibException:
    tr = TestRun.create(project_id=project_id, test_run_id=test_run_id, template=testrun_template_id)

# mark testrun status to in progress
tr.status = 'inprogress'
tr.build = build_number
tr.plannedin = milestone_id
# tr.update()

for test_suite in test_suites:
    for item in test_suite:
        if item.tag == 'testcase':
            # print(item.attrib['name'])
            test_id_match = compiled_testcase_id.match(item.attrib['name'])
            if test_id_match:
                test_id = test_id_match.groups()[0]
                try:
                    test_record = TestRecord(project_id=project_id, test_case_id=test_id)
                    if len(item) > 0:
                        test_record.comment = item[0].attrib['message']
                        test_record.result = 'failed'
                        print('{}: failed'.format(test_id))
                    else:
                        test_record.result = 'passed'
                        print('{}: passed'.format(test_id))
                    tr.update_test_record_by_object(test_case_id=test_id, test_record=test_record)
                except PylarionLibException:
                    print('Test case {} not found'.format(test_id))
