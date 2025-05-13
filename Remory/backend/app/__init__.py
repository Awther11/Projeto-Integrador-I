from flask import Flask

app = Flask(__name__,
            template_folder= 'front/templates',
            static_folder= 'front/static')

from app.routes import medicamentos