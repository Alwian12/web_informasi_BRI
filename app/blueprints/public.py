from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Announcement, Category, Faq, Feedback, Message, Service, Setting, Visit

public_bp = Blueprint('public', __name__)


@public_bp.before_request
def record_public_visit():
    if request.method == 'GET':
        db.session.add(Visit(path=request.path))
        db.session.commit()


@public_bp.route('/')
def index():
    services = Service.query.filter_by(status='aktif').limit(6).all()
    announcements = Announcement.query.filter_by(status='aktif').order_by(Announcement.created_at.desc()).limit(3).all()
    settings = Setting.query.first()
    return render_template('public/index.html', services=services, announcements=announcements, settings=settings)


@public_bp.route('/about')
def about():
    settings = Setting.query.first()
    return render_template('public/about.html', settings=settings)


@public_bp.route('/services')
def services():
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    services_query = Service.query.filter_by(status='aktif')
    if query:
        like = f'%{query}%'
        services_query = services_query.filter((Service.nama_layanan.ilike(like)) | (Service.deskripsi.ilike(like)))
    if category_id:
        services_query = services_query.filter_by(category_id=category_id)
    categories = Category.query.all()
    services_list = services_query.order_by(Service.created_at.desc()).all()
    settings = Setting.query.first()
    return render_template('public/services.html', services=services_list, categories=categories, settings=settings, selected_category=category_id, q=query)


@public_bp.route('/services/<slug>')
def service_detail(slug):
    service = Service.query.filter_by(slug=slug, status='aktif').first_or_404()
    settings = Setting.query.first()
    return render_template('public/service_detail.html', service=service, settings=settings)


@public_bp.route('/announcements')
def announcements():
    announcements = Announcement.query.filter_by(status='aktif').order_by(Announcement.tanggal_publish.desc()).all()
    settings = Setting.query.first()
    return render_template('public/announcements.html', announcements=announcements, settings=settings)


@public_bp.route('/faq')
def faq():
    faqs = Faq.query.filter_by(status='aktif').order_by(Faq.created_at.desc()).all()
    settings = Setting.query.first()
    return render_template('public/faq.html', faqs=faqs, settings=settings)


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = Setting.query.first()
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        email = request.form.get('email', '').strip()
        telepon = request.form.get('telepon', '').strip()
        subjek = request.form.get('subjek', '').strip()
        pesan = request.form.get('pesan', '').strip()

        if not all([nama, email, subjek, pesan]):
            flash('Semua field wajib diisi.', 'danger')
            return render_template('public/contact.html', settings=settings)

        message = Message(
            nama=nama,
            email=email,
            telepon=telepon,
            subjek=subjek,
            pesan=pesan,
            status='Belum dibaca'
        )
        db.session.add(message)
        db.session.commit()
        flash('Pesan Anda berhasil dikirim. Admin akan menindaklanjuti.', 'success')
        return redirect(url_for('public.contact'))

    return render_template('public/contact.html', settings=settings)


@public_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    settings = Setting.query.first()
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        email = request.form.get('email', '').strip()
        kategori = request.form.get('kategori', '').strip()
        pesan = request.form.get('pesan', '').strip()

        if not all([nama, email, kategori, pesan]):
            flash('Semua field wajib diisi.', 'danger')
            return render_template('public/feedback.html', settings=settings)

        feedback_entry = Feedback(
            nama=nama,
            email=email,
            kategori=kategori,
            pesan=pesan,
        )
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Feedback Anda berhasil dikirim. Terima kasih atas masukan Anda.', 'success')
        return redirect(url_for('public.feedback'))

    return render_template('public/feedback.html', settings=settings)


@public_bp.route('/messages')
def messages():
    """Display public messages submitted by the community"""
    messages_list = Message.query.filter(Message.status.in_(['Terbaca', 'Sudah dibalas'])).order_by(Message.created_at.desc()).all()
    settings = Setting.query.first()
    return render_template('public/messages.html', messages=messages_list, settings=settings)
