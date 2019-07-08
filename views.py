from myapp import app,db,login_manager
from flask_login import login_user,login_required,logout_user,current_user,user_logged_in,user_logged_out
from flask import render_template,session,request,redirect,url_for,flash
from sqlalchemy import exc
from models import Contact,Videos,Users,bcrypt,GalleryImg,Interns,Applicationfee,OfflinePay
from myapp import app,mail,Message
from itsdangerous import URLSafeTimedSerializer
from forms import SigninForm,RegisterForm,InternshipForm,VacancyForm,RecieptUpload
from decorators import check_confirmed,admin_login
from upload import upload_photo,upload_sign,upload_reciept
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.wrappers import Response
from datetime import datetime
import json
import os

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


with open(os.path.join(app.config['JSON_CONFIG'],'requirements.json'),'r') as json_file:
    json_data=json.load(json_file)


username = json_data["params"]["admin_username"]
password = json_data["params"]["admin_pass"]

# IS_VACANT=False

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

login_manager.login_view='signin'
login_manager.login_message = ""


@app.context_processor
def inject_links():
    return dict(sewa_links=json_data["sewa_links"])

@app.context_processor
def inject_vacancy():
    return dict(status=app.config['IS_VACANT'])


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about_us.html', name='ABOUT US')


@app.route('/contact',methods=['POST','GET'])
def contact():
    if request.method=='POST' :
        f_name=request.form.get('first_name')
        l_name = request.form.get('last_name')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('message')

        entry=Contact(first_name=f_name,last_name=l_name,address=address,email=email,phone=phone,msg=msg)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact_us.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/works')
def our_works():
    return render_template('our_works.html')

'''use function name in href links'''

@app.route('/gallery')
def gallery():
    return redirect(url_for('galleryitems',page_num=1))


@app.route('/gallery/<int:page_num>')
def galleryitems(page_num):
    final_imglist=GalleryImg.query.paginate(per_page=10,page=page_num,error_out=False)
    print(final_imglist.total)

    return render_template('gallery.html',img_list=final_imglist)


@app.route('/videos')
def video_gallery():
    vid_list=Videos.query.all()
    return render_template('video-gallery.html', filelist=vid_list)

@app.route('/it_team')
def it_team():
    return render_template('it_team.html')


#============================Vacancy related routes======================================>
@app.route('/vacancy', methods=['GET','POST'])
@login_required
def vacancy_form():
    vform=VacancyForm()
    amt=Applicationfee.query.all()
    if vform.validate_on_submit():

        pass

    return render_template('vacancy.html',form=vform,fee=amt[-1].vacancyfee)


@app.route('/dashboard/vacancy')
@login_required
@admin_login
def dash_vacancy():
    return render_template('src_dashboard/vacancy_control.html')


@app.route('/vacancy-indicate/<status>')
@login_required
@admin_login
def vacancy_indicate(status):
    app.config['IS_VACANT'] = status
    print(app.config['IS_VACANT'])
    # vs=Vacancy_status(datetime=datetime.now(),status=status)
    # db.session.add(vs)
    # db.session.commit()
   
    return redirect(url_for('dash_vacancy'))

#============================Vacancy related routes======================================>
@app.route('/offlinepay',methods=['GET','POST'])
def offlinePay():
    form=RecieptUpload()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.career.data)
        rpath=upload_reciept()
        print(rpath)
        pass

    return render_template('payment_handler/offline_payment.html',form=form)


