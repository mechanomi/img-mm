# Image Matchmaker

Matchmaking system for quickly ranking huge collections of images.

high-level goals:

- uses simple python web app framework (flask?)
- runs from the commandline and is given paths to find images
- launches app in browser
- displays multiple (default: 2) photos
- prioritize the ranking of images with no rank, and then prioritize images
  which haven't been matched for the longest time
- photos are now in a match. you click the winner
- app uses ELO type algo to determine new ranks
- ranks written to file metadata (document format so other apps can work with it)
- no other data store is used
- new photos are displayed
- app should be as responsive as possible to aid speed of use
- you can quit any time while playing
- compatibility with as many brower plugins as possible is desirable (e.g., image zoom plugins)
- app should be able to be run on a server as a long-running app

initial milestones:

- research and pick python web app framework
- write initial hello world app
- set up pypi infrastructure (for purposes of cli script workflow)
- add cli script that opens the app in a browser window
- add options to cli script to specify where to look for images
- modify app to search for images and all into memory
- research and decide on ELO algo
- research and decide upon metadata format
- document metadata format
- modify app to read metadata
- modify app to select images with a preference for images with no existing
  metadata, and then images that had not been modified for a longer amount of time
- modify app display images in a form which can be submitted by selecting one
- modify app to calculate ranks and write to image metadata
- test interface for compatibility with popular relevant browser extensions
- modify interface to improve compatibility with popular relevant browser extensions
- add options to cli script to specify how many images to put in a match
- add options to cli script to intermittently load small random batches of
  images to speed things up with large collections
