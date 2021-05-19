import json
import re
from pylarion.exceptions import PylarionLibException
from pylarion.test_record import TestRecord
from pylarion.test_run import TestRun
import argparse
import ssl
import yaml

# fix to certificate issue
ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser()

parser.add_argument('--path_to_report', type=str, help='path to xml report',
                    required=True)
parser.add_argument('--testrun-template-id', type=str, help='testrun template id', required=True)
parser.add_argument('--build_number', type=str, help='build number of the operator', required=True)
# parser.add_argument('--milestone_id', type=str, help='Milestone ID of the release plan', required=True)
parser.add_argument('--testrun_name_prefix', type=str, help='testrun name prefix', required=True)

args = parser.parse_args()
path_to_report = args.path_to_report
build_number = args.build_number
testrun_template_id = args.testrun_template_id
testrun_name_prefix = args.testrun_name_prefix

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
# Create/Get testrun
try:
    tr = TestRun(project_id=project_id, test_run_id=test_run_id)
    print('Getting testrun {}'.format(test_run_id), flush=True)
except PylarionLibException:
    print('Creating testrun {}'.format(test_run_id), flush=True)
    tr = TestRun.create(project_id=project_id, test_run_id=test_run_id, template=testrun_template_id)

tr.status = 'inprogress'
tr.build = build_number

with open(path_to_report) as f:
    data = json.load(f)
tc_regex = r'(P-\d+-TC\d+)'
example_regex = r'example #(\d+)'
for result in data['results']:
    for suite in result['suites']:
        for test in suite['tests']:
            match = re.search(tc_regex, test['title'])
            tc_id = match.groups()[0]
            example = re.search(example_regex, test['title'])
            if example:
                example_number = example.groups()[0]
                tc_id = '{}-{}'.format(tc_id, ('{}'.format(example_number)).zfill(2))
            if test['state'] != 'pending':
                if test['state'] == 'passed':
                    tc_rec = TestRecord(project_id=project_id, test_case_id=tc_id)
                    tc_rec.result = test['state']
                    print('Updating result of {} as passed'.format(tc_id), flush=True)
                elif test['state'] == 'failed':
                    tc_rec = TestRecord(project_id=project_id, test_case_id=tc_id)
                    tc_rec.result = test['state']
                    tc_rec.comment = test['err']['message']
                    print('Updating result of {} as failed'.format(tc_id), flush=True)
                tr.update_test_record_by_object(test_case_id=tc_id, test_record=tc_rec)
