from flask import Flask

app = Flask(__name__)

# Import the database initialization function
from app.init_db import init_db
# Initialize the database
init_db()

from app import view