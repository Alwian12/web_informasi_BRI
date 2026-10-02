import smtplib
from datetime import datetime
from email.message import EmailMessage

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Announcement, Category, Faq, Feedback, Message, Service, Setting, User, Visit

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def admin_entry():
    if current_user.is_authenticated and current_user.role in ['admin', 'super_admin']:
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))


def admin_required(func):
    from functools import wraps

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'super_admin']:
            flash('Anda tidak memiliki akses ke halaman ini.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return wrapper


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    months = []
    for offset in range(5, -1, -1):
        month_index = current_month.month - offset
        year = current_month.year + (month_index - 1) // 12
        month = (month_index - 1) % 12 + 1
        months.append(datetime(year, month, 1))

    visits = Visit.query.all()
    messages = Message.query.all()
    visitor_values = [sum(item.created_at.year == month.year and item.created_at.month == month.month for item in visits) for month in months]
    message_values = [sum(item.created_at.year == month.year and item.created_at.month == month.month for item in messages) for month in months]
    visitor_max = max(visitor_values or [1])
    chart_points = ' '.join(f'{index * 20},{100 - (value / visitor_max * 82):.1f}' for index, value in enumerate(visitor_values))
    message_max = max(message_values or [1])
    chart_labels = [month.strftime('%b') for month in months]
    stats = {
        'services': Service.query.count(),
        'announcements': Announcement.query.count(),
        'faqs': Faq.query.count(),
        'messages': Message.query.count(),
        'waiting_replies': Message.query.filter(Message.status == 'Terbaca', Message.reply.is_(None)).count(),
        'unread_messages': Message.query.filter_by(status='Belum dibaca').count(),
    }
    recent_services = Service.query.order_by(Service.created_at.desc()).limit(5).all()
    recent_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()
    recent_announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_services=recent_services,
        recent_messages=recent_messages,
        recent_announcements=recent_announcements,
        chart_labels=chart_labels,
        visitor_values=visitor_values,
        message_values=message_values,
        message_max=message_max,
        chart_points=chart_points,
    )


@admin_bp.route('/services', methods=['GET', 'POST'])
@admin_required
def services():
    categories = Category.query.all()
    if request.method == 'POST':
        service = Service(
            category_id=request.form.get('category_id'),
            nama_layanan=request.form.get('nama_layanan'),
            slug=request.form.get('slug') or request.form.get('nama_layanan').lower().replace(' ', '-'),
            deskripsi=request.form.get('deskripsi'),
            persyaratan=request.form.get('persyaratan'),
            prosedur=request.form.get('prosedur'),
            estimasi_waktu=request.form.get('estimasi_waktu'),
            status=request.form.get('status', 'aktif')
        )
        db.session.add(service)
        db.session.commit()
        flash('Layanan berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.services'))
    all_services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template('admin/services.html', services=all_services, categories=categories)


