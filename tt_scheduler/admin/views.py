from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required 

from . import admin




def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403) 


@admin.route('/admin/dashboard')
@login_required
def dashboard():
    check_admin() 
    return render_template('admin/dashboard.html')