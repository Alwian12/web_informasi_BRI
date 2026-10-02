# Website Informasi Pelayanan Perbankan Unit Indrapura

Aplikasi web informasi pelayanan perbankan berbasis Flask untuk Unit Indrapura.

## Fitur utama
- Public website: beranda, profil, layanan, pengumuman, FAQ, kontak, feedback
- Admin dashboard dengan login session
- CRUD untuk layanan, kategori, pengumuman, FAQ, pesan, feedback, pengaturan
- Database MySQL yang dapat dihubungkan melalui SQLAlchemy
- Responsive design modern dan profesional

## Struktur project
```text
project_perbankan/
├─ app/
│  ├─ blueprints/
│  │  ├─ admin.py
│  │  ├─ auth.py
│  │  ├─ public.py
│  │  └─ __init__.py
│  ├─ static/
│  │  ├─ css/style.css
│  │  └─ js/main.js
│  ├─ templates/
│  │  ├─ admin/
│  │  └─ public/
│  ├─ models/
│  │  └─ __init__.py
│  ├─ __init__.py
│  ├─ config.py
│  └─ seed.py
├─ tests/
│  └─ test_app.py
├─ .env.example
├─ requirements.txt
├─ run.py
└─ README.md
```

## Persiapan lingkungan
1. Pastikan Python 3.10+ sudah terinstal.
2. Instal dependency:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Buat database MySQL dengan nama `db_pelayanan_perbankan`.
4. Sesuaikan konfigurasi database di `.env` atau `.env.example`.

## Konfigurasi database
Contoh `.env`:
```env
SECRET_KEY=supersecretkey
DATABASE_URL=mysql+pymysql://root:@localhost:3306/db_pelayanan_perbankan
FLASK_ENV=development
```

## Menjalankan aplikasi
```bash
python run.py
```

Atau:
```bash
flask run
```

## Mengatur SMTP email balasan
Balasan admin tetap disimpan ke database meskipun SMTP belum dikonfigurasi. Agar masyarakat menerima balasan melalui email, isi variabel berikut di file `.env`:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=alamat-email-anda@gmail.com
MAIL_PASSWORD=app-password-gmail
MAIL_DEFAULT_SENDER=alamat-email-anda@gmail.com
```

Untuk Gmail, gunakan **App Password**, bukan password akun utama. Setelah mengubah `.env`, restart aplikasi dengan `python run.py`.

## Login admin
- URL: `/admin/login`
- Username/email: `admin@indrapura.com`
- Password: `admin123`

## Catatan
Aplikasi ini sudah dibuat dengan basis struktur Flask profesional dan dapat dikembangkan lebih lanjut sesuai kebutuhan operasional Unit Indrapura.
