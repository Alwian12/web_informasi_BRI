import os
os.environ['FLASK_ENV'] = 'development'

import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect directly to database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='db_pelayanan_perbankan'
)

cursor = connection.cursor()

# Drop old messages table
try:
    cursor.execute('DROP TABLE IF EXISTS messages')
    connection.commit()
    print("✓ Old messages table dropped")
except Exception as e:
    print(f"Note: {e}")

connection.close()

# Now load app and create tables
from app import create_app, db
from app.models import Message

app = create_app()

with app.app_context():
    # Create new table
    db.create_all()
    print("✓ New messages table created")
    
    # Add sample messages without replies. Admin answers them manually.
    messages = [
        Message(
            nama='Rina',
            email='rina@gmail.com',
            telepon='081234567890',
            subjek='Informasi Tabungan',
            pesan='Saya ingin menanyakan syarat membuka rekening tabungan baru. Unit Indrapura sangat membantu dalam memberikan informasi layanan perbankan.',
            status='Terbaca'
        ),
        Message(
            nama='Budi',
            email='budi@gmail.com',
            telepon='082345678901',
            subjek='Kredit Usaha untuk UMKM',
            pesan='Apakah ada pembiayaan untuk usaha kecil dan menengah? Saya tertarik dengan program kredit usaha yang ditawarkan.',
            status='Terbaca'
        ),
        Message(
            nama='Sari',
            email='sari@gmail.com',
            telepon='083456789012',
            subjek='Mobile Banking Mudah Digunakan',
            pesan='Bagaimana cara aktivasi layanan mobile banking? Website ini sangat informatif dan memudahkan saya mencari informasi.',
            status='Terbaca'
        ),
        Message(
            nama='Ahmad Wijaya',
            email='ahmad.wijaya@gmail.com',
            telepon='084567890123',
            subjek='Kepuasan Pelayanan Teller',
            pesan='Staf Unit Indrapura sangat profesional dan membantu. Pelayanan yang diberikan sangat cepat dan memuaskan.',
            status='Terbaca'
        ),
        Message(
            nama='Dewi Kusuma',
            email='dewi.kusuma@gmail.com',
            telepon='085678901234',
            subjek='Program Transfer Antar Bank',
            pesan='Terimakasih atas layanan transfer antar bank yang cepat dan terpercaya. Sangat membantu dalam kebutuhan transaksi saya.',
            status='Terbaca'
        ),
    ]
    
    db.session.add_all(messages)
    db.session.commit()
    print("✓ Sample messages without replies added")
    print("\n✓ Database migration completed successfully!")
