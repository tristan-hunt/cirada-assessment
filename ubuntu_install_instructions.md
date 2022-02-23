# Installation and Usage: 

# 1. Check your python version
Most versions of ubuntu come with python3 as the default install. 
Do
```bash
$ python --version
```
To check. It should come back with a version > 3. 
If it comes back with a version smaller than 3, try:
```bash
$ python3 --version
```
And if that works, then just type python3 where it says python for the rest of these instructions.

# 2. Make sure pip is installed
pip is a package manager for python. It allows the user to access python repositories and install them. 
```bash
$ sudo apt update
$ sudo apt install python.pip
$ pip --version
```

# 3. Create virtual env for the cirada program
Ok this might seem like overkill for you but from experiene it's a bitch to fuck with your base install of python.
```bash
$ python -m venv cirada-env
$ source cirada-env/bin/activate
```

Now that you are working on a virtualenv for python, it's safe to do the following command which will install the required packages:
```bash
(cirada-env)$ pip install -r requirements.txt
```

When you're done playing you can do the following to deactivate the virtualenv
```bash
(cirada-env)$ deactivate
```

Note: If you try to run the tools without the packages installed (or if you've installed the packages but forgotten to activate 
the virtual environment) then you'll get an error message like the following:
```bash
Traceback (most recent call last):
  File "C:\Users\Tristan\Projects\CIRADA Assessment\visualization_tool.py", line 3, in <module>
    from astropy import units as u
ModuleNotFoundError: No module named 'astropy'
```
In this case either do
```bash
$ source cirada-env/bin/activate
```

or 
```bash
(cirada-env)$ pip install -r requirements.txt
```

and then the program should run fine. 

# 4. Running the tools: 
To run the visualization tool with no extra options:
```bash
$ python visualization_tool.py
```
This will prompt you for the right ascension and declination in degrees.

To run the visualization tool & specify your coordinate from the command line:
```bash
$ python visualization_tool.py -ra 338.12 -dec 11.53
```

To specify your search radius (in degrees):
```bash
$ python visualization_tool.py -ra 338.12 -dec 11.53 -r 1
```

To get a table of your results (which will display the names of the sources as well):
```bash
$ python table_tool.py -ra 338.12 -dec 11.53
```

Note that the default search radius for the visualization tool is 0.25 and the default for the table tool is 1. 
However both consume arguments in the same way. 

Once you know the names of the sources, you can use them as your search query:
```bash
$ python visualization_tool.py -sJ223235.3+114213 -r 0.25
```

:D 



