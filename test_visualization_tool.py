from astropy.table import Table

import unittest
import unittest.mock as mock

import visualization_tool

@mock.patch('visualization_tool.get_FIRST_sources_within_radius')
@mock.patch('visualization_tool.save_html')
class TestVisualizationTool(unittest.TestCase): 

    @mock.patch('builtins.input')
    def test_with_no_cmd_args(self, mock_input, mock_save, mock_get_sources):
        mock_get_sources.return_value = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994], [0.5, 0.6, 0.2], [' ', 'g', 's']], names=['RAJ2000', 'DEJ2000', 'Fint', 'c1'])
        mock_input.side_effect = [0, -1]
        
        plot = visualization_tool.main(None, None)
        
        mock_save.assert_called_with(0, -1, 0.25)
        mock_get_sources.assert_called_with(0, -1, radius=0.25)
        self.assertEqual('FIRST Sources within 0.25° of 0.00° -1.00°', plot[1].title.get_text())
        self.assertEqual('Right Ascension (degree)', plot[1].xaxis.get_label().get_text())
        self.assertEqual('Declination (degree)', plot[1].yaxis.get_label().get_text())

    def test_with_coordinates(self, mock_save, mock_get_sources):
        mock_get_sources.return_value = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994], [0.5, 0.6, 0.2], [' ', 'g', 's']], names=['RAJ2000', 'DEJ2000', 'Fint', 'c1'])
        
        plot = visualization_tool.main(338.12, 11.53)
        
        mock_save.assert_called_with(338.12, 11.53, 0.25)
        mock_get_sources.assert_called_with(338.12, 11.53, radius=0.25)
        self.assertEqual('FIRST Sources within 0.25° of 338.12° 11.53°', plot[1].title.get_text())
        self.assertEqual('Right Ascension (degree)', plot[1].xaxis.get_label().get_text())
        self.assertEqual('Declination (degree)', plot[1].yaxis.get_label().get_text())

    def test_with_radius(self, mock_save, mock_get_sources):
        mock_get_sources.return_value = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994], [0.5, 0.6, 0.2], [' ', 'g', 's']], names=['RAJ2000', 'DEJ2000', 'Fint', 'c1'])
        
        plot = visualization_tool.main(338.12, 11.53, radius=1)

        mock_save.assert_called_with(338.12, 11.53, 1)
        mock_get_sources.assert_called_with(338.12, 11.53, radius=1)
        self.assertEqual('FIRST Sources within 1° of 338.12° 11.53°', plot[1].title.get_text())
        self.assertEqual('Right Ascension (degree)', plot[1].xaxis.get_label().get_text())
        self.assertEqual('Declination (degree)', plot[1].yaxis.get_label().get_text())

    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_with_source(self, mock_coordinates, mock_save, mock_get_sources):
        mock_get_sources.return_value = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994], [0.5, 0.6, 0.2], [' ', 'g', 's']], names=['RAJ2000', 'DEJ2000', 'Fint', 'c1'])
        mock_coordinates.return_value = [4, 5, 'TestObjectName']
        
        plot = visualization_tool.main(None, None, source='TestObjectName')
        
        mock_save.assert_called_with(4, 5, 0.25)
        mock_get_sources.assert_called_with(4, 5, radius=0.25)
        self.assertEqual('FIRST Sources within 0.25° of TestObjectName', plot[1].title.get_text())
        self.assertEqual('Right Ascension (degree)', plot[1].xaxis.get_label().get_text())
        self.assertEqual('Declination (degree)', plot[1].yaxis.get_label().get_text())

    @mock.patch('builtins.input')
    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_with_source_not_found(self, mock_coordinates, mock_input, mock_save, mock_get_sources):
        mock_get_sources.return_value = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994], [0.5, 0.6, 0.2], [' ', 'g', 's']], names=['RAJ2000', 'DEJ2000', 'Fint', 'c1'])
        mock_input.side_effect = [0, -1]
        mock_coordinates.side_effect = KeyError

        plot = visualization_tool.main(None, None, source='missing')

        mock_save.assert_called_with(0, -1, 0.25)
        mock_get_sources.assert_called_with(0, -1, radius=0.25)
        self.assertEqual('FIRST Sources within 0.25° of 0.00° -1.00°', plot[1].title.get_text())
        self.assertEqual('Right Ascension (degree)', plot[1].xaxis.get_label().get_text())
        self.assertEqual('Declination (degree)', plot[1].yaxis.get_label().get_text())

    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_with_source_not_found_and_with_ra_and_dec(self, mock_coordinates, mock_save, mock_get_sources):
        mock_get_sources.return_value = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994], [0.5, 0.6, 0.2], [' ', 'g', 's']], names=['RAJ2000', 'DEJ2000', 'Fint', 'c1'])
        mock_coordinates.side_effect = KeyError

        plot = visualization_tool.main(338, 11, source='missing')
        
        mock_save.assert_called_with(338, 11, 0.25)
        mock_get_sources.assert_called_with(338, 11, radius=0.25)
        self.assertEqual('FIRST Sources within 0.25° of 338.00° 11.00°', plot[1].title.get_text())
        self.assertEqual('Right Ascension (degree)', plot[1].xaxis.get_label().get_text())
        self.assertEqual('Declination (degree)', plot[1].yaxis.get_label().get_text())


if __name__ == '__main__':
    unittest.main()