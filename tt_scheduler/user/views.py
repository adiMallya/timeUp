from flask import render_template, abort
from flask_login import login_required, current_user

from . import user 

#User/employee profile
@user.route('/profile')
@login_required
def homepage():
    if current_user.is_admin:
        abort(403)
    return render_template('user/profile.html')