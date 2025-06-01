import json
import os
from datetime import datetime
import hashlib


class AuthManager:
    def __init__(self):
        self.users_file = "../data/users.json"
        self.ensure_users_file_exists()

    def ensure_users_file_exists(self):
        """Đảm bảo file người dùng tồn tại"""
        os.makedirs("../data", exist_ok=True)
        if not os.path.exists(self.users_file):
            # Tạo admin mặc định nếu file không tồn tại
            default_users = [
                {
                    'username': 'admin',
                    'password': self._hash_password('admin123'),
                    'role': 'admin',
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)

    def _hash_password(self, password):
        """Băm mật khẩu sử dụng SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def get_all_users(self):
        """Lấy tất cả người dùng"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            return users
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def get_user(self, username):
        """Lấy thông tin người dùng"""
        users = self.get_all_users()
        for user in users:
            if user['username'] == username:
                return user
        return None

    def login(self, username, password):
        """Xác thực đăng nhập"""
        user = self.get_user(username)
        if user and user['password'] == self._hash_password(password):
            return True, user
        return False, None

    def register_user(self, username, password, role='user'):
        """Đăng ký người dùng mới"""
        if self.get_user(username):
            return False, "Tên đăng nhập đã tồn tại!"

        users = self.get_all_users()
        users.append({
            'username': username,
            'password': self._hash_password(password),
            'role': role,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._save_users(users)
        return True, "Đăng ký thành công!"

    def update_user_role(self, username, new_role):
        """Cập nhật vai trò người dùng"""
        users = self.get_all_users()
        for i, user in enumerate(users):
            if user['username'] == username:
                users[i]['role'] = new_role
                self._save_users(users)
                return True
        return False

    def delete_user(self, username):
        """Xóa người dùng"""
        users = self.get_all_users()
        users = [user for user in users if user['username'] != username]
        self._save_users(users)
        return True

    def change_password(self, username, current_password, new_password):
        """Đổi mật khẩu"""
        user = self.get_user(username)
        if not user or user['password'] != self._hash_password(current_password):
            return False, "Mật khẩu hiện tại không đúng!"

        users = self.get_all_users()
        for i, user in enumerate(users):
            if user['username'] == username:
                users[i]['password'] = self._hash_password(new_password)
                self._save_users(users)
                return True, "Đổi mật khẩu thành công!"

        return False, "Có lỗi xảy ra!"

    def _save_users(self, users):
        """Lưu danh sách người dùng vào file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)