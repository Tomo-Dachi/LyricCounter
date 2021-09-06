# LyricCounter

This project allows a user to enter a musical artist and
will then return the average word count of all their songs

Built using Python, it makes use of the 'requests' library
to make HTTP requests to *Musixmatch*, an API that
specialises in returning information and metadata about
musical artists and their releases.

Click was used to then make a simple cli that takes the artist,
checks if they exist on the musixmatch database, returns the first
artist and then loops through all their existing songs to determine
the average number of words

### Installation
After cloning the repo, create a python virtual environment and activate it:

`virtualenv venv`

`venv/scripts/activate`

Then install the required packages with help from the requirements.txt file:

`pip install -r requirements.txt`



### How to use
First, obtain an API key by creating a developer account at musixmatch (https://developer.musixmatch.com/). The API key can then be found under /applications on your dashboard

Make sure your virtual environment has been activated and then, invoke LyricCounter by calling `lyriccounter`

The user will then be prompted to enter their API key, and then the name of an artist whose average word count they wish to know.
These can also be provided on the command line: 

`lyriccounter --apikey <apikey> --artist <artist>`

The program will then run, calculating the chosen artist's average. If the artist cannot be found, or any http errors occur then the user will be informed via the CLI and the program will stop

### Future goals
With more time, there are several additions I would make to the project:
  - Unit testing, to help ensure functionality isn't broken when the app grows in size
  - The functionality to ask more specific questions to LyricCounter. The functionality to return informaton on an artist's albums, tracks, and lyrics is available within the current functionality, but cannot be called by the CLI. A future release to fix this and to also add further questions like an artist's genre would be a good addition to the project.
  - An inheritable API class, to more easily make use of different 
  - A Flask frontend, to better display the information returned from musixmatch and to make the app more accessible.

### Links
- Musicranx developer documentation (https://developer.musixmatch.com/documentation)
- Python requests library (https://docs.python-requests.org/en/master/)
- Click library (https://click.palletsprojects.com/en/8.0.x/)
