from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


"""
___just_migration___
docker-compose up --build
docker-compose exec web bash
flask db init
flask db migrate -m "migration-name"



___if errors___
rm -rf migrations
docker-compose exec db psql -U postgres -c "DROP TABLE alembic_version;"
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "migration-name"
docker-compose exec web flask db upgrade
"""


from app import routes


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))