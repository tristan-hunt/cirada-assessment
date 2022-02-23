from astropy import units as u
from astropy.coordinates import SkyCoord, Angle
from astropy.io import fits 
from astropy.table import Table
import numpy as np


FILENAME = 'FIRST_data.fit'

def get_FIRST_sources_within_radius(ra1, dec1, radius=1):
	c1 = SkyCoord(ra=ra1*u.degree, dec=dec1*u.degree)
	with fits.open(FILENAME) as hdul:  
		data = hdul[1].data	

	# Get the 2nd and 3rd columns into their own numpy arrays and then create a catalog with the coordinates:
	ra = data['RAJ2000']
	dec = data['DEJ2000']
	catalog = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)

	# Get indexes of FIRST sources that are within the given radius:
	separations = c1.separation(catalog)
	catalogmsk = separations < radius*u.degree

	# Use catalogmsk to get the relevant rows from data. 
	masked_data = np.compress(catalogmsk, data, axis=0)
	masked_separations = np.compress(catalogmsk, separations, axis=0)

	# Using the AstroPy Table class in order to concat the column with angular separation from the user-defined position. 
	# Technically not necessary for the visualization, but computation cost is not very much 
	# and we already have everything we need right here.
	table = Table(data=masked_data)
	separations_col = Table.Column(name='Angular Separation', data=masked_separations)
	table.add_column(separations_col)

	return table



def get_search_coordinates(ra1, dec1, source):
	"""
	Returns the right ascension (ra) and declination (dec) of the search query, along with the name of the source if appropriate.

	i.e. 
	If a source is given and found within FIRST_data, returns the ra and dec of the source along with the given name.
	If a source is given and can not be found, requests a new set of coordinates from the user and returns None as the source name.
	If a source is not given, and a right ascension and declination have been provided, then returns those and None as the source name.
	If no search criteria has been provided, requests a right ascension and declination from the user (in degrees).
	"""
	if source:
		try:
			return get_coordinates_for_FIRST_source(source)
		except KeyError:
			print('No matching FIRST source found.')
			source = None

	if ra1 is None:
		ra1 = float(input("Enter the right ascension (in degrees): "))  # test input: 338.12

	if dec1 is None:
		dec1 = float(input("Enter the declination (in degrees): "))  # test input: 11.53

	return ra1, dec1, source



def get_coordinates_for_FIRST_source(FIRST):
	"""
	Used for extension #2, which allows the user to specify a FIRST source around which
	to perform the query.

	This implementation is less efficient because we are opening and reading the fit file twice - 
	but during testing, this hasn't made a noticable difference in terms of speed and it has the
	benefit of separating the code for extension #2 out from the rest of the code. 

	Raises a KeyError if no matching FIRST source is found.
	"""
	with fits.open(FILENAME) as hdul:
		data=hdul[1].data

	table = Table(data=data)
	table.add_index('FIRST')
	
	row = table.loc[FIRST]

	return row['RAJ2000'], row['DEJ2000'], FIRST