@admin_bp.route('/services/<int:service_id>/delete', methods=['POST'])
@admin_required
def delete_service(service_id):
    service = db.get_or_404(Service, service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Layanan berhasil dihapus.', 'success')
    return redirect(url_for('admin.services'))


@admin_bp.route('/services/<int:service_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_service(service_id):
    service = db.get_or_404(Service, service_id)
    categories = Category.query.order_by(Category.nama_kategori).all()
    if request.method == 'POST':
        service.category_id = request.form.get('category_id', type=int)
        service.nama_layanan = request.form.get('nama_layanan', '').strip()
        service.slug = request.form.get('slug', '').strip() or service.slug
        service.deskripsi = request.form.get('deskripsi', '').strip()
        service.persyaratan = request.form.get('persyaratan', '').strip()
        service.prosedur = request.form.get('prosedur', '').strip()
        service.estimasi_waktu = request.form.get('estimasi_waktu', '').strip()
        service.status = request.form.get('status', 'aktif')
        db.session.commit()
        flash('Layanan berhasil diperbarui.', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_edit.html', service=service, categories=categories)


@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    if request.method == 'POST':
        category = Category(nama_kategori=request.form.get('nama_kategori'), deskripsi=request.form.get('deskripsi'))
        db.session.add(category)
        db.session.commit()
        flash('Kategori berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.categories'))
    all_categories = Category.query.order_by(Category.created_at.desc()).all()
    return render_template('admin/categories.html', categories=all_categories)


@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@admin_required
def delete_category(category_id):
    category = db.get_or_404(Category, category_id)
    if category.services:
        flash('Kategori tidak dapat dihapus karena masih memiliki layanan.', 'danger')
        return redirect(url_for('admin.categories'))
    db.session.delete(category)
    db.session.commit()
    flash('Kategori berhasil dihapus.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    category = db.get_or_404(Category, category_id)
    if request.method == 'POST':
        category.nama_kategori = request.form.get('nama_kategori', '').strip()
        category.deskripsi = request.form.get('deskripsi', '').strip()
        db.session.commit()
        flash('Kategori berhasil diperbarui.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_edit.html', category=category)


@admin_bp.route('/announcements', methods=['GET', 'POST'])
@admin_required
def announcements():
    if request.method == 'POST':
        announcement = Announcement(
            judul=request.form.get('judul'),
            slug=request.form.get('slug') or request.form.get('judul').lower().replace(' ', '-'),
            isi=request.form.get('isi'),
            gambar=request.form.get('gambar'),
            status=request.form.get('status', 'aktif'),
            tanggal_publish=datetime.utcnow(),
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Pengumuman berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.announcements'))
    all_announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=all_announcements)


@admin_bp.route('/announcements/<int:announcement_id>/delete', methods=['POST'])
@admin_required
def delete_announcement(announcement_id):
    announcement = db.get_or_404(Announcement, announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    flash('Pengumuman berhasil dihapus.', 'success')
    return redirect(url_for('admin.announcements'))


@admin_bp.route('/announcements/<int:announcement_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_announcement(announcement_id):
    announcement = db.get_or_404(Announcement, announcement_id)
    if request.method == 'POST':
        announcement.judul = request.form.get('judul', '').strip()
        announcement.slug = request.form.get('slug', '').strip() or announcement.slug
        announcement.isi = request.form.get('isi', '').strip()
        announcement.gambar = request.form.get('gambar', '').strip()
        announcement.status = request.form.get('status', 'aktif')
        db.session.commit()
        flash('Pengumuman berhasil diperbarui.', 'success')
        return redirect(url_for('admin.announcements'))
    return render_template('admin/announcement_edit.html', announcement=announcement)


@admin_bp.route('/faqs', methods=['GET', 'POST'])
@admin_required
def faqs():
    if request.method == 'POST':
        faq = Faq(
            pertanyaan=request.form.get('pertanyaan'),
            jawaban=request.form.get('jawaban'),
            status=request.form.get('status', 'aktif')
        )
        db.session.add(faq)
        db.session.commit()
        flash('FAQ berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.faqs'))
    all_faqs = Faq.query.order_by(Faq.created_at.desc()).all()
    return render_template('admin/faqs.html', faqs=all_faqs)


@admin_bp.route('/faqs/<int:faq_id>/delete', methods=['POST'])
@admin_required
def delete_faq(faq_id):
    faq = db.get_or_404(Faq, faq_id)
    db.session.delete(faq)
    db.session.commit()
    flash('FAQ berhasil dihapus.', 'success')
    return redirect(url_for('admin.faqs'))


@admin_bp.route('/faqs/<int:faq_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_faq(faq_id):
    faq = db.get_or_404(Faq, faq_id)
    if request.method == 'POST':
        faq.pertanyaan = request.form.get('pertanyaan', '').strip()
        faq.jawaban = request.form.get('jawaban', '').strip()
        faq.status = request.form.get('status', 'aktif')
        db.session.commit()
        flash('FAQ berhasil diperbarui.', 'success')
        return redirect(url_for('admin.faqs'))
    return render_template('admin/faq_edit.html', faq=faq)


@admin_bp.route('/feedback')
@admin_required
def feedback():
    all_feedback = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('admin/feedback.html', feedbacks=all_feedback)


@admin_bp.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
@admin_required
def delete_feedback(feedback_id):
    feedback = db.get_or_404(Feedback, feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback berhasil dihapus.', 'success')
    return redirect(url_for('admin.feedback'))


@admin_bp.route('/messages')
@admin_required
def messages():
    all_messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_messages)


@admin_bp.route('/messages/<int:message_id>/status', methods=['POST'])
@admin_required
def update_message_status(message_id):
    message = db.get_or_404(Message, message_id)
    message.status = request.form.get('status', 'Belum dibaca')
    db.session.commit()
    flash('Status pesan berhasil diperbarui.', 'success')
    return redirect(url_for('admin.messages'))


def _send_reply_email(message, reply_text):
    mail_server = current_app.config.get('MAIL_SERVER', '').strip()
    if not mail_server:
        return False

    setting = Setting.query.first()
    sender = (setting.email if setting and setting.email else current_app.config.get('MAIL_DEFAULT_SENDER', 'info@unitindrapura.com')).strip()
    subject = f'Re: {message.subjek}'
    body = (
        f"Halo {message.nama},\n\n"
        f"Terima kasih atas pesan Anda dengan subjek '{message.subjek}'.\n\n"
        "Balasan dari Unit Indrapura:\n\n"
        f"{reply_text}\n\n"
        "Semoga informasi ini bermanfaat.\n\n"
        "Salam hangat,\n"
        "Unit Indrapura"
    )

    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = message.email
    email.set_content(body)

    with smtplib.SMTP(mail_server, current_app.config.get('MAIL_PORT', 587)) as server:
        if current_app.config.get('MAIL_USE_TLS'):
            server.starttls()

        username = current_app.config.get('MAIL_USERNAME', '')
        password = current_app.config.get('MAIL_PASSWORD', '')
        if username and password:
            server.login(username, password)

        server.sendmail(sender, [message.email], email.as_string())

    return True


@admin_bp.route('/messages/<int:message_id>/reply', methods=['POST'])
@admin_required
def reply_message(message_id):
    message = db.get_or_404(Message, message_id)
    reply_text = request.form.get('reply', '').strip()

    if not reply_text:
        flash('Balasan tidak boleh kosong.', 'danger')
        return redirect(url_for('admin.messages'))

    message.reply = reply_text
    message.replied_at = datetime.utcnow()
    message.status = 'Sudah dibalas'
    db.session.commit()

    try:
            email_sent = _send_reply_email(message, reply_text)
            if email_sent:
                flash('Balasan berhasil disimpan dan email notifikasi telah dikirim.', 'success')
            else:
                flash('Balasan berhasil disimpan, tetapi SMTP belum dikonfigurasi sehingga email belum dikirim.', 'warning')
    except smtplib.SMTPAuthenticationError:
        flash('Balasan tersimpan, tetapi Gmail menolak login SMTP. Periksa email dan App Password Gmail di file .env.', 'warning')
    except Exception:
        flash('Balasan berhasil disimpan, tetapi pengiriman email gagal. Silakan cek pengaturan SMTP.', 'warning')

    return redirect(url_for('admin.messages'))


@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    setting = Setting.query.first()
    if request.method == 'POST':
        if not setting:
            setting = Setting()
        setting.nama_instansi = request.form.get('nama_instansi')
        setting.alamat = request.form.get('alamat')
        setting.telepon = request.form.get('telepon')
        setting.email = request.form.get('email')
        setting.jam_operasional = request.form.get('jam_operasional')
        setting.maps = request.form.get('maps')
        db.session.add(setting)
        db.session.commit()
        flash('Pengaturan berhasil diperbarui.', 'success')
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html', setting=setting)


@admin_bp.route('/users')
@admin_required
def users():
    if current_user.role != 'super_admin':
        flash('Hanya super admin yang dapat mengakses daftar admin.', 'danger')
        return redirect(url_for('admin.dashboard'))
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/add', methods=['POST'])
@admin_required
def add_user():
    if current_user.role != 'super_admin':
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('admin.dashboard'))
    user = User(
        name=request.form.get('name'),
        username=request.form.get('username'),
        email=request.form.get('email'),
        role=request.form.get('role', 'admin'),
        status=request.form.get('status', 'active')
    )
    user.set_password(request.form.get('password'))
    db.session.add(user)
    db.session.commit()
    flash('Admin baru berhasil ditambahkan.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    if current_user.role != 'super_admin':
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('admin.dashboard'))
    user = db.get_or_404(User, user_id)
    if request.method == 'POST':
        role = request.form.get('role', 'admin')
        status = request.form.get('status', 'active')
        if user.id == current_user.id and (role != 'super_admin' or status != 'active'):
            flash('Akun super admin yang sedang digunakan harus tetap aktif.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user.id))
        user.name = request.form.get('name', '').strip()
        user.email = request.form.get('email', '').strip()
        user.role = role
        user.status = status
        password = request.form.get('password', '')
        if password:
            user.set_password(password)
        db.session.commit()
        flash('Akun admin berhasil diperbarui.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_edit.html', user=user)