#============================Internship related routes======================================>
@app.route('/internship',methods=['GET','POST'])
@login_required
def internship():
    iform=InternshipForm()
    amt_fee=Applicationfee.query.all()
    try:
        if iform.validate_on_submit():
        # if request.method =='POST':
            p=upload_photo() #capturing photoname
            s=upload_sign()  #capturing signature name

            print(s)
            print(type(s))
            print(p)
            print(type(p))

            if type(p) is not Response and type(s) is not Response:
                intern=Interns(name=iform.fullname.data,
                               email=iform.email.data,
                               contactadd=iform.contactadd.data,
                               permanentadd=iform.permanentadd.data,
                               add_course=iform.addtionalcourse.data,
                               learnings=iform.learnings.data,
                               motivation=iform.motivation.data,
                               voluntary=iform.voluntaryprog.data,
                               nationality=iform.nationality.data,
                               dob=iform.dob.data,
                               lang=iform.language.data,
                               area_of_interest=iform.areas.data,
                               phone=iform.phone.data,
                               gender=iform.gender.data,
                               fee=iform.fee.data,
                               amt=amt_fee[-1].internfee,
                               photopath=p,
                               signpath=s,
                               userid=current_user.username)
                db.session.add(intern)
                db.session.commit()
                flash('Uploaded Successfully','success')
                # if iform.fee.data == 'online':
                #     return render_template('it_team.html')
                # else:
                #     return redirect(url_for('index'))
           
            
    except exc.IntegrityError:
        flash('File already present. You may change the filaname','danger')
        return  redirect(url_for('internship'))
    except AttributeError:
        flash('File too large','dnager')
        return redirect(url_for('internship'))

    return render_template('internship.html',form=iform,ifee=amt_fee[-1].internfee)





@app.route('/dashboard/interns')
@login_required
@admin_login
def dash_intern():
    # amt_fee=Applicationfee.query.all()
    # print(amt_fee)
    # print(amt_fee[-1].internfee)
    # print(amt_fee[-1].vacancyfee)
    return render_template('src_dashboard/interns_detail.html')



@app.route('/setapplcnfee',methods=['GET','POST'])
@login_required
@admin_login
def setapplcnfee():  #sets fees amount for both internship and vacancy form
    if request.method == 'POST':
        if 'internfeebtn' in request.form:
            l=Applicationfee.query.all()
            json_data['params']['default_vacancy_fee']=l[-1].vacancyfee
            ifee=request.form['internfee']
            fee=Applicationfee(internfee=ifee,vacancyfee=json_data['params']['default_vacancy_fee'])
            db.session.add(fee)
            db.session.commit()
            print(type(ifee))
            print(ifee)
            return redirect(url_for('dash_intern'))

        if 'vacancyfeebtn' in request.form:
            l=Applicationfee.query.all()
            json_data['params']['default_intern_fee']=l[-1].internfee
            vfee=request.form['vacancyfee']
            fee=Applicationfee(internfee=json_data['params']['default_intern_fee'],vacancyfee=vfee)
            db.session.add(fee)
            db.session.commit()
            print(fee)
            return redirect(url_for('dash_vacancy'))

    return redirect(url_for('dashboard'))

#============================Internship related routes======================================>

@app.route('/register',methods=['GET','POST'])
def register():
    regform=RegisterForm()
    if regform.validate_on_submit():

        try:
            if regform.password.data == regform.confirmPassword.data:

                new_user=Users(regform.firstname.data,regform.lastname.data,regform.address.data,regform.phone.data,regform.email.data,regform.username.data,regform.password.data,verified=False,admin=False)

                db.session.add(new_user)
                db.session.commit()
                print('new user has been created')

                token = serializer.dumps(regform.email.data,salt=app.config['SECURITY_PASSWORD_SALT'])
                link=url_for('verify_email',token=token,_external=True)
                msg=Message('Confirm email',sender=app.config['MAIL_USERNAME'],recipients=[regform.email.data])
                msg.body='Welcome! Thank you for registering to SEWA. Please click on the link to activate your account: Note: Please note the link will expire after 1hr {}'.format(link)
                mail.send(msg)

                login_user(new_user)

                #flash('A confirmation email has been sent to your email. If not found check your spam folder','success ')
                return redirect(url_for('unconfirmed'))

            else:
                flash('Pasword mismtach. Please try again!','danger')
                return render_template('user/register.html', sewa_links=json_data["sewa_links"],form=regform)
        except exc.IntegrityError as e:

            flash('Username or Email already exists. Try again!', 'danger')
            return render_template('user/register.html', sewa_links=json_data["sewa_links"], form=regform)


    return render_template('user/register.html',form=regform)


