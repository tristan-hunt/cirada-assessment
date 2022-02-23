from astropy.io import fits
from astropy.table import Table
import numpy as np

import unittest
import unittest.mock as mock
import helpers

class TestGetFIRSTSourcesWithinRadius(unittest.TestCase):
    def test_reads_file_and_has_correct_columns(self):
        result = helpers.get_FIRST_sources_within_radius(338.12, 11.53)
        self.assertEqual(188, len(result))
        self.assertEqual(['FIRST', 'RAJ2000', 'DEJ2000', 'Fint', 'c1', 'Angular Separation'], result.colnames)

    @mock.patch('astropy.io.fits.open')
    def test_returns_correct_rows(self, mock_open):
        mock_file = mock.MagicMock()
        mock_table = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994]], names=['RAJ2000', 'DEJ2000'])
        mock_file.data = mock_table
        mock_open.return_value.__enter__.return_value = [None, mock_file]

        result = helpers.get_FIRST_sources_within_radius(0, 0)
        self.assertEqual(2, len(result))

    @mock.patch('astropy.io.fits.open')
    def test_when_specifying_radius(self, mock_open):
        mock_file = mock.MagicMock()
        mock_table = Table([[0.086, 0.154, 0.127], [-0.0798, 0.100, -1.994]], names=['RAJ2000', 'DEJ2000'])
        mock_file.data = mock_table
        mock_open.return_value.__enter__.return_value = [None, mock_file]

        result = helpers.get_FIRST_sources_within_radius(0, 0, 2)
        self.assertEqual(3, len(result))

class TestGetCoordinatesForFIRSTSource(unittest.TestCase):
    @mock.patch('astropy.io.fits.open')
    def test_when_found(self, mock_open):
        mock_file = mock.MagicMock()
        mock_table = Table([['a', 'b', 'c'], [1, 3, 5], [2, 4, 6]], names=['FIRST', 'RAJ2000', 'DEJ2000'])
        mock_file.data = mock_table
        mock_open.return_value.__enter__.return_value = [None, mock_file]

        result = helpers.get_coordinates_for_FIRST_source('b')
        self.assertEqual(result[0], 3)
        self.assertEqual(result[1], 4)
        self.assertEqual(result[2], 'b')

    @mock.patch('astropy.io.fits.open')
    def test_when_not_found(self, mock_open):
        mock_file = mock.MagicMock()
        mock_table = Table([['a', 'b', 'c'], [1, 3, 5], [2, 4, 6]], names=['FIRST', 'RAJ2000', 'DEJ2000'])
        mock_file.data = mock_table
        mock_open.return_value.__enter__.return_value = [None, mock_file]

        with self.assertRaises(KeyError):
            helpers.get_coordinates_for_FIRST_source('d')


class TestGetSearchCoordinates(unittest.TestCase):
    @mock.patch('builtins.input')
    def test_asks_user_input_if_none_given(self, mock_input):
        mock_input.side_effect = [0, -1]
        r1, r2, r3 = helpers.get_search_coordinates(None, None, None)
        self.assertEqual(r1, 0)
        self.assertEqual(r2, -1)
        self.assertEqual(r3, None)

    def test_returns_passed_coordinates_if_ra_and_dec_given(self):
        r1, r2, r3 = helpers.get_search_coordinates(0, -1, None)
        self.assertEqual(r1, 0)
        self.assertEqual(r2, -1)
        self.assertEqual(r3, None)      

    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_returns_coordinates_of_source_if_source_given(self, mock_coordinates):
        mock_coordinates.return_value = [4, 5, 'search_term']
        r1, r2, r3 = helpers.get_search_coordinates(None, None, 'search_term')

        self.assertEqual(r1, 4)
        self.assertEqual(r2, 5)
        self.assertEqual(r3, 'search_term')

    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_prioritizes_source(self, mock_coordinates):
        mock_coordinates.return_value = [4, 5, 'search_term']
        r1, r2, r3 = helpers.get_search_coordinates(0, -1, 'search_term')

        self.assertEqual(r1, 4)
        self.assertEqual(r2, 5)
        self.assertEqual(r3, 'search_term')

    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_returns_when_source_not_found(self, mock_coordinates):
        mock_coordinates.side_effect = KeyError
        r1, r2, r3 = helpers.get_search_coordinates(2, 3, 'missing')

        self.assertEqual(r1, 2)
        self.assertEqual(r2, 3)
        self.assertEqual(r3, None)

    @mock.patch('builtins.input')
    @mock.patch('helpers.get_coordinates_for_FIRST_source')
    def test_when_source_not_found_and_no_passed_coordinates(self, mock_coordinates, mock_input):
        mock_input.side_effect = [0, -1]
        mock_coordinates.side_effect = KeyError
        r1, r2, r3 = helpers.get_search_coordinates(None, None, 'missing')

        self.assertEqual(r1, 0)
        self.assertEqual(r2, -1)
        self.assertEqual(r3, None)



if __name__ == '__main__':
    unittest.main()