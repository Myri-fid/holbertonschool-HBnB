import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'part4')))

from part4.app.api.v1 import create_app
from config import DevelopmentConfig

app = create_app(config_class=DevelopmentConfig)

if __name__ == '__main__':
    app.run()
