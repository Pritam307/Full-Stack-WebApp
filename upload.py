from myapp import app,db
from models import GalleryImg,Interns,GalleryImg
from flask_login import login_required
from decorators import admin_login
from flask import render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from sqlalchemy.exc import IntegrityError
from PIL import Image
import os
from io import BytesIO

isimguploaded=False
issignuploaded=False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_IMG']

def allowed_img(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_DOCS']


# def get_img_size(photo):
#     file=Image.open(photo)
#     w,h=file.size
#     # size=os.path.getsize(photo)
#     return w,h


@app.route('/dashboard/gallery_pictures')
@login_required
@admin_login
def upload_pictures():
    return redirect(url_for('picturepages',page_num=1))


@app.route('/dashboard/gallery_pictures/<int:page_num>')
@login_required
@admin_login
def picturepages(page_num):
    imglist=GalleryImg.query.paginate(page=page_num,per_page=5,error_out=False)
    return render_template('src_dashboard/upload_pictures.html',listimg=imglist)

@app.route('/dashboard/delete_img/<imgname>')
@login_required
@admin_login
def delImg(imgname):
    img=GalleryImg.query.filter_by(imgname=imgname).first()
    print(img.imgname)
    db.session.delete(img)
    db.session.commit()
    path=os.path.join(app.config['UPLOAD_FOLDER']+'gallery_img/',imgname)
    os.remove(path)
    flash('{} removed successfully'.format(imgname),'success')
    return redirect(url_for('upload_pictures'))

@app.route('/dashboard/gallery_pictures',methods=['GET','POST'])
@login_required
@admin_login
def upload_file():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('No file part','warning')
                return redirect(request.url)

            file= request.files['file']

            if file.filename == '':
                flash('No file selected for uploading','warning')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                secure_file=secure_filename(file.filename)
                filepath=os.path.join(app.config['UPLOAD_FOLDER']+'gallery_img/',secure_file)
                file.save(filepath)
                size=os.path.getsize(filepath)/(1024*1024)
                print(size)
                if size < 5:
                    img=GalleryImg(imgpath=os.path.join(app.config['UPLOAD_FOLDER']+'gallery_img/',secure_file),imgname=secure_file)
                    db.session.add(img)
                    db.session.commit()
                    flash('File successfully uploaded','success')
                    return redirect(url_for('upload_pictures'))
                else:
                    os.remove(filepath)
                    flash('Image too large. Maximum size 5Mb','warning')
                    return redirect(url_for('upload_pictures'))
            else:
                flash('File is not an image!','warning')
                return redirect(url_for('upload_pictures'))
        except RequestEntityTooLarge:
            flash('file in too large!','warning')
            return  redirect(url_for('upload_pictures'))
        except IntegrityError:
            flash('Image already exist! Select different image','danger')
            return redirect(url_for('upload_pictures'))

    return redirect(url_for('upload_pictures'))


@app.route('/dashboard/gallery_pictures/multi',methods=['GET','POST'])
@login_required
@admin_login
def upload_multiple_file():
    if request.method == 'POST':
        try:
            if 'file[]' not in request.files:
                flash('No file part','warning')
                return redirect(request.url)
            files=request.files.getlist('file[]')
          
            for file in files:
                if file and allowed_file(file.filename):
                    filename=secure_filename(file.filename)
                    filepath=os.path.join(app.config['UPLOAD_FOLDER']+'gallery_img/',filename)
                    file.save(filepath)
                    size=os.path.getsize(filepath)/(1024*1024)
                    print(size)
                    if size < 5:
                        img=GalleryImg(imgname=filename,imgpath=os.path.join(app.config['UPLOAD_FOLDER']+'gallery_img/',filename))
                        db.session.add(img)
                        db.session.commit()
                    else:
                        os.remove(filepath)
                        flash('Image too large. Maximum size 5Mb','warning')
                        return redirect(url_for('upload_pictures'))
                

                else:
                    flash('File is not an image!','warning')
                    return redirect(url_for('upload_pictures'))
            flash('File(s) successfully uploaded','success')

        except RequestEntityTooLarge:
            flash('File too large to upload. Maximum size 1024x1024','danger')
            return redirect(url_for('upload_pictures'))
        except IntegrityError:
            flash('Image already exist! Select different image', 'danger')
            return redirect(url_for('upload_pictures'))
    return redirect(url_for('upload_pictures'))

#==================Upload methods for Internship form ==============================#

def upload_photo():

        if 'photo' not in request.files :
            flash('No photo selected','warning')
            return redirect(request.url)

        # f=request.files['photo'].read()
        # size=len(f)/1024
        # print(size)

        file_photo=request.files['photo']

        if file_photo.filename == '' :
            flash('No photo selected!', 'warning')
            return redirect(request.url)

        if file_photo and allowed_file(file_photo.filename):
            filename=secure_filename(file_photo.filename)
            filepath=os.path.join(app.config['UPLOAD_FOLDER']+'interns_img/photo/',filename)

            file_photo.save(filepath)
            size=os.path.getsize(filepath)/1024
            if size < 50:
                # flash('photo uploaded', 'success')
                return filename
            else:
                flash('Maximum size of signature : 50kb', 'warning')
                os.remove(filepath)
                return redirect(url_for('internship'))
        else:
            flash('Photo is not an image!','warning')
            return redirect(url_for('internship'))
            

def upload_sign():

        if 'signature' not in request.files:
            flash('No signature selected','warning')
            return redirect(request.url)

        # f=request.files['signature'].read()
        # f.close()
        # size=len(f)/1024
        # print(size)


        file_sign=request.files['signature']


        if file_sign.filename == '':
            flash('No signature selected!','warning')
            return redirect(request.url)

        if file_sign and allowed_file(file_sign.filename):
            filename=secure_filename(file_sign.filename)
            filepath=os.path.join(app.config['UPLOAD_FOLDER']+'interns_img/signature/',filename)

            file_sign.save(filepath)
            size=os.path.getsize(filepath)/1024
            if size < 50:
                # flash('sign uploaded', 'success')
                return filename
            else:
                flash('Maximum size of signature : 50kb', 'warning')
                os.remove(filepath)
                return redirect(url_for('internship'))
        else:
            flash('Signature is not an image!','warning')
            return redirect(url_for('internship'))
            
#==================Upload methods for Internship form ==============================#

def upload_reciept():

    if 'reciept' not in request.files:
        flash('No reciept selected','warning')
        return redirect(request.url)


    reciept=request.files['reciept']

    if reciept.filename =='':
        flash('No signature selected!','warning')
        return redirect(request.url)

    if reciept and allowed_file(reciept.filename):
        filename=secure_filename(reciept.filename)
        filepath=os.path.join(app.config['UPLOAD_FOLDER']+'offline_reciepts/',filename)

        reciept.save(filepath)
        return filepath
    else:
        flash('Not an image!','warning')
        return redirect(url_for('offlinePay'))

