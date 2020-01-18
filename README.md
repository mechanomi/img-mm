# Image Matchmaker

[![Travis CI status](https://img.shields.io/travis/mechanomi/img-mm/master.svg)](https://travis-ci.org/mechanomi/img-mm) [![Total alerts](https://img.shields.io/lgtm/alerts/g/mechanomi/img-mm.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mechanomi/img-mm/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mechanomi/img-mm.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mechanomi/img-mm/context:python)

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
- [ ] App should be able to be run on a server as a long-running app

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
- [ ] Preserve correct thumbnail order
- [ ] Fix restoration after undoing a delete
- [ ] Modify CLI script to use
  [Click](https://www.palletsprojects.com/p/click/))
- [ ] Add browser auto-reloading when source files change
- [ ] Add options to CLI script to control how images are loaded (passed in via
  STDIN, arguments, or implement our file search)

### Project setup

- [ ] Write initial Travis CI tests
- [ ] Research functional testing frameworks and implement initial tests
- [ ] Research code standard testing frameworks and implement initial tests
- [ ] Create initial docs project infrastructure
- [ ] Host docs on Read The Docs
- [ ] Write the initial docs
- [ ] Write initial docs tests
- [ ] Add top-level documentation
- [ ] Set up PyPI package
- [ ] Develop release process
- [ ] Codecov setup
- [ ] LGTM setup
- [ ] snyk.io setup
- [ ] pepy.tech setup
- [ ] enable other versions of Python (Travis CI)

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
- [ ] Add options to write metadata to filename (append) so files can be sorted
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

