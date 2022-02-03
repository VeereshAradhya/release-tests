import ssl

# fix to certificate issue
ssl._create_default_https_context = ssl._create_unverified_context


from pylero.work_item import TestCase
from pylero.exceptions import PyleroLibException


def create_or_update_test(project_id, test_id, test_properties):
    try:
        t = TestCase(project_id=project_id, work_item_id=test_id)
        for item in test_properties:
            setattr(t, item, test_properties[item])
        print('Updating test case {}'.format(test_id), flush=True)
        t.update()
    except PyleroLibException:
        t = TestCase(project_id)
        print('Creating test case {}'.format(test_id), flush=True)
        t.create(project_id=project_id, work_item_id=test_id, **test_properties)
