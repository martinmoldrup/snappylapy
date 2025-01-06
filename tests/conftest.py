import sys
import os
# Add the root directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

pytest_plugins = 'pytester'