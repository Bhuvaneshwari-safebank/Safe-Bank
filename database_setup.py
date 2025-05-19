import sqlite3
import os

def create_user_db():
    if not os.path.exists('database'):
        os.makedirs('database')

    conn = sqlite3.connect('database/user.db')  

    # Users Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            balance INTEGER DEFAULT 1000000,
            is_blocked INTEGER DEFAULT 0,
            unblock_time INTEGER DEFAULT NULL,
            device_info TEXT,
            last_ip TEXT
        )
    ''')

    # Trusted Locations Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS trusted_locations (
            email TEXT NOT NULL,
            ip TEXT NOT NULL,
            added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Trusted Devices Table – moved to same DB
    conn.execute('''
        CREATE TABLE IF NOT EXISTS trusted_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            device_id TEXT NOT NULL,
            added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, device_id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ user.db created successfully!")


def create_transaction_db():
    conn = sqlite3.connect('database/transaction.db')

    # Transactions Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email TEXT NOT NULL,
            receiver_email TEXT NOT NULL,
            amount INTEGER NOT NULL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            fraud_score REAL DEFAULT 0.0
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ transaction.db created successfully!")


if __name__ == "__main__":
    create_user_db()
    create_transaction_db()
    print("✅ All tables created successfully!")
