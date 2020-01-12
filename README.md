# Image Matchmaker

Matchmaking system for quickly ranking huge collections of images.

## High-level goals

- [x] Uses simple Python web app framework (Flask?)
- [ ] Runs from the commandline and is given paths to find images
- [ ] Launches app in browser
- [ ] Displays multiple (default: two) photos
- [ ] Prioritize the ranking of images with no rank, and then prioritize images
  [ ] Which haven't been matched for the longest time
- [ ] Photos are now in a match. you click the winner
- [ ] App uses ELO type algo to determine new ranks
- [ ] Ranks written to file metadata (document format so other apps can work
  with it)
- [ ] No other data store is used
- [ ] New photos are displayed
- [ ] App should be as responsive as possible to aid speed of use
- [ ] You can quit any time while playing
- [ ] Compatibility with as many browser plugins as possible is desirable (e.g.,
  Image zoom plugins)
- [ ] App should be able to be run on a server as a long-running app

## Initial milestones

### MVP


- [x] Research and pick Python web app framework
- [x] Write initial "Hello world!"
  [Flask](https://www.palletsprojects.com/p/flask/) app
- [x] Add script auto-reloading when source files change
- [x] Modify app to load filenames from sys.argv and read metadata into memory
- [x] Research and decide on ELO algo
- [X] Research and decide upon metadata format
- [X] Modify app to read metadata
- [X] Add filter for unsupported file types
- [X] Modify app display two random images side-by-side
- [X] Modify app to use a form to select one image
- [X] Modify app to calculate new ranks and write to image metadata

### Improve MVP

- [ ] Modify app to select images with a preference for images with no existing
  metadata, and then images that had not been modified for a longer amount of
  time
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
