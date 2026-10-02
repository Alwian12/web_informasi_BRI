from app import db
from app.models import Announcement, Category, Faq, Message, Service, Setting, User


def seed_database():
    if User.query.first() is None:
        admin = User(name='Administrator', username='admin', email='admin@indrapura.com')
        admin.set_password('admin123')
        admin.role = 'super_admin'
        admin.status = 'active'
        db.session.add(admin)

    if Category.query.count() == 0:
        categories = [
            Category(nama_kategori='Simpanan', deskripsi='Layanan simpanan dan tabungan.'),
            Category(nama_kategori='Kredit', deskripsi='Layanan pembiayaan dan kredit.'),
            Category(nama_kategori='Digital Banking', deskripsi='Layanan digital banking.'),
            Category(nama_kategori='Transaksi', deskripsi='Layanan transaksi harian.'),
        ]
        db.session.add_all(categories)

    if Service.query.count() == 0:
        cat_map = {c.nama_kategori: c for c in Category.query.all()}
        services = [
            Service(category_id=cat_map['Simpanan'].id, nama_layanan='Tabungan Reguler', slug='tabungan-reguler', deskripsi='Tabungan untuk kebutuhan sehari-hari masyarakat.', persyaratan='KTP, KK, formulir pengisian', prosedur='1. Datang ke unit\n2. Isi formulir\n3. Verifikasi dokumen\n4. Aktivasi rekening', estimasi_waktu='15-30 Menit', status='aktif'),
            Service(category_id=cat_map['Simpanan'].id, nama_layanan='Deposito', slug='deposito', deskripsi='Produk deposito dengan tenor fleksibel.', persyaratan='KTP, NPWP, saldo awal', prosedur='1. Konsultasi produk\n2. Verifikasi data\n3. Setor dana\n4. Penutupan akad', estimasi_waktu='30-45 Menit', status='aktif'),
            Service(category_id=cat_map['Kredit'].id, nama_layanan='Kredit Usaha', slug='kredit-usaha', deskripsi='Pembiayaan modal usaha mikro dan kecil.', persyaratan='KTP, proposal usaha, dokumen pendukung', prosedur='1. Ajukan permohonan\n2. Verifikasi usaha\n3. Survey calon debitur\n4. Persetujuan', estimasi_waktu='3-7 Hari', status='aktif'),
            Service(category_id=cat_map['Kredit'].id, nama_layanan='Kredit Konsumtif', slug='kredit-konsumtif', deskripsi='Pembiayaan untuk kebutuhan konsumsi prioritas.', persyaratan='KTP, slip gaji, dokumen pendukung', prosedur='1. Pengajuan\n2. Verifikasi\n3. Analisa\n4. Pencairan', estimasi_waktu='2-5 Hari', status='aktif'),
            Service(category_id=cat_map['Digital Banking'].id, nama_layanan='Mobile Banking', slug='mobile-banking', deskripsi='Layanan transaksi digital via smartphone.', persyaratan='Rekening aktif, ponsel, nomor handphone', prosedur='1. Daftar aplikasi\n2. Aktivasi akun\n3. Registrasi otp\n4. Gunakan layanan', estimasi_waktu='10-20 Menit', status='aktif'),
            Service(category_id=cat_map['Digital Banking'].id, nama_layanan='Internet Banking', slug='internet-banking', deskripsi='Akses transaksi perbankan melalui website resmi.', persyaratan='Rekening aktif, email aktif', prosedur='1. Daftar\n2. Verifikasi\n3. Aktivasi\n4. Login', estimasi_waktu='15-25 Menit', status='aktif'),
            Service(category_id=cat_map['Digital Banking'].id, nama_layanan='ATM', slug='atm', deskripsi='Layanan tarik tunai dan transaksi mandiri.', persyaratan='Kartu ATM, PIN aktif', prosedur='1. Masukkan kartu\n2. Input PIN\n3. Pilih layanan\n4. Selesaikan transaksi', estimasi_waktu='5-10 Menit', status='aktif'),
            Service(category_id=cat_map['Transaksi'].id, nama_layanan='Transfer', slug='transfer', deskripsi='Transfer antar rekening dan antar bank.', persyaratan='Rekening, data penerima, nominal', prosedur='1. Login atau datang ke teller\n2. Isi data transfer\n3. Konfirmasi\n4. Proses selesai', estimasi_waktu='5-15 Menit', status='aktif'),
            Service(category_id=cat_map['Transaksi'].id, nama_layanan='Setor Tunai', slug='setor-tunai', deskripsi='Setor tunai untuk berbagai keperluan nasabah.', persyaratan='Uang tunai, rekening aktif', prosedur='1. Ambil antrean\n2. Serahkan uang\n3. Verifikasi\n4. Selesai', estimasi_waktu='10-20 Menit', status='aktif'),
            Service(category_id=cat_map['Transaksi'].id, nama_layanan='Tarik Tunai', slug='tarik-tunai', deskripsi='Layanan penarikan tunai sesuai kebutuhan.', persyaratan='Kartu atm atau rekening', prosedur='1. Ambil antrean\n2. Verifikasi identitas\n3. Proses pencairan\n4. Selesai', estimasi_waktu='10-15 Menit', status='aktif'),
        ]
        db.session.add_all(services)

    if Announcement.query.count() == 0:
        announcements = [
            Announcement(judul='Peningkatan Layanan Mobile Banking', slug='peningkatan-layanan-mobile-banking', isi='Layanan mobile banking mengalami pembaruan pada keamanan transaksi dan fitur transfer.', gambar='', status='aktif'),
            Announcement(judul='Jam Operasional Khusus', slug='jam-operasional-khusus', isi='Unit Indrapura tetap melayani masyarakat pada jam kerja hari Senin sampai Jumat.', gambar='', status='aktif'),
            Announcement(judul='Program Pembukaan Rekening Baru', slug='program-pembukaan-rekening-baru', isi='Program khusus pembukaan rekening baru untuk kebutuhan masyarakat dan UMKM.', gambar='', status='aktif'),
            Announcement(judul='Pelatihan Digital Banking', slug='pelatihan-digital-banking', isi='Unit Indrapura menyelenggarakan sesi edukasi penggunaan layanan digital banking.', gambar='', status='aktif'),
            Announcement(judul='Kebijakan Pelayanan Baru', slug='kebijakan-pelayanan-baru', isi='Pelayanan nasabah akan diperkuat dengan sistem antrean digital.', gambar='', status='aktif'),
        ]
        db.session.add_all(announcements)

    if Faq.query.count() == 0:
        faqs = [
            Faq(pertanyaan='Bagaimana cara membuka rekening?', jawaban='Nasabah dapat datang ke unit dengan membawa KTP, KK, dan mengisi formulir pembukaan rekening.', status='aktif'),
            Faq(pertanyaan='Apa saja persyaratan pengajuan layanan?', jawaban='Persyaratan akan disesuaikan dengan jenis layanan yang dipilih. Umumnya meliputi KTP, KK, dokumen pendukung, dan formulir.', status='aktif'),
            Faq(pertanyaan='Bagaimana jam operasional Unit?', jawaban='Jam operasional Unit Indrapura adalah Senin - Jumat pukul 08.00 - 16.00 WIB.', status='aktif'),
            Faq(pertanyaan='Apakah tersedia layanan digital?', jawaban='Ya, tersedia layanan mobile banking, internet banking, dan ATM.', status='aktif'),
            Faq(pertanyaan='Bagaimana cara menghubungi petugas?', jawaban='Anda dapat menggunakan formulir kontak atau menelepon nomor yang tertera di halaman kontak.', status='aktif'),
            Faq(pertanyaan='Apakah layanan kredit tersedia untuk UMKM?', jawaban='Ya, tersedia program kredit usaha dan pembiayaan usaha untuk UMKM.', status='aktif'),
            Faq(pertanyaan='Berapa estimasi waktu pelayanan?', jawaban='Waktu pelayanan tergantung layanan yang dipilih, biasanya berkisar antara 15 menit hingga beberapa hari.', status='aktif'),
            Faq(pertanyaan='Apakah saya bisa meminta informasi via website?', jawaban='Tentu, seluruh informasi layanan tersedia di website resmi Unit Indrapura.', status='aktif'),
            Faq(pertanyaan='Apakah ada layanan untuk setoran tunai?', jawaban='Ya, tersedia layanan setor tunai dan tarik tunai di Unit Indrapura.', status='aktif'),
            Faq(pertanyaan='Apakah saya dapat mengirim kritik dan saran?', jawaban='Anda dapat mengirim kritik dan saran melalui formulir kontak di halaman Kontak.', status='aktif'),
        ]
        db.session.add_all(faqs)

    if Message.query.count() == 0:
        messages = [
            Message(nama='Rina', email='rina@gmail.com', telepon='081234567890', subjek='Informasi Tabungan', pesan='Saya ingin menanyakan syarat membuka rekening tabungan baru. Unit Indrapura sangat membantu dalam memberikan informasi layanan perbankan.', status='Terbaca'),
            Message(nama='Budi', email='budi@gmail.com', telepon='082345678901', subjek='Kredit Usaha untuk UMKM', pesan='Apakah ada pembiayaan untuk usaha kecil dan menengah? Saya tertarik dengan program kredit usaha yang ditawarkan.', status='Terbaca'),
            Message(nama='Sari', email='sari@gmail.com', telepon='083456789012', subjek='Mobile Banking Mudah Digunakan', pesan='Bagaimana cara aktivasi layanan mobile banking? Website ini sangat informatif dan memudahkan saya mencari informasi.', status='Terbaca'),
            Message(nama='Ahmad Wijaya', email='ahmad.wijaya@gmail.com', telepon='084567890123', subjek='Kepuasan Pelayanan Teller', pesan='Staf Unit Indrapura sangat profesional dan membantu. Pelayanan yang diberikan sangat cepat dan memuaskan.', status='Terbaca'),
            Message(nama='Dewi Kusuma', email='dewi.kusuma@gmail.com', telepon='085678901234', subjek='Program Transfer Antar Bank', pesan='Terimakasih atas layanan transfer antar bank yang cepat dan terpercaya. Sangat membantu dalam kebutuhan transaksi saya.', status='Terbaca'),
        ]
        db.session.add_all(messages)

    if Setting.query.count() == 0:
        setting = Setting(
            nama_instansi='Unit Indrapura',
            alamat='Jl. Indrapura No. 12, Kecamatan Indrapura, Sumatera Barat',
            telepon='(0751) 123456',
            email='info@unitindrapura.com',
            jam_operasional='Senin - Jumat: 08.00 - 16.00 WIB',
            maps='<iframe src="https://www.google.com/maps?q=indrapura&output=embed" width="100%" height="250" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
        )
        db.session.add(setting)

    db.session.commit()
