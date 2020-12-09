# filmfest

This project automates downloading a submissions folder from www.filmfreeway.com for a local film fest using selenium with chromedriver.
The csv that selenium points to is a custom export config created in the website's settings, named "Basic Summary"

## logging in

Run submissions.py

If settings.py does not find a local .env folder, it will create one and ask to store your keys (username and password) here. 
If you enter them wrong, delete the local .env folder and try again

## submissions.py

submissions.py triggers selenium to: 
1. open a headless chrome window
2. log in (using the credentials in your local environment)
3. navigate to the submissions tab
4. export a custom congigured csv file ("Basic Summary" configuration)

In a perfact world, I would be using requests over selenium, but...
*I chose selenium after hitting a wall with requests, do to all of the embedded javascript on the site*

It looked like I could plausibly use requests with jQuery to successfully automate this download (I looked into that beifly)
...but due to time constaints and my familiarity with Python I chose selenium.

## process.py

process.py will only work with my 2020 "Basic Summary" submissions export configuration
It's just cleaning up some data and generating a couple very basic visualizations

Run process.py
- generate EntriesPerCat_BAR.png
- generate EntriesPerCat_PIE.png

## settings.py

settings.py contains a function that creates a local .env to store user credentials in environment variables in order to login to filmfreeway securely. It will ask for the username and password in the terminal. *if the password is incorrectly entered, you have to delete the .env file and restart the submissions script.* python-dotenv *is used to load the credentials into submissions.py. This script is not indended to run directly in the terminal.*

## TODO

- Create a log of each year's data and log old summary submission csv's for analysis
- Create a login check so you will not have to manually delete .env file
- Create some better looking summary statistics and data viz that can be reused with little modification

- Extend functionality: Automate grabbing movie from each submission (after the Submission status is labelled as accepted in the retrieved submissions df)