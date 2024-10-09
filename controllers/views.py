from flask import Blueprint, render_template

views_controller = Blueprint('views_controller', __name__)

@views_controller.route('/header')
def header():
    return render_template('header.html')