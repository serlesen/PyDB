import unittest
from app.tools.search_context import SearchContext

class SearchContextTest(unittest.TestCase):

    def test_load_search_context(self):
        context = SearchContext({'$filter': {'id': 1}})

        self.assertIsNotNone(context.filter)
        self.assertEqual(context.size, 10)
        self.assertEqual(context.skip, 0)
        self.assertIsNone(context.sort)
        self.assertIsNone(context.map)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(SearchContextTest)
