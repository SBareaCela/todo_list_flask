from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#* Inicialización de objeto de SQLAlchemy
db = SQLAlchemy()

def create_app():
    #* Inicialización de objeto Flask
    app = Flask(__name__)

    migrate = Migrate(app, db)
    
    #! Configuración del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///flpsb.db"
    )

    #! Realizar conexión a la base de datos
    db.init_app(app)

    #! Filtros Personalizados
    @app.add_template_filter    #? Añadir un filtro de forma global
    def today (date):
        return date.strftime('%d-%m-%Y')

    #! Funcion Personalizada
    @app.add_template_global    #? Añadir una funcion de forma global
    def repeat(s, n):
        return s * n

    #! Ruta Principal
    @app.route('/')
    def index():
        name = 'Sergio'
        friends = ['Ferry', 'Quique', 'Fernando', 'Fran']
        date = datetime.now()

        return render_template(
            'index.html', 
            name = name, 
            friends = friends,
            date = date
            )

    #! Ruta del Saludo
    @app.route('/hello')
    @app.route('/hello/')
    @app.route('/hello/<string:name>')
    @app.route('/hello/<string:name>/')
    @app.route('/hello/<string:name>/<int:age>')
    @app.route('/hello/<string:name>/<int:age>/')
    def hello(name = None, age = None):
        if name == None and age == None:
            return render_template('saludo.html')
        elif name and age == None:
            return f'<h1>Hello, {name}!</h1>'
        else:
            return f'<h1>Hello, {name}!</h1><h2>Your age is {age}</h2>'

    #! Ruta de la Suma
    @app.route('/plus')
    @app.route('/plus/')
    @app.route('/plus/<int:num1>')
    @app.route('/plus/<int:num1>/')
    @app.route('/plus/<int:num1>/<int:num2>')
    @app.route('/plus/<int:num1>/<int:num2>/')
    def plus(num1 = None, num2 = None):
        if num1 == None and num2 == None:
            return render_template('sumar.html')
        elif num2 == None:
            return '<h1>Solo has ingresado el primer numero, por favor ingrese el segundo numero a sumar.</h1>'
        else:
            result = num1 + num2
            return f'<h1>La suma de {num1} y {num2} es: {result}</h1>'

    #! Ruta Hello World
    @app.route('/hello-world')
    def helloWorld():
        return 'Hello World!'

    #! Registro de BluePrints
    from . import todo, auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    #! Migración de modelos que falten a la BBDD
    with app.app_context():
        db.create_all()

    return app
