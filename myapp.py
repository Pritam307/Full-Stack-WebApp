from flask import Flask
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES,patch_request_class
import os

app=Flask(__name__)

app.config.from_pyfile('config.py')


db=SQLAlchemy(app)
mail=Mail(app)
Bootstrap(app)

login_manager=LoginManager()
login_manager.init_app(app)

# galleryphoto=UploadSet('photos',IMAGES,default_dest=lambda app: os.path.join(app.config['UPLOAD_FOLDER']+'gallery_img/'))
# internsphoto=UploadSet('phtoto',IMAGES,default_dest=lambda app: os.path.join(app.config['UPLOAD_FOLDER']+'interns_img/'))
# configure_uploads(app,(galleryphoto,internsphoto))
# patch_request_class(app,10* 1024 * 1024)

from views import *
from upload import *



if __name__ == '__main__':
    app.run()
