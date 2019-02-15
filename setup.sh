
#!/bin/sh
source `which virtualenvwrapper.sh`
mkvirtualenv -p `which python3` backend-challenge-trip
pip install -r requirements-dev.txt
workon backend-challenge-trip
