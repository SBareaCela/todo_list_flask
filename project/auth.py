from flask import (
    Blueprint, render_template, request, url_for, redirect, flash,
    session, g
    )
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from project import db
#* Importaciones de wtform
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
import functools

#? Inicialización del blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

#! Crear formulario wtform
class RegisterForm(FlaskForm):
    username = StringField("Nombre de usuario: ", validators= [DataRequired(), Length(min=4, max=25)])
    password = PasswordField("Contraseña: ", validators= [DataRequired(), Length(min=6, max=40)])
    submit = SubmitField("Registrar")

#! Metodo para realizar el registro / mostrar formulario de registro
@bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        #? Sacar de la bbdd si existe un usuario ya con ese nombre
        user_name = User.query.filter_by(username = username).first()

        message = None

        if user_name == None:
            db.session.add(user)
            db.session.commit()

            message = f'El usuario {username} se ha registrado correctamente'
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            message = f'El usuario {username} ya está registrado'
            flash(message, 'error')
    return render_template('auth/register.html')

#! Metodo para realizar el login / mostrar formulario login
@bp.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #? Sacar de la bbdd si existe un usuario ya con ese nombre
        user = User.query.filter_by(username = username).first()

        message = None

        if user == None or not check_password_hash(user.password, password):
            message = "La contraseña o el usuario no concuerdan, verifique los datos introducidos."
            flash(message, 'error')

        if message == None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))

    return render_template('auth/login.html')

#! Metodo para mantener la sesión del usuario logeado
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

#! Metodo para cerrar sesión
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#! Decorador para comprobar si el usuario ha iniciado sesión antes de entrar en una url
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view