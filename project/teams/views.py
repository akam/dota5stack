from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User, TeamUsers
from project.teams.models import Team
from project.users.views import ensure_correct_user
from project.teams.forms import TeamForm
from flask_login import current_user, login_required
from project import db

teams_blueprint = Blueprint(
    'teams',
    __name__,
    template_folder='templates'
)

@teams_blueprint.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = TeamForm(request.form)
        from IPython import embed; embed()
        new_team = Team(
            name = form.name.data,
            prefix = form.prefix.data,
            num_players = current_user.id
        )
        db.session.add(new_team)        
        db.session.commit()
        new_team_member = TeamUsers(
            team_id = new_team.id,
            user_id = current_user.id,
            status = 3,
        )
        db.session.add(new_team_member)
        db.session.commit()
        flash({ 'text': "You have successfully made team {} [{}]!".format(form.name.data,form.prefix.data), 'status': 'success' })
        return redirect(url_for('teams.index'))
    teams = Team.query.all()
    return render_template('teams/index.html', teams=teams)

@teams_blueprint.route('/new')
def new():
    form = TeamForm(request.form)
    return render_template('teams/new.html', form=form)

@teams_blueprint.route('/<int:id>', methods=['GET', 'PATCH'])
def show(id):
    team = Team.query.get(id)
    if request.method == b'PATCH':
        form=TeamForm(request.form)
        if form.validate():
            team.name = form.name.data
            team.prefix = form.prefix.data
            db.session.add(team)
            db.session.commit()
            flash({ 'text': "You have successfully edited the team name to {}!".format(form.name.data), 'status': 'success' })
            return redirect(url_for('teams.show', id=team.id))
        return render_template('teams/edit.html', form=form, team=team)
    found_team = TeamUsers.query.filter_by(team_id=id).all()
    
    found_users = [user.user_id for user in found_team]
    users = User.query.filter(User.id.in_(found_users)).all()
    return render_template('teams/show.html', team=team, users=users)

@teams_blueprint.route('/<int:id>/edit')
def edit(id):
    team = Team.query.get(id)
    if team.num_players != current_user.id:
        flash({'text': "Not Authorized", 'status': 'danger'})
        return redirect(url_for('teams.index'))
    return render_template('teams/edit.html', form=TeamForm(request.form), team=Team.query.get(id))

@teams_blueprint.route('/<int:id>/invite/<int:user_id>', methods=['POST'])
def invite(id, user_id):
    team = Team.query.get(id)
    if team.num_players != current_user.id:
        flash({'text': "Not Authorized", 'status': 'danger'})
        return redirect(url_for('teams.index'))
    

    new_team_member = TeamUsers(
        team_id = id,
        user_id = user_id,
        status = 1,
    )
    db.session.add(new_team_member)
    db.session.commit()
    flash({ 'text': "Invite sent successfully!", 'status': 'success' })
    return redirect(url_for('teams.index'))

