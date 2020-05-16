from flask import session, render_template , request, abort
from . import admin  
from mod_users.forms import LoginForm
from mod_users.modeles import User
 

@admin.route('/')
def index():
    return 'Hello from admin index '


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        #user = User.query.filter(User.email == form.email.data.first())          ##non case ensetice
        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first()   ##case ensetive
        if not user:
            return "Incorrect credentials !", 400
        if not user.check_password(form.password.data):
            return "Incorrect password !", 400
        session['email'] = user.email
        session['user_id'] = user.id
        return "Loged in successfully"
    if session.get('email') is not None:
        return "you are already loged in !"
    return render_template('admin/login.html', form=form)
