from myapp import app,db
from flask_login import UserMixin
from flask_bcrypt import Bcrypt,generate_password_hash

bcrypt=Bcrypt(app)


class Contact(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50),  nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    msg = db.Column(db.String(150), nullable=False)



class Videos(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    vid = db.Column(db.String(50),unique=True,nullable=False)

class Users(UserMixin, db.Model):

    __tablename__= 'users'

    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String,unique=False,nullable=False)
    lastname=db.Column(db.String,unique=False,nullable=False)
    address=db.Column(db.String,unique=False,nullable=False)
    phone=db.Column(db.String,unique=True,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    verified=db.Column(db.BOOLEAN,nullable=False,default=False)
    admin=db.Column(db.BOOLEAN,nullable=False,default=False)

    def __init__(self,firstname,lastname,address,phone,email,username,password,verified,admin=False):
        self.firstname=firstname
        self.lastname=lastname
        self.address=address
        self.phone=phone
        self.email=email
        self.username=username
        self.password=generate_password_hash(password)
        self.verified=verified
        self.admin=admin



class GalleryImg(db.Model):
    __tablename__='galleryimages'

    id=db.Column(db.Integer,primary_key=True)
    imgname=db.Column(db.String(50),unique=True,nullable=False)
    imgpath=db.Column(db.String(50),unique=True,nullable=False)

class Interns(db.Model):

    __tablename__='interns'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=False,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    contactadd=db.Column(db.Text,unique=False,nullable=False)
    permanentadd = db.Column(db.Text, unique=False, nullable=False)
    add_course=db.Column(db.String,unique=False,nullable=False)
    learnings=db.Column(db.Text,unique=False,nullable=False)
    motivation=db.Column(db.Text,unique=False,nullable=False)
    voluntary=db.Column(db.Text,unique=False,nullable=False)
    nationality=db.Column(db.String,unique=False,nullable=False)
    dob=db.Column(db.DateTime,unique=False,nullable=False)
    lang=db.Column(db.String,unique=False,nullable=False)
    area_of_interest=db.Column(db.String,unique=False,nullable=False)
    phone=db.Column(db.String,unique=False,nullable=False)
    gender=db.Column(db.String,unique=False,nullable=False)
    fee=db.Column(db.String,unique=False,nullable=False)
    amt=db.Column(db.String,unique=False,nullable=False)
    photopath=db.Column(db.String,unique=True,nullable=False)
    signpath=db.Column(db.String,unique=True,nullable=False)
    userid=db.Column(db.String,unique=True,nullable=False)
    

    # def __int__(self,name,email,contactadd,permanentadd,add_course,learnings,motivation, voluntary,nationality,dob,lang,area_of_interest,area,phone,gender,fee,photo,signature):
    #     self.name=name
    #     self.email=email
    #     self.contactadd=contactadd
    #     self.permanentadd=permanentadd
    #     self.add_course=add_course
    #     self.learnings=learnings
    #     self.motivation=motivation
    #     self.voluntary=voluntary
    #     self.nationality=nationality
    #     self.dob=dob
    #     self.lang=lang
    #     self.area_of_interest=area_of_interest
    #     self.phone=phone
    #     self.gender=gender
    #     self.fee=fee
    #     self.photo=photo
    #     self.signature=signature

# class Vacancy_status(db.Model):
#     __tablename__="vacancy_status"

#     id=db.Column(db.Integer,primary_key=True)
#     datetime=db.Column(db.DateTime,unique=False,nullable=False)
#     status=db.Column(db.BOOLEAN,unique=False,default=False)

#     def __init__(self,datetime,status):
#         self.datetime=datetime
#         self.status=status


class Applicationfee(db.Model):
    __tablename__='application_fees'

    id=db.Column(db.Integer,primary_key=True)
    internfee=db.Column(db.String(50),unique=False,default=250)
    vacancyfee=db.Column(db.String(50),unique=False,default=250)


    """docstring for Applicationfee"""
    def __init__(self, internfee,vacancyfee):
        self.internfee=internfee
        self.vacancyfee=vacancyfee


class OfflinePay(db.Model):
    __tablename__="offlinepay_reciept"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=False,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    username=db.Column(db.String,unique=True,nullable=False)
    amt=db.Column(db.Integer,unique=False,nullable=False)
    career=db.Column(db.String,unique=False,nullable=False)
    datetime=db.Column(db.String,unique=False,nullable=False)
    reciept_img=db.Column(db.String,unique=True,nullable=False)