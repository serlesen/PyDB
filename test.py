import unittest
from app.services.test_file_reader import FileReaderTest
from app.tools.test_filter_tool import FilterToolTest
from app.tools.test_search_context import SearchContextTest

def suite():
    return unittest.TestSuite([
        FileReaderTest.suite(),
        FilterToolTest.suite(),
        SearchContextTest.suite()
        ])

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())