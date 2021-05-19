from pylarion.work_item import TestCase
from pylarion.exceptions import PylarionLibException


def create_or_update_test(project_id, test_id, test_properties):
    try:
        t = TestCase(project_id=project_id, work_item_id=test_id, flush=True)
        for item in test_properties:
            setattr(t, item, test_properties[item])
        print('Updating test case {}'.format(test_id))
        t.update()
    except PylarionLibException:
        t = TestCase(project_id)
        print('Creating test case {}'.format(test_id), flush=True)
        t.create(project_id=project_id, work_item_id=test_id, **test_properties)
