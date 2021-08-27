# @TODO we want to "from .app import main" so the test suite can import the
# main() function but if we do that then app.py throws errors when importing
# from config.py & its other dependencies
from .has_syllabus import *
