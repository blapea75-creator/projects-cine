import sqlite3

DATABASE = "cinemax.db"

def create_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE,
            movie TEXT NOT NULL,
            ticket_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            seats TEXT,
            total REAL NOT NULL,
            payment REAL NOT NULL,
            change_amount REAL NOT NULL,
            username TEXT,
            transaction_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_transaction(
    movie,
    ticket_type,
    quantity,
    seats,
    total,
    payment,
    change_amount,
    username
):
    connection = sqlite3.connect(DATABASE)

    try:
        cursor = connection.cursor()

        # Insert the transaction to generate an automatic database ID
        cursor.execute("""
            INSERT INTO transactions (
                transaction_id,
                movie,
                ticket_type,
                quantity,
                seats,
                total,
                payment,
                change_amount,
                username
            )
            VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            movie,
            ticket_type,
            quantity,
            ", ".join(seats),
            total,
            payment,
            change_amount,
            username
        ))

        # Use the database's automatically incremented ID
        database_id = cursor.lastrowid
        transaction_id = f"TXN-{database_id:04d}"

        cursor.execute("""
            UPDATE transactions
            SET transaction_id = ?
            WHERE id = ?
        """, (transaction_id, database_id))

        connection.commit()
        return transaction_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def get_transaction_count():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    connection.close()
    return count

def get_all_transactions():
    import sqlite3
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT transaction_id, transaction_date, username, movie,
               ticket_type, quantity, seats, total, payment, change_amount
        FROM transactions
        ORDER BY id DESC
    """)

    transactions = cursor.fetchall()
    connection.close()

    return transactions

# Create the database and table if they do not exist
create_database()
