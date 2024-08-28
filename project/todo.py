from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from project.auth import login_required
from .models import Todo, User
from project import db

bp = Blueprint('todo', __name__, url_prefix='/todo')

#! Metodo para mostrar la pagina de tareas de un usuario
@bp.route('/list')
@login_required
def index():
    todos = Todo.query.filter_by(created_by = g.user.id).all()
    has_todos =  len(todos) > 0
    return render_template('todo/index.html', todos = todos, has_todos = has_todos)

#! Metodo para crear la tarea de un usuario
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        try:
            title = request.form['title']
            desc = request.form['desc']

            todo = Todo(g.user.id, title, desc)

            db.session.add(todo)
            db.session.commit()
            flash('Tarea creada con éxito', 'success')
        except Exception as e:
            flash('Error al crear la tarea', 'error')
        return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

#! Metodo para actualizar la tarea de un usuario
@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        try:
            todo.title = request.form['title']
            todo.desc = request.form['desc']
            todo.state = True if request.form.get('state') == 'on' else False
            db.session.commit()
            flash('Tarea actualizada con éxito', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la tarea', 'error')
        return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo = todo)

#! Metodo para eliminar la tarea de un usuario
@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    try:
        db.session.delete(todo)
        db.session.commit()
        flash('Tarea eliminada con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la tarea', 'error')

    return redirect(url_for('todo.index'))

#! Metodo para obtener la lista de tareas por la id del usuario
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo