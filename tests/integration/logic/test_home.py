from tests.base_test import BaseTest


class TestHomePageResponseDataPreparation(BaseTest):
    # TODO: test cases
    """
    test for simple home page (without args)
    test for filtered by search
    test for filtered by category
    test for filtered by subject

    All tests should call 'NoteModel.get_all_visible'
    assert called some function (depends on filter type)
    ResponseData.resource should has only notes visible for data.context.person_visibility
    """
    pass

