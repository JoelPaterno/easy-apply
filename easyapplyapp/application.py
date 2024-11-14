import os
from easyapplyapp import create_app

application = create_app()

# Add this for local testing
if __name__ == '__main__':
    application.run()