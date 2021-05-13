import xml.etree.ElementTree as ET
import re
from pylarion.test_record import TestRecord
from pylarion.test_run import TestRun

location = '/home/varadhya/workspace/src/github.com/release-tests/reports/xml-report/result.xml'
tree = ET.parse(location)
test_suites = tree.getroot()
project_id = 'VAradhyaExerciseAug30'

# print(root.tag)
# print(root.attrib)
tr = TestRun.create(project_id=project_id, test_run_id='op_1_5_1', template='pipelines_1_5-template', title='OPS-1.5-1')
tr.status = 'inprogress'

for test_suite in test_suites:
    for item in test_suite:
        if item.tag == 'testcase':
            # print(item.attrib['name'])
            test_id_match = re.match(r".+:\s*(P-\d+-TC\d+)", item.attrib['name'])
            if test_id_match:
                test_id = test_id_match.groups()[0]
                test_record = TestRecord(project_id=project_id, test_case_id=test_id)
                if len(item) > 0:
                    test_record.comment = item[0].attrib['message']
                    test_record.result = 'failed'
                    print('{}: failed'.format(test_id))
                else:
                    test_record.result = 'passed'
                    print('{}: passed'.format(test_id))
                tr.add_test_record_by_object(test_record)
