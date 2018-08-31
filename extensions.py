from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#auth = JwtAuthentication()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


