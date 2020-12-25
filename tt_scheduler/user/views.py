from flask import render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from . import user 
from .forms import EditProfileForm
from .. import db, bcrypt
from ..models import Employee

#User/employee profile
@user.route('/profile',methods=['GET', 'POST'])
@login_required
def editprofile():
    if current_user.is_admin:
        abort(403)

    user = Employee.query.get_or_404(current_user.eid)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.f_name = form.fname.data
        user.m_name = form.mname.data
        user.l_name = form.lname.data
        user.type = form.type.data
        user.workload = form.workload.data
        user.ph_no = form.phno.data
        db.session.commit()
        flash('Profile updated.','success')

        return redirect(url_for('user.editprofile'))

    form.username.data = user.username
    form.email.data = user.email
    form.fname.data = user.f_name
    form.mname.data = user.m_name
    form.lname.data = user.l_name
    form.type.data = user.type
    form.workload.data = user.workload
    form.phno.data = user.ph_no
    return render_template('user/profile.html', form=form, user=user)


