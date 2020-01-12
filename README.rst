================
Image Matchmaker
================

Matchmaking system for quickly ranking huge collections of images.

High-level goals
================

- Uses simple Python web app framework (flask?)
- Runs from the commandline and is given paths to find images
- Launches app in browser
- Displays multiple (default: two) photos
- Prioritize the ranking of images with no rank, and then prioritize images
  Which haven't been matched for the longest time
- Photos are now in a match. you click the winner
- App uses ELO type algo to determine new ranks
- Ranks written to file metadata (document format so other apps can work with
  it)
- No other data store is used
- New photos are displayed
- App should be as responsive as possible to aid speed of use
- You can quit any time while playing
- Compatibility with as many browser plugins as possible is desirable (e.g.,
  Image zoom plugins)
- App should be able to be run on a server as a long-running app

Initial milestones
==================

MVP
---

- [] Research and pick Python web app framework
- [] Write initial hello world app
- [] Add cli script that opens the app in a browser window
- [] Add options to cli script to specify where to look for images
- [] Modify app to search for images and all into memory
- [] Research and decide on ELO algo
- [] Research and decide upon metadata format
- [] Document metadata format
- [] Modify app to read metadata
- [] Modify app to select images with a preference for images with no existing
     metadata, and then images that had not been modified for a longer amount of
     time
- [] Modify app display images in a form which can be submitted by selecting one
- [] Modify app to calculate ranks and write to image metadata

Project setup
-------------

- [] Write initial Travis CI tests
- [] Research functional testing frameworks and implement initial tests
- [] Research code standard testing frameworks and implement initial tests
- [] Create initial docs project infrastructure
- [] Host docs on Read The Docs
- [] Write the initial docs
- [] Write initial docs tests
- [] Add top-level documentation
- [] Set up PyPI package
- [] Develop release process

Chrome extensions compatibility
-------------------------------

- [] Test interface for compatibility with relevant Chrome browser extensions
     (e.g., image zoom extensions)
- Modify interface to improve compatibility

Speed improvements
------------------

- [] Add options to cli script to intermittently load small random batches of
     images to speed things up with large collections

Match enhancements
------------------

- [] Add options to cli script to specify how many images to put in a match

Interface enchainments
----------------------

TBD

Design enhancements
-------------------

TBD

Cross-browser compatibility
---------------------------

TBD

Accessibility
-------------

TBD

Hosted version
--------------

TBD
