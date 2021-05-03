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


def create_or_update_test(testCase):
	testProperties = {}
	test = re.match('.+', testCase)
	testTitle = test.group(0)

	# Extract test case ID
	testID = re.match(r".+:\s*(P-\d+-TC\d+)", testTitle)

	# If test case ID is present then only create/update tests
	if testID:
		testID = testID.groups()[0]
		testTitle = testTitle.replace(': ' + testID, '')
		description = testCase.split('\n')
		description = description[1:]
		for i in range(len(description)):
			description[i] = description[i].strip()
			tags = re.match(r'^Tags: (.+)', description[i])
			if tags:
				tags = tags.groups()
				testProperties['tags'] = tags
				if 'not-automated' in tags:
					testProperties['caseautomation'] = 'notautomated'
				elif 'manual-only' in tags:
					testProperties['caseautomation'] = 'manualonly'
				else:
					testProperties['caseautomation'] = 'automated'
				description[i] = ''
		description = "<br/>\n".join(description)
		testProperties['title'] = testTitle
		testProperties['desc'] = description
		testProperties['description'] = description

		try:
			t = TestCase(project_id=projectID, work_item_id=testID)
			for item in testProperties:
				setattr(t, item, testProperties[item])
			print('Updating test case {}'.format(testID))
			t.update()
		except PylarionLibException:
			t = TestCase(projectID)
			print('Creating test case {}'.format(testID))
			t.create(project_id=projectID, work_item_id=testID, **testProperties)



for root, dirs, files in os.walk(folder_path):
	for name in files:
		if name.endswith(".{}".format(extension)):
			with open(os.path.join(root, name)) as f:
				content = f.read()
				testCases = content.split("## ")
				testCases = testCases[1:]
				for testCase in testCases:
					create_or_update_test(testCase)
					