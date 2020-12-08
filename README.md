# filmfest

This project automates downloading a submissions folder from www.filmfreeway.com for a local film fest using selenium with chromedriver.
The csv that selenium points to is a custom export config created in the website's settings, named "Basic Summary"

## logging in

Run submissions.py

If settings.py does not find a local .env folder, it will create one and ask to store your keys (username and password) here. 
If you enter them wrong, delete the local .env folder and try again

submissions.py triggers selenium to: 
-open a headless chrome window
-log in (using the credentials in your local environment)
-navigate to the submissions tab
-export a custom congigured csv file ("Basic Summary" configuration)

In a perfact world, I would be using requests over selenium, but...
*I chose selenium after hitting a wall with requests, do to all of the embedded javascript on the site*

It looked like I could plausibly use requests with jQuery to successfully automate this download (I looked into that beifly)
...but due to time constaints and my familiarity with Python I chose selenium.

## getting viz

process.py will only work with my 2020 "Basic Summary" submissions export configuration
It's just cleaning up some data and generating a couple (not so impressive) visualizations

Run process.py
-generate EntriesPerCat_BAR.png
-generate EntriesPerCat_PIE.png

## TODO

Create some better looking summary statistics and data viz that can be reused with little modification