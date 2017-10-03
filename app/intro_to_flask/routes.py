# import Flask class & render_template function
from intro_to_flask import app
from flask import render_template, request, flash, session, redirect, url_for
from .forms import ContactForm, SignupForm, SigninForm
from flask_mail import Message, Mail 
from .models import db, User

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

# create the mail variable that contain a usable instance of Mail class
mail = Mail()

#  map URL / to function home --> URL visited, home() will execute
@app.route('/')
def home():
    # render home.html template
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      print("form invalid")
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      print("sending email")
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['ttrang1311@gmail.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      print(msg)
      print(mail.send(msg))
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    print("get form")
    return render_template('contact.html', form=form)

#create URL for  
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile')) 

   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      
      # taking hashing email into an excrypted ID and storing it in a cookie on the user's browser
      session['email'] = newuser.email
      # to redirect the user to a Profile page after signing in
      return redirect(url_for('profile'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

# create URL mapping for /profile
@app.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')

# create URL for /signin form
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

# create URL for signout
@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
  
  # clearing the cookie in the browser and dissociating the user data
  session.pop('email', None)
  return redirect(url_for('home'))
#  run app on local server
# if __name__ == '__main__':
#   app.run(debug=True)
# applicable error message shown '
# local server automatically reloads after code has been changed
