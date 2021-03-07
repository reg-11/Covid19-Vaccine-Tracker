from flask import Blueprint, render_remplate


main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('home.html')

@main.route('/profil')