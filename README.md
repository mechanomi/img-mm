# Anyrank

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Travis CI status](https://img.shields.io/travis/mechanomi/imgmm/master.svg)](https://travis-ci.org/mechanomi/imgmm) [![Total alerts](https://img.shields.io/lgtm/alerts/g/mechanomi/imgmm.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mechanomi/imgmm/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mechanomi/imgmm.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mechanomi/imgmm/context:python)

Matchmaking system for quickly ranking huge collections of images.


## High-level goals

- [x] Uses simple Python web app framework
- [X] Runs from the command line and is given paths to find images
- [X] Launches app in browser
- [X] Displays multiple photos
- [ ] Work with more than two photos
- [X] Prioritize the ranking of images with least confidence
- [X] Photos are now in a match and you select the winner
- [X] App uses ELO type algo to determine new ranks
- [X] Ranks written to file metadata
- [ ] Document format so other apps can work with it
- [X] No other data store is used
- [X] New photos are displayed
- [X] App should be as responsive as possible to aid speed of use
- [X] You can quit any time while playing
- [ ] Compatibility with as many browser plugins as possible is desirable (e.g.,
  image zoom plugins)
- [ ] App should be able to be run like a regular OS app


## Initial milestones


### MVP


- [x] Research and pick Python web app framework
- [x] Write initial "Hello world!"
  [Flask](https://www.palletsprojects.com/p/flask/) app
- [x] Add script auto-reloading when source files change
- [x] Modify app to load filenames from `sys.argv` and read metadata into memory
- [x] Research and decide on ELO algo
- [X] Research and decide upon metadata format
- [X] Modify app to read metadata
- [X] Add filter for unsupported file types
- [X] Modify app display two random images side-by-side
- [X] Modify app to use a form to select one image
- [X] Modify app to calculate new ranks and write to image metadata
- [X] Record ranks using filenames


### Improve MVP

- [X] Handle missing files on reload
- [X] Fix image display vertical alignment
- [X] Modify app to select images with a preference for images with highest
  sigma
- [X] Pick highest sigma, then randomly from the closest mu values
- [X] Bind left and right arrow to candidate submissions
- [X] Don't pit an image against itself
- [X] Improve CSS so images auto-fit viewport
- [X] Implement delete functionality
- [X] Add shortcuts for delete
- [X] Implement undo functionality
- [X] Implement result action summary thumbnails
- [X] Remove randomization
- [X] Fix restoration after undoing a delete
- [ ] Preserve correct thumbnail order
- [ ] Add sqlite cache
- [ ] Fix stats calculation
- [ ] Look into file system changes monitoring
- [ ] Look into forking a subprocess to periodically update cache
- [ ] Prioritize files that were updated longest ago (less volatile if you're
  making active changes to the directory)
- [ ] Add material design
- [ ] Bind to 0.0.0.0 and test on mobile
- [ ] Calculate good match based on image similarity too (perceptual hash,
  hamming distance, multiply factors to generate match quality)


### CLI

- [ ] Modify CLI script to use
  [Click](https://www.palletsprojects.com/p/click/))
- [ ] Add options to CLI script to control how images are loaded (passed in via
  STDIN, arguments, or implement our file search)


### Project setup

- [X] Convert app into package (instead of module)
- [ ] Organize code into modules
- [ ] Set up PyPI package
- [ ] Develop release process
- [ ] Codecov setup
- [X] LGTM setup
- [X] snyk.io setup
- [ ] pepy.tech setup
- [ ] enable other versions of Python (Travis CI)
- [ ] Move imgmm README tasks to GitHub issues


### Tests

- [X] Write initial Travis CI tests
- [ ] Research functional testing frameworks and implement initial tests
- [X] Research code standard testing frameworks and implement initial tests
- [ ] Write initial docs tests
- [ ] Add top-level documentation


### Docs

- [ ] Create initial docs project infrastructure
- [ ] Host docs on Read The Docs
- [ ] Write the initial docs


### Chrome extensions compatibility

- [ ] Test interface for compatibility with relevant Chrome browser extensions
  (e.g., image zoom extensions)
- [ ] Modify interface to improve compatibility


### Speed improvements

- [ ] Add options to CLI script to intermittently load small random batches of
  images to speed things up with large collections


### Match enhancements

- [ ] Add options to specify how many images to put in a match
- [ ] Add options to convert rank to standard five-star rating metadata
  (logarithmic?) so files can be sorted in other apps
- [X] Add options to write metadata to filename (append) so files can be sorted
  in file manager


### Interface enchainments

TBD


### Design enhancements

TBD


### Cross-browser compatibility

TBD


### Accessibility

TBD


### Hosted version

TBD

