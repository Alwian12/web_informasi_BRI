# Analisis Sistem

## Tujuan Sistem
- Menyediakan informasi pelayanan perbankan secara digital.
- Memudahkan masyarakat mengakses layanan, persyaratan, dan jadwal operasional.
- Mengurangi komunikasi manual serta meningkatkan efisiensi pelayanan.

## Identifikasi Pengguna
### Pengunjung/Masyarakat
- Melihat layanan
- Mencari informasi
- Mengirim pertanyaan dan feedback

### Administrator
- Login ke dashboard
- Mengelola layanan, kategori, pengumuman, FAQ, pesan, dan pengaturan

## Fitur Utama
- Public website
- Search dan filter layanan
- FAQ accordion
- Form kontak dan feedback
- Dashboard admin
- CRUD data

## Use Case
```text
Pengunjung -> Website -> Lihat layanan -> Detail layanan -> Informasi dan persyaratan
Pengunjung -> Kontak -> Kirim pesan -> Admin menerima pesan
Admin -> Login -> Dashboard -> Kelola data -> Simpan ke database
```

## Flowchart Pengunjung
```mermaid
flowchart TD
    A[Start] --> B[Membuka Website]
    B --> C[Masuk Halaman Beranda]
    C --> D[Memilih Menu]
    D --> E{Memilih Layanan?}
    E -- Ya --> F[Menampilkan Daftar Layanan]
    F --> G[Memilih Layanan]
    G --> H[Menampilkan Detail Layanan]
    H --> I[Melihat Persyaratan & Prosedur]
    I --> J[End]
    E -- Tidak --> K[Memilih Menu Lain]
    K --> L[Menampilkan Informasi]
    L --> J
```

## Flowchart Administrator
```mermaid
flowchart TD
    A[Start] --> B[Admin buka login]
    B --> C[Masukkan username dan password]
    C --> D[Validasi Login]
    D --> E{Data benar?}
    E -- Tidak --> F[Tampilkan login gagal]
    F --> B
    E -- Ya --> G[Masuk Dashboard]
    G --> H[Memilih menu manajemen]
    H --> I{Mengelola data?}
    I -- Ya --> J[Tambah/Edit/Hapus data]
    J --> K[Simpan perubahan]
    K --> L[Database diperbarui]
    L --> M[Dashboard]
    M --> N[Logout]
    N --> O[End]
```

## ERD Database
```mermaid
erDiagram
    USERS ||--o{ SERVICES : manages
    CATEGORIES ||--o{ SERVICES : contains
    SERVICES ||--o{ ANNOUNCEMENTS : related
    USERS ||--o{ MESSAGES : receives
    USERS ||--o{ FAQS : manages
    USERS ||--o{ FEEDBACK : manages
    SETTINGS ||--o| USERS : config
```

## Struktur Folder
- app/
- blueprints/
- models/
- templates/
- static/
- config.py
- run.py
