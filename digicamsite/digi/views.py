from flask import Blueprint, redirect, flash
from flask import render_template
from base64 import b64encode
from flask import request
from digi import db
from flask import Blueprint, render_template, redirect, url_for, session,flash
from functools import wraps
from digi.models import Photo
from sqlalchemy import desc
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
import random
from werkzeug.utils import secure_filename

#this file sets what the index route of the web application will be
mainbp = Blueprint("main", __name__)

site_password = 'big nuts'
admin_pass='zz'
mypath='C:\\Users\\eej\\Pictures'
# custome decorator to check password
def check_pw(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        status = session.get('status')
        if status != "good":
            return redirect(url_for('main.login'))
        return func(*args, **kwargs)

    return decorated_function
#the index route is a search bar unless a search has been done in which case the function querys the database and fetches the results to display them

@mainbp.route("/<pagenum>")
@check_pw
def index(pagenum):  
    photos = Photo.query.order_by(desc(Photo.creation_date)).all()
    #random.shuffle(photos)
    listing=PageResult(photos,pagenum)
    print((listing.page))
    return render_template("bindex.html",listing=PageResult(photos,pagenum))
   
@mainbp.route("/")
def reroute():
    return redirect("/0")
class PageResult:
   def __init__(self, data, page = 1, number = 21):
     self.__dict__ = dict(zip(['data', 'page', 'number'], [data, page, number]))
     self.full_listing = [self.data[i:i+number] for i in range(0, len(self.data), number)]
   def __iter__(self):
     for i in self.full_listing[int(self.page)-1]:
       yield i
   def __repr__(self): #used for page linking
     return "/displayitems/{}".format(int(self.page)+1) #view the next page

@mainbp.route("/admin/<pagenum>")
@check_pw
def showalladmin(pagenum):
    photos = Photo.query.order_by(desc(Photo.creation_date)).all()
    random.shuffle(photos)
    listing=PageResult(photos,pagenum)
    print((listing.page))
    return render_template("adminindex.html",listing=PageResult(photos,pagenum))

@mainbp.route('/login', methods=['GET','POST'])
def login():
     if request.method == "POST":
            print("poggers")
            

            password = request.form.get('password')
            print(password)
            if password==admin_pass:
                session["status"] = 'good'
                return redirect("/admin/0")

            if password != site_password:
                flash('wrong password! try again...')
                return redirect(request.url)

            if password==site_password:
                session["status"] = 'good'
                print("yoooo")
                return redirect("/0")


     return render_template('login.html')
@mainbp.route("/add")
def add():
 
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))& f.endswith('.JPG')]
    for file in onlyfiles:
     photo = Photo(
              
                name=file,
                image_name=file,
                creation_date=datetime.today()       
            )
     db.session.add(photo)

    db.session.commit()

    return redirect("/0")

@mainbp.route("/delete/<int:id>")

def delete(id):
      photos = Photo.query.filter_by(id=id).first()
      print(photos)
      os.remove(os.getcwd()+ "\\digicamsite\\digi\\static\\imgs\\"+ secure_filename(photos.image_name))
      db.session.delete(photos)
      db.session.commit()  
      return redirect("/0")

@mainbp.route("/post", methods=["GET", "POST"])
def create():
    #form = PhotoForm()

    # attaching the form users fill out to the function
    if request.method == "POST":
       
            uploaded_files = request.files['file']
                
            # add file names to file db and then save files to server
            uploaded_files.save(
                os.path.join(
                os.getcwd() + "\\digicamsite\\digi\\static\\imgs",
                secure_filename(uploaded_files.filename),
                    )
                )
            print(request.form.get('name'))
            photo = Photo(
                        name=request.form.get('name'),
                        image_name=secure_filename(uploaded_files.filename),
                        creation_date=datetime.today()       
                    ) 
            db.session.add(photo)
                     
                    
            db.session.commit()  

               
                
                
   
            return redirect("/0")
    return render_template("uploader.html")

