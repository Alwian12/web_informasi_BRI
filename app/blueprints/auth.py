from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import db
from app.models import User


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
        if user and user.check_password(password):
            if user.status != 'active':
                flash('Akun Anda saat ini tidak aktif.', 'danger')
                return render_template('admin/login.html')
            login_user(user)
            flash('Login berhasil.', 'success')
            return redirect(url_for('admin.dashboard'))

        flash('Email/Username atau password salah.', 'danger')

    return render_template('admin/login.html')


@auth_bp.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('Anda berhasil logout.', 'success')
    return redirect(url_for('auth.login'))
