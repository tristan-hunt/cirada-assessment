from astropy.table import Table

import unittest
import unittest.mock as mock

import table_tool
import helpers


@mock.patch('table_tool.get_FIRST_sources_within_radius')
@mock.patch('table_tool.save_html')
class TestTableTool(unittest.TestCase):

    @mock.patch('builtins.input')
    def test_with_no_cmd_args(self, mock_input, mock_save, mock_get_sources):
        mock_input.side_effect = [0, -1]
        
        table = table_tool.main(None, None)

        mock_get_sources.assert_called_with(0, -1, radius=1)
        table.sort.assert_called_with('Angular Separation')

    def test_with_coordinates(self, mock_save, mock_get_sources):
        table = table_tool.main(338.12, 11.53)
        
        mock_get_sources.assert_called_with(338.12, 11.53, radius=1)
        table.sort.assert_called_with('Angular Separation')

    def test_with_radius(self, mock_save, mock_get_sources):
        table = table_tool.main(338.12, 11.53, radius=2)

        mock_get_sources.assert_called_with(338.12, 11.53, radius=2)
        table.sort.assert_called_with('Angular Separation')

    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_with_source(self, mock_coordinates, mock_save, mock_get_sources):
        mock_coordinates.return_value = [4, 5, 'search_term']
        table = table_tool.main(None, None, source='search_term')

        mock_get_sources.assert_called_with(4, 5, radius=1)
        table.sort.assert_called_with('Angular Separation')

    @mock.patch('builtins.input')
    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_with_source_not_found(self, mock_coordinates, mock_input, mock_save, mock_get_sources):
        mock_input.side_effect = [0, -1]
        mock_coordinates.side_effect = KeyError

        table = table_tool.main(None, None, source='missing')

        mock_get_sources.assert_called_with(0, -1, radius=1)
        table.sort.assert_called_with('Angular Separation')

    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_with_source_not_found_and_with_coordinates_given(self, mock_coordinates, mock_save, mock_get_sources):
        mock_coordinates.side_effect = KeyError
        table = table_tool.main(338, 11, source='missing')
    
        mock_get_sources.assert_called_with(338, 11, radius=1)
        table.sort.assert_called_with('Angular Separation')


if __name__ == '__main__':
    unittest.main()