from flask import Flask

app = Flask(__name__, template_folder="../templates", static_folder="../static")
from box2box.app import routes
