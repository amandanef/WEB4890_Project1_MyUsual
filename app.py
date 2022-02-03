# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

import datetime
from flask import Flask, request, render_template
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

    # Flask-User settings
    USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"


def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize Flask-BabelEx
    babel = Babel(app)

    # Initialize Flask-SQLAlchemy
    db = SQLAlchemy(app)

    # Define the User data-model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
        first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

        # Define the relationship to Role via UserRoles
        roles = db.relationship('Role', secondary='user_roles')

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.create_all()

    # Create 'member@example.com' user with no roles
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(
            email='member@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
        )
        db.session.add(user)
        db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(
            email='admin@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()

    class Meals(db.Model):
        __tablename__ = 'meals'
        id = db.Column(db.Integer(), primary_key = True)
        title = db.Column(db.String(50), unique = True)
        restaurant = db.Column(db.String(50))
        tags = db.Column(db.String(50))
        description = db.Column(db.String(50))
        tryAgain = db.Column(db.String(50))
        starRating = db.Column(db.Integer())





    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template("index.html")

    # The Admin page requires an 'Admin' role
    @app.route('/admin')
    @roles_required('Admin')
    def admin_page():
        return render_template('admin.html')

    # Seeds the Database (admins only)
    @app.route('/seedDB')
   # @roles_required('Admin')
    def seedDB():
        db.drop_all()
        db.create_all()
        tonkatsu = Meals(title='Tonkatsu Ramen', restaurant="Nikko's", description="This dish was a perfect bowl of ramen. The pork was cooked perfectly and the broth was good too.", tags="affordable, leftovers, Japanese", tryAgain="Yes", starRating="5")
        pasta = Meals(title='Seafood Pasta', restaurant="Olive Garden", description="The meal was good but there wasn't as much seafood as I was hoping for. Would feel like more value for the price if they added some more in.", tags="pricey, small portion size, Italian", tryAgain="Maybe", starRating="3")
        cupBop = Meals(title='Rock Bop', restaurant="Cup Bop", description="This dish was way too spicy for my taste! I could barely task any of the food because my mouth burned.", tags="Korean, spicy, noodles", tryAgain="No", starRating="1")
   
        db.session.add(tonkatsu)
        db.session.add(pasta)
        db.session.add(cupBop)
       
        db.session.commit()
          

        return '<h1>DB Seeded!</h1>'
    # Erase the Database (admins only)
    @app.route('/erase_DB')
    @roles_required('Admin')
    def eraseDB():
        meals = Meals.query.all()
        db.session.delete(meals)
        db.session.commit()
        return '<h1>DB Erased!</h1>'
    # View All Books
    @app.route('/all_meals')
    @login_required
    def all_meals():
            meals = Meals.query.all()            
            my_list_of_meals = [row for row in meals]
               
            return render_template('all_meals.html', meals=my_list_of_meals)

    @app.context_processor
    def utility_processor():
        def isAdmin(user):
            sqlStatement = "Select roles.name FROM roles JOIN user_roles ON roles.id=user_roles.role_id JOIN users ON users.id=user_id WHERE users.email='" + user + "' AND roles.name='Admin'"
            roleName = db.engine.execute(sqlStatement)
            roleName = [row for row in roleName]
            if len(roleName) > 0 and roleName[0]['name'] == 'Admin':
                returnValue = 1
            else:
                returnValue = 0
            return returnValue
        return dict(isAdmin=isAdmin)

    @app.route('/add_meal', methods={'GET','POST'})
    def addmeal():
            if request.method == 'POST':
                    restaurant = request.form['restaurant']
                    title = request.form['title']
                    description = request.form['description']
                    tags = request.form['tags']
                    tryAgain = request.form['tryAgain']
                    starRating = request.form['starRating']

                   # search = Meals.query.filter(Meals.author =='?')
                    newMeal = Meals(title=title, restaurant=restaurant, description=description, tags=tags, tryAgain=tryAgain, starRating=starRating)
    
                    #CHANGE THIS TO BE TITLE AND RESTAURANT EQUIVELENAT
                    # if len(search) > 0:
                    #     return '<h2>That meal title already exists, please select another.</h2>'
                    # else:
                    #     newMeal = Meals(title=title, author=author, description=description)
                    #     db.session.add(newMeal)
                    #     db.session.commit()

                    #     return render_template('add_meal.html', meal_title = title)
                    
                    db.session.add(newMeal)
                    db.session.commit()

            return render_template('add_meal.html', meal_title = "")




    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)