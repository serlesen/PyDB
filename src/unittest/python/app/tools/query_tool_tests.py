import unittest
from app.tools.query_tool import QueryTool

class QueryToolTest(unittest.TestCase):
    def test_and_condition(self):
        query = QueryTool({'filter':{'id':1234}})

        self.assertTrue(query.match({'id': 1234}))

    def test_fail_and_condition(self):
        query = QueryTool({'filter':{'id':1234}})

        self.assertFalse(query.match({'id': 12345}))

    def test_fail_and_condition_by_missing(self):
        query = QueryTool({'filter':{'id':1234}})

        self.assertFalse(query.match({'some': 12345}))

    def test_multiple_and_conditions(self):
        query = QueryTool({'filter': {'first_name':'fn', 'last_name':'ln'}})

        self.assertTrue(query.match({'id': 1234, 'first_name': 'fn', 'last_name': 'ln'}))

    def test_fail_multiple_and_conditions(self):
        query = QueryTool({'filter': {'first_name':'fn', 'last_name':'ln'}})

        self.assertFalse(query.match({'id': 1234, 'first_name': 'fn', 'last_name': 'ln2'}))

    def test_in_condition(self):
        query = QueryTool({'filter': {'id': [12, 13, 14]}})

        self.assertTrue(query.match({'id': 13}))

    def test_fail_in_condition(self):
        query = QueryTool({'filter': {'id': [12, 13, 14]}})

        self.assertFalse(query.match({'id': 15}))

    def test_or_condition(self):
        query = QueryTool({'filter': [{'id': 15}, {'first_name': 'fn'}]})

        self.assertTrue(query.match({'first_name': 'fn'}))

    def test_fail_or_condition(self):
        query = QueryTool({'filter': [{'id': 15}, {'first_name': 'fn'}]})

        self.assertFalse(query.match({'first_name': 'fn2'}))

    def test_fail_or_condition_by_missing(self):
        query = QueryTool({'filter': [{'id': 15}, {'first_name': 'fn'}]})

        self.assertFalse(query.match({'last_name': 'ln'}))

    def test_inner_or_filter_condition(self):
        query = QueryTool({'filter': {'first_name': 'fn', 'filter': [{'last_name': 'ln'}, {'address': 'somewhere'}]}})

        self.assertTrue(query.match({'first_name': 'fn', 'last_name': 'ln2', 'address': 'somewhere'}))

    def test_fail_inner_or_filter_condition(self):
        query = QueryTool({'filter': {'first_name': 'fn', 'filter': [{'last_name': 'ln'}, {'address': 'somewhere'}]}})

        self.assertFalse(query.match({'first_name': 'fn', 'last_name': 'ln2', 'address': 'somewhere2'}))

    def test_inner_and_filter_condition(self):
        query = QueryTool({'filter': [{'first_name': 'fn'}, {'filter': {'last_name': 'ln', 'address': 'somewhere'}}]})

        self.assertTrue(query.match({'last_name': 'ln', 'address': 'somewhere'}))

    def test_fail_inner_and_filter_condition(self):
        query = QueryTool({'filter': [{'first_name': 'fn'}, {'filter': {'last_name': 'ln', 'address': 'somewhere'}}]})

        self.assertFalse(query.match({'last_name': 'ln2', 'address': 'somewhere2'}))
