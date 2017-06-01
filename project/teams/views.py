from flask import redirect, render_template, request, url_for, Blueprint 
# from project.messages.models import Message
from project.users.models import User
from project.users.views import ensure_correct_user
# from project.messages.forms import MessageForm
from flask_login import current_user, login_required
from project import db

teams_blueprint = Blueprint(
    'teams',
    __name__,
    template_folder='templates'
)

@teams_blueprint.route('/')
def index():
    return render_template('teams/index.html')