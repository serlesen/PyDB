import unittest

from app.tools.results_mapper import ResultsMapper
from app.tools.search_context import SearchContext

class ResultsMapperTest(unittest.TestCase):

    def test_map_fields(self):
        search_context = SearchContext({'$map': {'first_name': 'name'}})

        results = ResultsMapper.map([{'first_name': 'John', 'last_name': 'Smith'}], search_context)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'John')
        self.assertTrue('last_name' not in results[0])
        self.assertTrue('first_name' not in results[0])

    def test_map_input_inner_doc(self):
        search_context = SearchContext({'$map': {'user.first_name': 'name'}})

        results = ResultsMapper.map([{'user': {'first_name': 'John', 'last_name': 'Smith'}}], search_context)

        self.assertEqual(results[0]['name'], 'John')

    def test_map_output_inner_doc(self):
        search_context = SearchContext({'$map': {'$include': {'first_name': 'user.name'}}})

        results = ResultsMapper.map([{'first_name': 'John', 'last_name': 'Smith'}], search_context)

        self.assertEqual(results[0]['user']['name'], 'John')

    def test_both_map_inner_doc(self):
        search_context = SearchContext({'$map': {'user.first_name': 'customer.name'}})

        results = ResultsMapper.map([{'user': {'first_name': 'John', 'last_name': 'Smith'}}], search_context)
        
        self.assertEqual(results[0]['customer']['name'], 'John')

    def test_field_as_itself(self):
        search_context = SearchContext({'$map': {'first_name': '$itself'}})

        results = ResultsMapper.map([{'first_name': 'John', 'last_name': 'Smith'}], search_context)

        self.assertEqual(results[0]['first_name'], 'John')

    def test_doc_as_itself(self):
        search_context = SearchContext({'$map': {'user': '$itself'}})

        results = ResultsMapper.map([{'user': {'first_name': 'John', 'last_name': 'Smith'}}], search_context)

        self.assertEqual(results[0]['user']['first_name'], 'John')
        self.assertEqual(results[0]['user']['last_name'], 'Smith')

    def test_exclude_single_field(self):
        search_context = SearchContext({'$map': {'$exclude': ['first_name']}})

        results = ResultsMapper.map([{'first_name': 'John', 'last_name': 'Smith'}], search_context)

        self.assertTrue('first_name' not in results[0])
        self.assertTrue('last_name' in results[0])


    def test_exclude_inner_field(self):
        search_context = SearchContext({'$map': {'$exclude': ['user.first_name']}})

        results = ResultsMapper.map([{'user': {'first_name': 'John', 'last_name': 'Smith'}}], search_context)

        self.assertTrue('first_name' not in results[0]['user'])
        self.assertTrue('last_name' in results[0]['user'])


    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(ResultsMapperTest)
