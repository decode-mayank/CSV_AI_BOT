from flask_migrate import Migrate, upgrade
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)
with app.app_context():
    upgrade()
