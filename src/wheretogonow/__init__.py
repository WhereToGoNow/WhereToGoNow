import os

from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ensure all the necessary modules are imported
import wheretogonow.controllers
