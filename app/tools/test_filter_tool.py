import unittest
from app.tools.filter_tool import FilterTool

class FilterToolTest(unittest.TestCase):

    def test_and_condition(self):
        search_filter = FilterTool({'$filter':{'id':1234}})

        self.assertTrue(search_filter.match({'id': 1234}))

    def test_fail_and_condition(self):
        search_filter = FilterTool({'$filter':{'id':1234}})

        self.assertFalse(search_filter.match({'id': 12345}))

    def test_fail_and_condition_by_missing(self):
        search_filter = FilterTool({'$filter':{'id':1234}})

        self.assertFalse(search_filter.match({'some': 12345}))

    def test_multiple_and_conditions(self):
        search_filter = FilterTool({'$filter': {'first_name':'fn', 'last_name':'ln'}})

        self.assertTrue(search_filter.match({'id': 1234, 'first_name': 'fn', 'last_name': 'ln'}))

    def test_fail_multiple_and_conditions(self):
        search_filter = FilterTool({'$filter': {'first_name':'fn', 'last_name':'ln'}})

        self.assertFalse(search_filter.match({'id': 1234, 'first_name': 'fn', 'last_name': 'ln2'}))

    def test_in_condition(self):
        search_filter = FilterTool({'$filter': {'id': [12, 13, 14]}})

        self.assertTrue(search_filter.match({'id': 13}))

    def test_fail_in_condition(self):
        search_filter = FilterTool({'$filter': {'id': [12, 13, 14]}})

        self.assertFalse(search_filter.match({'id': 15}))

    def test_or_condition(self):
        search_filter = FilterTool({'$filter': [{'id': 15}, {'first_name': 'fn'}]})

        self.assertTrue(search_filter.match({'first_name': 'fn'}))

    def test_fail_or_condition(self):
        search_filter = FilterTool({'$filter': [{'id': 15}, {'first_name': 'fn'}]})

        self.assertFalse(search_filter.match({'first_name': 'fn2'}))

    def test_fail_or_condition_by_missing(self):
        search_filter = FilterTool({'$filter': [{'id': 15}, {'first_name': 'fn'}]})

        self.assertFalse(search_filter.match({'last_name': 'ln'}))

    def test_inner_or_filter_condition(self):
        search_filter = FilterTool({'$filter': {'first_name': 'fn', '$filter': [{'last_name': 'ln'}, {'address': 'somewhere'}]}})

        self.assertTrue(search_filter.match({'first_name': 'fn', 'last_name': 'ln2', 'address': 'somewhere'}))

    def test_fail_inner_or_filter_condition(self):
        search_filter = FilterTool({'$filter': {'first_name': 'fn', '$filter': [{'last_name': 'ln'}, {'address': 'somewhere'}]}})

        self.assertFalse(search_filter.match({'first_name': 'fn', 'last_name': 'ln2', 'address': 'somewhere2'}))

    def test_inner_and_filter_condition(self):
        search_filter = FilterTool({'$filter': [{'first_name': 'fn'}, {'$filter': {'last_name': 'ln', 'address': 'somewhere'}}]})

        self.assertTrue(search_filter.match({'last_name': 'ln', 'address': 'somewhere'}))

    def test_fail_inner_and_filter_condition(self):
        search_filter = FilterTool({'$filter': [{'first_name': 'fn'}, {'$filter': {'last_name': 'ln', 'address': 'somewhere'}}]})

        self.assertFalse(search_filter.match({'last_name': 'ln2', 'address': 'somewhere2'}))

    def test_inner_dict_exists_field(self):
        search_filter = FilterTool({'$filter': {'first_name': {'$exists': True}}})

        self.assertTrue(search_filter.match({'first_name': 'John', 'last_name': 'Doe'}))

    def test_inner_dict_doesnt_exists_field(self):
        search_filter = FilterTool({'$filter': {'first_name1': {'$exists': True}}})

        self.assertFalse(search_filter.match({'first_name': 'John', 'last_name': 'Doe'}))

    def test_inner_dict_not_exists_field(self):
        search_filter = FilterTool({'$filter': {'first_name1': {'$exists': False}}})

        self.assertTrue(search_filter.match({'first_name': 'John', 'last_name': 'Doe'}))

    def test_inner_dict_doesnt_not_exists_field(self):
        search_filter = FilterTool({'$filter': {'first_name': {'$exists': False}}})

        self.assertFalse(search_filter.match({'first_name': 'John', 'last_name': 'Doe'}))

    def test_comparison_successfull(self):
        search_filter = FilterTool({'$filter': {'age': {'$gt': 40}}})

        self.assertTrue(search_filter.match({'id': 15, 'age': 50}))

    def test_fail_comparison(self):
        search_filter = FilterTool({'$filter': {'age': {'$lt': 40}}})

        self.assertFalse(search_filter.match({'id': 15, 'age': 50}))

    def test_regex(self):
        search_filter = FilterTool({'$filter': {'first_name': {'$reg': '^Jo.*'}}})

        self.assertTrue(search_filter.match({'first_name': 'John', 'last_name': 'Smith'}))

    def test_fail_regex(self):
        search_filter = FilterTool({'$filter': {'first_name': {'$reg': '.*nh$'}}})

        self.assertFalse(search_filter.match({'first_name': 'John', 'last_name': 'Smith'}))

    def test_inner_doc(self):
        search_filter = FilterTool({'$filter': {'user.first_name': 'John'}})

        self.assertTrue(search_filter.match({'user': {'first_name': 'John', 'last_name': 'Smith'}}))

    def test_fail_inner_doc_as_missing(self):
        search_filter = FilterTool({'$filter': {'user.name': 'John'}})

        self.assertFalse(search_filter.match({'user': {'first_name': 'John', 'last_name': 'Smith'}}))

    def test_fail_inner_doc(self):
        search_filter = FilterTool({'$filter': {'user.last_name': 'Doe'}})

        self.assertFalse(search_filter.match({'user': {'first_name': 'John', 'last_name': 'Smith'}}))

    def test_find_in_list(self):
        search_filter = FilterTool({'$filter': {'children': 'Junior'}})

        self.assertTrue(search_filter.match({'first_name': 'John', 'last_name': 'Doe', 'children': ['Junior', 'Mick']}))

    def test_negate(self):
        search_filter = FilterTool({'$filter': {'first_name': {'$not': 'John'}}})

        self.assertFalse(search_filter.match({'last_name': 'Doe', 'first_name': 'John'}))
        self.assertTrue(search_filter.match({'last_name': 'Doe', 'first_name': 'Joe'}))

    def test_negate_expression(self):
        search_filter = FilterTool({'$filter': {'$not': {'first_name': 'John'}}})

        self.assertFalse(search_filter.match({'last_name': 'Doe', 'first_name': 'John'}))
        self.assertTrue(search_filter.match({'last_name': 'Doe', 'first_name': 'Joe'}))

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(FilterToolTest)
