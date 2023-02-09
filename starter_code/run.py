from section_7.starter_code.app import app
from section_7.starter_code.db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
