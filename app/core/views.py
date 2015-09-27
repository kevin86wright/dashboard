# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app import app, db
from models import Microapp
from app.core.models import UserProfileForm

core_blueprint = Blueprint('core', __name__, url_prefix='/')


# The Home page is accessible to anyone
@core_blueprint.route('')
def home_page():
    return render_template('core/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@core_blueprint.route('dashboard')
@login_required  # Limits access to authenticated users
def dashboard():
    return render_template('core/dashboard.html')

# The User page is accessible to authenticated users (users that have logged in)
@core_blueprint.route('appstore')
@login_required  # Limits access to authenticated users
def appstore():
    active_microapps = db.session.query(Microapp).filter_by(is_active=True).all()
    return render_template('core/appstore.html', active_microapps=active_microapps)

# The Admin page is accessible to users with the 'admin' role
@core_blueprint.route('admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('core/admin_page.html')


@core_blueprint.route('user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('core.home_page'))

    # Process GET or invalid POST
    return render_template('core/user_profile_page.html',
                           form=form)


# Register blueprint
app.register_blueprint(core_blueprint)
