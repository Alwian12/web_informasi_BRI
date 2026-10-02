import pytest

from app import create_app
from app.models import Announcement, Category, Faq, Message, Service, User


@pytest.fixture
def app():
    application = create_app()
    application.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_app_factory_import():
    app = create_app()
    assert app is not None
    assert app.name == 'app'


def test_public_pages_are_available(client):
    for path in ['/', '/about', '/services', '/announcements', '/faq', '/contact', '/feedback']:
        assert client.get(path).status_code == 200


def test_admin_requires_login(client):
    response = client.get('/admin/dashboard')
    assert response.status_code == 302
    assert '/admin/login' in response.location


def test_admin_login_and_edit_pages(client, app):
    login = client.post(
        '/admin/login',
        data={'identifier': 'admin', 'password': 'admin123'},
        follow_redirects=True,
    )
    assert login.status_code == 200

    with app.app_context():
        ids = {
            'service': Service.query.first().id,
            'category': Category.query.first().id,
            'announcement': Announcement.query.first().id,
            'faq': Faq.query.first().id,
            'user': User.query.filter_by(username='admin').first().id,
        }

    edit_paths = [
        f"/admin/services/{ids['service']}/edit",
        f"/admin/categories/{ids['category']}/edit",
        f"/admin/announcements/{ids['announcement']}/edit",
        f"/admin/faqs/{ids['faq']}/edit",
        f"/admin/users/{ids['user']}/edit",
    ]
    for path in edit_paths:
        assert client.get(path).status_code == 200


def test_admin_delete_pages_use_custom_confirmation(client):
    client.post(
        '/admin/login',
        data={'identifier': 'admin', 'password': 'admin123'},
        follow_redirects=True,
    )

    paths = ['/admin/services', '/admin/categories', '/admin/announcements', '/admin/faqs', '/admin/feedback']
    for path in paths:
        response = client.get(path)

        assert response.status_code == 200
        assert b'id="deleteConfirmModal"' in response.data
        assert b'return confirm(' not in response.data


def test_admin_reply_sends_email_and_marks_message_replied(client, app, monkeypatch):
    client.post(
        '/admin/login',
        data={'identifier': 'admin', 'password': 'admin123'},
        follow_redirects=True,
    )

    with app.app_context():
        message = Message(
            nama='Budi',
            email='budi@example.com',
            telepon='081234567890',
            subjek='Pertanyaan layanan',
            pesan='Saya ingin bertanya tentang simpanan.',
            status='Belum dibaca',
        )
        from app import db
        db.session.add(message)
        db.session.commit()
        message_id = message.id

    app.config.update(
        MAIL_SERVER='smtp.example.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='unitindrapura@example.com',
        MAIL_PASSWORD='secret',
        MAIL_DEFAULT_SENDER='unitindrapura@example.com',
    )

    class DummySMTP:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.sent = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            pass

        def login(self, username, password):
            pass

        def sendmail(self, from_addr, to_addrs, msg):
            self.sent = (from_addr, to_addrs, msg)
            return {}

    dummy = DummySMTP('smtp.example.com', 587)
    monkeypatch.setattr('smtplib.SMTP', lambda *args, **kwargs: dummy)

    response = client.post(
        f'/admin/messages/{message_id}/reply',
        data={'reply': 'Halo Budi, silakan datang ke unit kami.'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    with app.app_context():
        updated = Message.query.get(message_id)
        assert updated.reply == 'Halo Budi, silakan datang ke unit kami.'
        assert updated.status == 'Sudah dibalas'
        assert dummy.sent is not None
        assert 'budi@example.com' in dummy.sent[1]
