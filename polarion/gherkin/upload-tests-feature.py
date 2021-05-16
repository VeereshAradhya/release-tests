from gherkin.token_scanner import TokenScanner
from gherkin.parser import Parser
import re
from prettytable import PrettyTable
from utility import create_or_update_test

token_scanner = TokenScanner(
    '/home/varadhya/workspace/src/github.com/console/frontend/packages/pipelines-plugin/integration-tests/features/pipelines/create-from-add-options.feature')
parser = Parser()
content = parser.parse(token_scanner)
# print(len(content['feature']['children'][2]['scenario']['examples'][0]['tableBody']))

for children in content['feature']['children'][1:]:
    tc_title = children['scenario']['name']
    tc_id = re.search(r'P-\d+-TC\d+', tc_title)
    tc_id = tc_id.group(0)
    if tc_id:
        test_properties = {}
        tc_title = re.sub(r':.+', '', tc_title).strip()
        tc_description = map(lambda x: '<li>{}{}</li>'.format(x['keyword'], x['text']), children['scenario']['steps'])
        tc_description = '<ul>\n ' + '\n '.join(tc_description) + '\n</ul>'
        if children['scenario']['examples']:
            i = 1
            for example in children['scenario']['examples']:
                for table_body in example['tableBody']:
                    table = PrettyTable()
                    table.field_names = map(lambda x: x['value'], example['tableHeader']['cells'])
                    table.add_row(list(map(lambda x: x['value'], table_body['cells'])))
                    # table.field_names = heading/
                    # table.add_row(list(values))
                    # print(tc_title, '{}-{}'.format(tc_id, ('{}'.format(i)).zfill(2)))
                    # print(tc_description)
                    # # print(list(header))
                    # # print(list(l))
                    # print(table)
                    # print('\n')
                    # i = i+1
                    new_tc_id = '{}-{}'.format(tc_id, ('{}'.format(i)).zfill(2))
                    table = '<br/>\n'.join(table.get_string().split('\n'))
                    tc_description.replace('<', '&lt;')
                    tc_description.replace('>', '&gt;')
                    test_properties['title'] = tc_title
                    test_properties['desc'] = '{}<br/>\n{}'.format(tc_description, table)
                    test_properties['description'] = test_properties['desc']
                    create_or_update_test('VAradhyaExerciseAug30', new_tc_id, test_properties)
                    i = i+1
        else:
            # print(tc_title, tc_id)
            # print(tc_description)
            # print('\n')

            test_properties['title'] = tc_title
            test_properties['desc'] = tc_description
            test_properties['description'] = tc_description
            create_or_update_test('VAradhyaExerciseAug30', tc_id, test_properties)
