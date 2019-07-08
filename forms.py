from wtforms import StringField,PasswordField,BooleanField,TextAreaField,SelectField,RadioField,ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms.validators import InputRequired,Email,Length,DataRequired
from wtforms.fields.html5 import DateField
from flask_login import current_user
from datetime import date

c=['0','1','2','3','4','5','6','7','8','9']

class SigninForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(),DataRequired(),Length(min=6,max=15,message='username must be between 6 to 15 characters long')])
    password=PasswordField('password',validators=[InputRequired(),DataRequired(),Length(min=6,max=80,message='password must more than 6 characters long')])
    remember=BooleanField('remember me')


class RegisterForm(FlaskForm):
    firstname=StringField('firstname',validators=[InputRequired(),DataRequired(),Length(max=10)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(max=15)])
    email=StringField('email',validators=[InputRequired(),DataRequired(),Email(message='Invalid Email'),Length(max=50)])
    username = StringField('username', validators=[InputRequired(), DataRequired(), Length(min=6, max=15)])
    phone=StringField('phone',validators=[InputRequired(),DataRequired(),Length(min=6,max=10)])
    address=StringField('address',validators=[InputRequired(),Length(max=40)])
    password=PasswordField('password',validators=[InputRequired(),DataRequired(),Length(min=8,max=80)])
    confirmPassword=PasswordField('confirmPassword',validators=[InputRequired(),DataRequired(),Length(min=8,max=80)])

    def validate_phone(form,field):
        for i in field.data:
            if i not in c:
                raise ValidationError('Invalid number')




class InternshipForm(FlaskForm):

    fullname=StringField('fullname',validators=[InputRequired(),DataRequired(),Length(max=25)])
    email=StringField('email',validators=[InputRequired(),DataRequired(),Email(message='Invalid Email!'),Length(max=50)])
    contactadd=StringField('contactadd',validators=[InputRequired(),DataRequired(),Length(min=6,max=100)])
    permanentadd=StringField('permanentaddress',validators=[InputRequired(),DataRequired(),Length(min=6,max=100)])
    addtionalcourse=TextAreaField('course',validators=[InputRequired(),DataRequired(),Length(max=100)])
    learnings=TextAreaField('learnings',validators=[InputRequired(),DataRequired(),Length(max=200)])
    motivation=TextAreaField('motivation',validators=[InputRequired(),DataRequired(),Length(max=200)])
    voluntaryprog=TextAreaField('voluntaryprog',validators=[InputRequired(),DataRequired(),Length(max=150)])
    nationality=SelectField('nationality',validators=[InputRequired(),DataRequired()],choices=[('hindu','Hinduism'),('jain','Jainism'),('buddist','Buddhism'),('islam','Islam'),('sikh','Sikhism')])
    dob=DateField('dob',validators=[InputRequired(),DataRequired()],format='%Y-%m-%d')
    language=StringField('language',validators=[InputRequired(),DataRequired(),Length(max=50)])
    phone=StringField('phone',validators=[InputRequired(),DataRequired(),Length(max=10)])
    gender=RadioField('gender',validators=[InputRequired(),DataRequired()],choices=[('Male','Male'),('Female','Female')])
    areas=SelectField('areas',validators=[InputRequired(),DataRequired()],choices=[('Web Development','Web Development'),('MobileApp Developemt','Mobile App Development'),('SocailActivity','Social Activity')])
    fee=RadioField('fee',validators=[InputRequired(),DataRequired()],choices=[('online','ONLINE'),('offline','OFFLINE')])


    def validate_phone(form,field):
        if len(field.data) < 10:
            raise ValidationError('Invalid phone no')

        for i in field.data:
            if i not in c:
                raise ValidationError('Invalid phone no')


class VacancyForm(FlaskForm):

    fullname=StringField('fullname',validators=[InputRequired(),DataRequired(),Length(max=25)])
    email=StringField('email',validators=[InputRequired(),DataRequired(),Email(message='Invalid Email!'),Length(max=50)])
    contactadd=StringField('contactadd',validators=[InputRequired(),DataRequired(),Length(min=6,max=30)])
    permanentadd=StringField('permanentaddress',validators=[InputRequired(),DataRequired(),Length(min=6,max=40)])
    addtionalcourse=TextAreaField('course',validators=[InputRequired(),DataRequired(),Length(max=100)])
    learnings=TextAreaField('learnings',validators=[InputRequired(),DataRequired(),Length(max=200)])
    motivation=TextAreaField('motivation',validators=[InputRequired(),DataRequired(),Length(max=200)])
    voluntaryprog=TextAreaField('voluntaryprog',validators=[InputRequired(),DataRequired(),Length(max=150)])
    nationality=SelectField('nationality',validators=[InputRequired(),DataRequired()],choices=[('hindu','Hinduism'),('jain','Jainism'),('buddist','Buddhism'),('islam','Islam'),('sikh','Sikhism')])
    dob=DateField('dob',validators=[InputRequired(),DataRequired()],format='%Y-%m-%d')
    language=StringField('language',validators=[InputRequired(),DataRequired(),Length(max=50)])
    phone=StringField('phone',validators=[InputRequired(),DataRequired(),Length(max=10)])
    gender=RadioField('gender',validators=[InputRequired(),DataRequired()],choices=[('M','Male'),('F','Female')])
    areas=SelectField('areas',validators=[InputRequired(),DataRequired()],choices=[('Web','Web Development'),('mobile app','Mobile App Development'),('social','Social Activity')])
    fee=RadioField('fee',validators=[InputRequired(),DataRequired()],choices=[('online','ONLINE'),('offline','OFFLINE')])


    def validate_phone(form,field):
        if len(field.data) < 10:
            raise ValidationError('Invalid phone no')

        for i in field.data:
            if i not in c:
                raise ValidationError('Invalid phone no')

class RecieptUpload(FlaskForm):

    username=StringField('username',validators=[InputRequired(),DataRequired()])
    career=SelectField('career',validators=[InputRequired(),DataRequired()],choices=[('Internship','Internship'),('Vacancy','Vacancy')])


    def validate_username(form,field):
        if field.data != current_user.username:
            raise ValidationError('Invalid username')