import sqlite3



def create_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        available INTEGER DEFAULT 1
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS readers (
        reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        book_id INTEGER
    )
    ''')

    conn.commit()
    conn.close()


create_database()



def add_book(title, author, year):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO books (title, author, year) VALUES (?, ?, ?)
    ''', (title, author, year))
    conn.commit()
    conn.close()


def add_reader(name, phone):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO readers (name, phone) VALUES (?, ?)
    ''', (name, phone))
    conn.commit()
    conn.close()


def give_book(reader_id, book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE books SET available = 0 WHERE book_id = ?
    ''', (book_id,))
    cursor.execute('''
    UPDATE readers SET book_id = ? WHERE reader_id = ?
    ''', (book_id, reader_id))
    conn.commit()
    conn.close()


def return_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE books SET available = 1 WHERE book_id = ?
    ''', (book_id,))
    cursor.execute('''
    UPDATE readers SET book_id = NULL WHERE book_id = ?
    ''', (book_id,))
    conn.commit()
    conn.close()


def get_available_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM books WHERE available = 1
    ''')
    available_books = cursor.fetchall()
    conn.close()
    return available_books


def get_reader_books(reader_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT b.* FROM books b
    JOIN readers r ON b.book_id = r.book_id
    WHERE r.reader_id = ?
    ''', (reader_id,))
    reader_books = cursor.fetchall()
    conn.close()
    return reader_books


def search_books(keyword):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM books WHERE title LIKE ? OR author LIKE ?
    ''', ('%' + keyword + '%', '%' + keyword + '%'))
    found_books = cursor.fetchall()
    conn.close()
    return found_books



add_book('Война и мир', 'Лев Толстой', 1869)
add_book('1984', 'Джордж Оруэлл', 1949)
add_book('Гарри Поттер и философский камень', 'Джоан Роулинг', 1997)

add_reader('Иван Иванов', '123456789')
add_reader('Петр Петров', '987654321')


give_book(1, 1)


print("Доступные книги:", get_available_books())


return_book(1)


print("Доступные книги после возврата:", get_available_books())