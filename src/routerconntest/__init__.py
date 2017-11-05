from flask import Flask

app = Flask(__name__)

# ensure all the necessary modules are imported
import routerconntest.controllers
