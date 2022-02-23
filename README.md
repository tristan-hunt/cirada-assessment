# Setup:
This project was written in Python (version 3.9.5), using the astropy, matplotlib, and numpy libraries. 

To run, first create and activate a new Python virtual env. There are many ways to do this. Here are a few:
With Anaconda:
```bash
conda create -n tristan-assessment-env python=3.9
conda activate tristan-assessment-env
```
For Mac/Linux:
```bash
$ python3 -m venv tristan-assessment-env
$ source tristan-assessment-env/bin/activate
```
For Windows command line(assuming your PATH and PATHTEXT variables are configured for Python and you're using Python3):
```
c:\> python -m venv tristan-assessment-env
c:\> tristan-assessment-env\Scripts\activate.bat
```
(More info here: https://docs.python.org/3/library/venv.html)

Then install the necessary libraries:
```bash
$ pip install -r requirements.txt
```

# Running:
To run the most basic version of the visualization assessment:
```bash
(tristan-assessment-env)$ python visualization_tool.py
```
This will prompt you to enter in a right ascension and declination, then produce a plot
of the FIRST sources within a 0.25 degree radius of the given coordinates. 
It will save the plot to a file called plot.html, which can be viewed in your browser.

The transient source software developer assessment is called the same way:
```bash
(tristan-assessment-env)$ python table_tool.py
``` 
It will produce a table of FIRST sources within a 1 degree radius of the given coordinates, and
save this table to a file called table.html, which can be viewed in your browser.

# Extensions:
You also have the option of specifying the search coordinates via optional command line arguments:
Use `-ra ` for the right ascension and `-dec ` for the declination. For example, to enter the coordinate
with right ascension of 338.12 and declination of 11.53, use the following: 
```bash
(tristan-assessment-env)$ python visualization_tool.py -ra 338.12 -dec 11.53
(tristan-assessment-env)$ python table_tool.py -ra 338.12 -dec 11.53
``` 

To specify the search radius, use the optional arguments `-r` or `--radius`:
```bash
(tristan-assessment-env)$ python visualization_tool.py -r 1
(tristan-assessment-env)$ python table_tool.py --radius 0.25
```

To specify the name of the FIRST source around which to perform the query, use the optional arguments `-s` or `--source`:
```bash
(tristan-assessment-env)$ python visualization_tool.py -s J223235.3+114213
(tristan-assessment-env)$ python table_tool.py --source J223235.3+114213
```

You can combine optional arguments, to specify both an alternate search radius and the name of the object around which
you want to search.

If you give a name of an object which is not listed in FIRST_data.fit, the program will inform you
that it cannot find the object, then prompt you for a coordinate. 

If you give both the right ascension / declination of a point and the name of an object, the program will
use the source name as the search criteria, but use the given right ascension / declination as a fallback
if it cannot find a FIRST source with that name. 


Extension #3 (Allow user to specify position in sexigessimal) was not implemented. 

One way to do this would be to add different optional arguments for ra and dec in sexigessimal.
So, for example, you could call: `python visualization_tool.py -ra60 00h42m30s -dec60 +41d12m00s`. 
Then, use the SkyCoord class in astropy to convert this coordinate to degrees for the remainder of the calculations. 
We would also want to make sure that the search query is displayed properly for the plot title and axis so 
that the same units are displayed as those used by the user. 
