from flask import session, render_template , request, abort, flash
from . import admin  
from mod_users.forms import LoginForm
from mod_users.modeles import User
from .utils import admin_only_view


@admin.route('/')
@admin_only_view
def index():
    if session.get('user_id') is None:
        abort(401)
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
            flash('Incorrect credentials !', category='warning')
            return render_template('admin/login.html', form=form)
        if not user.check_password(form.password.data):
            flash('Incorrect password !', category='error')
            return render_template('/admin/login.html', form=form), 400
        if not user.is_admin():
            flash('You are not admin','warning')
            return render_template('/admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role
        return "Loged in successfully"
    if session.get('role') == 1:
        return "you are already loged in !"
    return render_template('admin/login.html', form=form)
