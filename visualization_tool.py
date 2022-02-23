import argparse

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits 
from astropy.table import Table

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import numpy as np

from helpers import get_FIRST_sources_within_radius, get_search_coordinates


COLOR_MAP = {
	'g': ['red', 'galaxy'],  # display galaxies as red
	's': ['green', 'star'],  # display stars as green  
	' ': ['blue', 'other']  # everything else is blue
}



def main(ra1, dec1, radius=0.25, source=None):	
	# Get the search coordinates from user input if no command line arguments were given,
	# or get the coordinates of the named source if a name was given:
	ra1, dec1, source = get_search_coordinates(ra1, dec1, source)
	
	# Keep track of the search term to use for the plot's title:
	search_term = source if source else '{:.2f}\u00b0 {:.2f}\u00b0'.format(ra1, dec1)

	# Calculate which sources to display in the visualization:
	table = get_FIRST_sources_within_radius(ra1, dec1, radius=radius)

	# Sort them by size to make the way the points overlap one another a bit more consistent:
	table.sort('Fint')
	table.reverse()

	# Create the scatterplot
	fig, ax = plt.subplots()

	# Add the data to the scatterplot
	x = table['RAJ2000']
	y = table['DEJ2000']
	sizes = table['Fint']
	colors = [COLOR_MAP[c][0] for c in table['c1']]
	scatter = ax.scatter(x, y, s=sizes, c=colors, alpha=0.5)

	# Set the legend and labels
	patches = [mpatches.Patch(color=value[0], label=value[1]) for value in COLOR_MAP.values()]
	ax.legend(handles=patches, title="SDSS Classification")

	ax.set_xlabel('Right Ascension (degree)')
	ax.set_ylabel('Declination (degree)')
	ax.set_title('FIRST Sources within {}{} of {}'.format(radius, '\u00b0', search_term))
	
	save_html(ra1, dec1, radius)

	return fig, ax


def save_html(ra1, dec1, radius):
	# Save the figure to a png image and then write to an html file. 
	title = 'fig_{}_{}_{}.png'.format(ra1, dec1, radius)
	plt.savefig(title)
	with open('plot.html', 'w') as file:
		file.write('<html><head><title>CIRADA Technical Assessment</title></head><img src="{}"></html>'.format(title))
	print('Done! View your result by opening plot.html')


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Visualization tool")
	parser.add_argument('-ra', type=float, help='Right Ascension of your chosen position, in decimal degrees.')
	parser.add_argument('-dec', type=float, help='Declination of your chosen position, in decimal degrees.')
	
	# Extension #1: Allow user to pass in radius
	parser.add_argument('-r', '--radius', type=float, default=0.25, help='Search Radius (in degrees).')

	# Extension #2: Allow user to specify FIRST source around which to perform the query
	parser.add_argument('-s', '--source', type=str, help='FIRST source around which to perform the query.')

	args = parser.parse_args()

	main(args.ra, args.dec, args.radius, args.source)