@app.route('/signin',methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    sform=SigninForm()
    try:
        if sform.validate_on_submit():
            user=Users.query.filter_by(username=sform.username.data).first()

            if user:
                if bcrypt.check_password_hash(user.password,sform.password.data):
                    login_user(user,remember=sform.remember.data)
                    flash('Your have successfully logged in','success')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid Password! Please try again','danger')
                    return redirect(url_for('signin'))
            else:
                flash('Invalid Username! Please try again...', 'danger')
                return redirect(url_for('signin'))

    except:
        flash('Oops! Something wrong with the Database.Please try again after some time.')
        return redirect(url_for('signin'))

    return render_template('user/signin.html',form=sform)


@app.route('/profile')
@check_confirmed
@login_required
def profile():
    return render_template('user/profile.html')

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.verified:
        print(current_user.verified)
        return redirect(url_for('index'))
    flash('Please confirm your account!','warning')
    return render_template('user/unconfirmed.html')



@app.route('/verify_email/<token>')
def verify_email(token):

    try:
        email= serializer.loads(token,salt=app.config['SECURITY_PASSWORD_SALT'],max_age=100)
        '''max age in seconds'''
        print('inside :'+email)
    except:

        return '<h1>Your token expired. Please Register Again!</h1>'

    user=Users.query.filter_by(email = email).first_or_404()
    print(user.email)
    print(user.verified)

    if user.verified:
        return 'Account already verified!'
    else:
        user.verified=True
        db.session.add(user)
        db.session.commit()
        return render_template('user/verify_user.html')


@app.route('/resend')
@login_required
def resend_confirmation():
    try:
        new_token=serializer.dumps(current_user.email,salt=app.config['SECURITY_PASSWORD_SALT'])
        verify_url=url_for('verify_email',token=new_token,_external=True)
        msg = Message('Confirm email', sender=app.config['MAIL_USERNAME'], recipients=[current_user.email])
        msg.body = 'Welcome! Thank you for registering to SEWA. Please click on the link to activate your account: Note: Please note the link will expire after 1hr {}'.format(
            verify_url)
        mail.send(msg)
        flash('A new verification link has been sent to your email.','success')
        return redirect(url_for('unconfirmed'))
    except:
        flash('Server is not respnding. Please try again later!','danger')
        return redirect(url_for('unconfirmed'))




@app.route('/dashboard')
@login_required
@admin_login
def dashboard():
    return render_template('src_dashboard/dashboard.html')


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':

        if request.form.get('ad_username') == username and request.form.get('ad_password') == password:
            session['username']=username
            print(session.get('username'))
            return render_template('src_dashboard/dashboard.html')
        else:
            flash('Invalid username or password!', 'warning')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))


#============================Registered Users related routes======================================>

@app.route('/dashboard/users')
@login_required
@admin_login
def users():
    return redirect(url_for('userpages', page_num=1))

@app.route('/dashboard/users/<int:page_num>')
@login_required
@admin_login
def userpages(page_num):
    user=Users.query.paginate(page=page_num,per_page=3,error_out=False)
    return render_template('src_dashboard/users.html',userslist=user)



@app.route('/dashboard/delete/<email>')
@login_required
@admin_login
def user_del(email):
    user=Users.query.filter_by(email=email).first()
    print(email)
    # db.session.delete(user)
    # db.session.commit()
    # print('user deleted')
    flash('User removed successfully!','success')
    return redirect(url_for('users'))

#============================Registered Users related routes======================================>

#final appilcation form to be printed out

@app.route('/final_form')
def finalform():
    intern=Interns.query.filter_by(userid=current_user.username).first()
    return render_template('printable_applications/final_internship_form.html',intern=intern)

# def flash_errors(form):
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(u"Error in the %s field - %s" % (
#                 getattr(form, field).label.text,
#                 error
#             ),'danger')


'''
def create_admin():
    db.session.add(Users(
        firstname='Bibek',
        lastname='Bora',
        email='pritam307aec@gmail.com',
        username='admin@sewa',
        password='sewa@123',
        admin=True,
        phone='1221323',
        verified=True,
        address='asdsad'))
    db.session.commit()
'''