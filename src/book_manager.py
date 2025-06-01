import json
import os
from datetime import datetime


class BookManager:
    def __init__(self):
        self.data_file = "../data/books.json"
        self.ensure_data_file_exists()

    def ensure_data_file_exists(self):
        """Đảm bảo file dữ liệu tồn tại"""
        os.makedirs("../data", exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)

    def get_all_books(self):
        """Lấy tất cả sách từ file JSON"""
        try:
            with open(self.data_file, 'r') as f:
                books = json.load(f)
            return books
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def get_book_by_id(self, book_id):
        """Lấy sách theo ID"""
        books = self.get_all_books()
        for book in books:
            if str(book['id']) == str(book_id):
                return book
        return None

    def add_book(self, book_data):
        """Thêm sách mới"""
        books = self.get_all_books()

        # Tạo ID mới
        new_id = max([book['id'] for book in books], default=0) + 1

        book = {
            'id': new_id,
            'title': book_data['title'],
            'author': book_data['author'],
            'year': int(book_data['year']),
            'genre': book_data['genre'],
            'description': book_data.get('description', ''),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        books.append(book)
        self._save_books(books)
        return book

    def update_book(self, book_id, updated_data):
        """Cập nhật thông tin sách"""
        books = self.get_all_books()
        for i, book in enumerate(books):
            if str(book['id']) == str(book_id):
                books[i] = {
                    'id': book['id'],
                    'title': updated_data['title'],
                    'author': updated_data['author'],
                    'year': int(updated_data['year']),
                    'genre': updated_data['genre'],
                    'description': updated_data.get('description', ''),
                    'created_at': book.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                }
                self._save_books(books)
                return True
        return False

    def delete_book(self, book_id):
        """Xóa sách"""
        books = self.get_all_books()
        books = [book for book in books if str(book['id']) != str(book_id)]
        self._save_books(books)
        return True

    def _save_books(self, books):
        """Lưu danh sách sách vào file JSON"""
        with open(self.data_file, 'w') as f:
            json.dump(books, f, indent=2)