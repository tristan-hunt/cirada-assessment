import argparse

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits 
from astropy.table import Table
import numpy as np

from helpers import get_FIRST_sources_within_radius, get_search_coordinates


def main(ra1, dec1, radius=1, source=None):
	# Get the point from the user if no command line arguments were given:
	# or get the coordinates of the named source if a name was given:
	ra1, dec1, source = get_search_coordinates(ra1, dec1, source)
	
	# Display search criteria: 
	search_term = source if source else '{:.2f} {:.2f}'.format(ra1, dec1)
	print('Finding FIRST sources within a {} {} radius of {}'.format(radius, 'degree', search_term))

	# Calculate which sources we want to show in the table
	table = get_FIRST_sources_within_radius(ra1, dec1, radius=radius)
	
	# Sort the table by distance from the given point
	table.sort('Angular Separation')

	save_html(table)

	return table


def save_html(table):
	table.write('table.html', format='html', overwrite=True)
	print('Done! View your result by opening table.html')	


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Transient Source Software tool")
	parser.add_argument('-ra', type=float, help='right ascension of your chosen position, in decimal degrees')
	parser.add_argument('-dec', type=float, help='declination of your chosen position, in decimal degrees')

	# Extension #1: allow user to pass in radius
	parser.add_argument('-r', '--radius', type=float, default=1, help='search radius (in degrees)')

	# Extension #2: allow user to specify FIRST source around which to perform the query
	parser.add_argument('-s', '--source', type=str, help='FIRST source around which to perform the query.')

	# See comments in visualization_tool.py for notes about extension3. 

	args = parser.parse_args()
	
	main(args.ra, args.dec, args.radius, args.source)