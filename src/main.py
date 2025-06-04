import tkinter as tk
from tkinter import messagebox
from book_manager import BookManager
from auth_manager import AuthManager
import requests
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as ttk
from PIL import ImageTk, Image


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Thư Viện")

        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.width = int(self.screen_width * 0.8)
        self.height = int(self.screen_height * 0.7)
        x = int(self.screen_width/2 - self.width/2)
        y = int(self.screen_height/2 - self.height/2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.root.minsize(600,600)
        self.init_image()

        self.auth_manager = AuthManager()
        self.book_manager = BookManager()
        self.current_user = None

        self.root.bind('<Escape>', lambda event: self.root.quit())

        self.setup_login_screen()

    def init_image(self):
        img = Image.open('images/lol_logo.png')
        self.lol_logo = ImageTk.PhotoImage(img)

        img = Image.open('images/riot_logo144.png')
        self.riot_logo144 = ImageTk.PhotoImage(img)

        logo = Image.open('images/vng.png')
        new = logo.resize((170, 20), Image.LANCZOS)
        self.vng_logo = ImageTk.PhotoImage(new)

        register = Image.open('images/register_button.png')
        new_size = register.resize((90, 90))
        self.register_button = ImageTk.PhotoImage(new_size)

        img = Image.open('images/riot.jpg')
        new = img.resize((self.width + 300, self.height + 300), Image.LANCZOS)
        self.riot = ImageTk.PhotoImage(new)

        img = Image.open('images/search.png')
        new_size = img.resize((230, 50))
        self.search_photo = ImageTk.PhotoImage(new_size)

        img_f = Image.open('images/flash.jpg')
        new_f = img_f.resize((65, 65))
        self.flash = ImageTk.PhotoImage(new_f)

        img_ig = Image.open('images/ignite.jpg')
        new_ig = img_ig.resize((65, 65))
        self.ignite = ImageTk.PhotoImage(new_ig)

        img = Image.open('images/save.png')
        self.save = ImageTk.PhotoImage(img)

        img = Image.open('images/chon.png')
        new_chon = img.resize((200, 50))
        self.photo_chon = ImageTk.PhotoImage(new_chon)

        img1 = Image.open('images/huy.png')
        new_huy = img1.resize((200, 50))
        self.photo_huy = ImageTk.PhotoImage(new_huy)

        img = Image.open('images/register_background.jpg')
        new_img = img.resize((self.screen_width, self.screen_height))
        self.register_bg = ImageTk.PhotoImage(new_img)

        img = Image.open('images/lol_logo_gold.png')
        self.riot_logo_gold = ImageTk.PhotoImage(img)

    def setup_login_screen(self):
        self.clear_window()
        self.root.iconphoto(0, self.riot_logo144)
        self.style = ttk.Style(theme='cosmo')

        frame = ttk.Frame(self.root)
        frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        tk.Label(frame, image=self.vng_logo).place(relx=0.5, rely=0.1, anchor='center')

        ttk.Label(frame, text="Sign in", font=("Arial", 20)).place(relx=0.5, rely=0.2, anchor='center')

        def on_entry_click_user(event):
            if user_string.get() == 'TÊN NGƯỜI DÙNG':
                user_string.set('')
            ttk.Label(frame, text='TÊN NGƯỜI DÙNG',
                     font='Calibri 7 bold',
                     foreground='#666666').place(relx=0.225, rely=0.305)

        def on_entry_click_pass(event):
            if pass_string.get() == 'MẬT KHẨU':
                pass_string.set('')
            self.password_entry['show'] = '•'
            ttk.Label(frame, text='MẬT KHẨU',
                     font='Calibri 7 bold',
                     foreground='#666666').place(relx=0.225, rely=0.405)

        user_string = tk.StringVar(value='TÊN NGƯỜI DÙNG')
        self.username_entry = ttk.Entry(frame, textvariable=user_string, font='Calibri 12 bold')
        self.username_entry.place(relx=0.22, rely=0.3, relwidth=0.6, relheight=0.08)

        pass_string = tk.StringVar(value='MẬT KHẨU')
        self.password_entry = ttk.Entry(frame, textvariable=pass_string, font='Calibri 12 bold')
        self.password_entry.place(relx=0.22, rely=0.4, relwidth=0.6, relheight=0.08)

        self.username_entry.bind('<FocusIn>', on_entry_click_user)
        self.username_entry.bind('<KeyPress-Return>', lambda event: self.password_entry.focus_set())

        self.password_entry.bind('<FocusIn>', on_entry_click_pass)
        self.password_entry.bind('<KeyPress-Return>', lambda event: self.login())

        style=ttk.Style()
        style.configure('Login.TButton',
                        borderwidth=0,
                        padding=0)
        ttk.Button(frame,text='Đăng nhập',
                  image=self.register_button,
                  style='Login.TButton',
                  command=self.login).place(relx=0.5, rely=0.8, anchor='center')

        style = ttk.Style()
        style.configure('Register.TButton',
                        foreground='#545757',
                        background='white',
                        font=('Calibri', 10, 'bold'),
                        borderwidth=0)
        style.map('Register.TButton',
                  foreground=[('active', 'black')],
                  background=[('active', 'white')],
                  font=[('active', ('Calibri', 11, 'bold'))])
        ttk.Button(frame, text="KHÔNG THỂ ĐĂNG NHẬP\n        TẠO TÀI KHOẢN",
                  style='Register.TButton',
                  command=self.show_register_dialog).place(relx=0.5, rely=0.95, anchor='s', width=220)

        ttk.Label(self.root, image=self.riot).place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        ttk.Sizegrip(self.root).place(relx=1, rely=1, anchor='se')

        #Backdoor
        def backdoor_function(event=None):
            sucess, user = self.auth_manager.login('admin', 'admin123')
            self.current_user = user
            self.setup_main_interface()
        self.root.bind('<Control-KeyPress-a>', backdoor_function)

    def show_register_dialog(self):
        dialog = tk.Toplevel(self.root)
        w = self.screen_width
        h = self.screen_height
        dialog.title("Đăng Ký Tài Khoản")
        dialog.attributes('-topmost', False)
        dialog.iconphoto(0, self.riot_logo144)
        dialog.geometry(f"{w}x{h}+"
                        f"{int(self.screen_width/2 - w/2)}+{int(self.screen_height/2 - h/2)}")
        dialog.minsize(1500,1000)

        ttk.Label(dialog, image=self.register_bg).pack(expand=True, fill='both')

        def on_entry_click_user(event):
            if user_string.get() == "TÊN NGƯỜI DÙNG":
                user_string.set('')

            entry_user_label.place(relx=0.105, rely=0.405)
            if len(user_string.get()) >= 1:
                user_button['state'] = 'enabled'
            else:
                user_button['state'] = 'disabled'

        self.new_pass = False
        def on_entry_click_pass(event):
            if pass_string.get() == 'MẬT KHẨU':
                pass_string.set('')
            new_password['show'] = '•'

            pass_entry_label.place(relx=0.105, rely=0.335)

            new_password.configure(bootstyle='danger')

            password = pass_string.get()
            len8 = False
            if len(password) >= 8:
                re2.configure(text='✔ Mật khẩu phải dài ít nhất 8 kí tự.',
                              foreground='green')
                len8 = True
            else:
                re2.configure(text='✘ Mật khẩu phải dài ít nhất 8 kí tự.',
                              foreground='#666666')
                len8 = False

            has_letter = any(c.isalpha() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_symbol = any(not c.isalnum() for c in password)

            count = sum([has_letter, has_digit, has_symbol])
            #print(count)
            if count >= 2 and len8:
                self.new_pass = True
                re3.configure(text='✔ Mật khẩu phải chứa hai trong số các ký tự sau:'
                                   '\n chữ cái, số hoặc ký hiệu.',
                              foreground='green')
                #pass_button['state'] = 'enabled'
                if count == 2:
                    new_password.configure(bootstyle='warning')
                    re1.configure(text='✔ Cần phải đạt mức Trung bình trở lên.',
                                  foreground='orange')
                else:
                    new_password.configure(bootstyle='success')
                    re1.configure(text='✔ Cần phải đạt mức Trung bình trở lên.',
                                  foreground='green')
            else:
                re3.configure(text='✘ Mật khẩu phải chứa hai trong số các ký tự sau:'
                                   '\n chữ cái, số hoặc ký hiệu.',
                              foreground='#666666')
                re1.configure(text='✘ Cần phải đạt mức Trung bình trở lên.',
                              foreground='#666666')
                self.new_pass = False

        def on_entry_click_con(event):
            if con_string.get() == 'XÁC NHẬN MẬT KHẨU':
                con_string.set('')
            confirm_password['show'] = '•'
            con_entry_label.place(relx=0.105, rely=0.635)

        def enable_pass_button(event):
            if self.new_pass and pass_string.get() == con_string.get():
                pass_button['state'] = 'enabled'
                #confirm_warning.configure(text='', background='#f2b6e8')
                confirm_password.configure(bootstyle='success')
                self.confirm_warning.destroy()
                con_entry_label.configure(foreground='#666666', background='white')
            else:
                style = ttk.Style()
                style.configure('Purple.TEntry',
                                fieldbackground='#f2b6e8',
                                bordercolor='#8c02c7',
                                highlightcolor='#8c02c7')
                confirm_password.configure(style='Purple.TEntry')
                con_entry_label.configure(foreground='#f227cd',
                                          background='#f2b6e8')
                self.confirm_warning.place(relx=0.1, rely=0.73)

        def register():
            success, message = self.auth_manager.register_user(
                user_string.get(),
                pass_string.get(),
                "user"
            )

            if success:
                dialog.destroy()
                Messagebox.show_info("Thành công", message)
            else:
                Messagebox.show_error("Lỗi", message)

        def onclick_user_button():
            user_label.destroy()
            new_username.destroy()
            user_button.destroy()
            entry_user_label.destroy()

            ttk.Label(frame, text='Chọn mật khẩu', font='Calibri 20 bold').place(relx=0.5, rely=0.2, anchor='center')
            ttk.Label(frame,
                     text='Hãy đảm bảo mật khẩu đủ mạnh',
                     foreground='#666666',
                     font='Calibri 17 bold').place(relx=0.5, rely=0.26, anchor='center')
            new_password.place(relx=0.1, rely=0.33, relwidth=0.8, relheight=0.1)
            pass_required.place(relx=0.5, rely=0.52, anchor='center', relwidth=0.6, relheight=0.15)
            confirm_password.place(relx=0.1, rely=0.63, relwidth=0.8, relheight=0.1)
            pass_button.place(relx=0.5, rely=0.9,anchor='s')

        frame = ttk.Frame(dialog)
        frame.place(relx=0.8, rely=0.5, relwidth=0.3, relheight=0.6, anchor='center')

        user_string = tk.StringVar(value='TÊN NGƯỜI DÙNG')
        new_username = ttk.Entry(frame, textvariable=user_string, font='Calibri 12 bold')
        entry_user_label = ttk.Label(frame, text='TÊN NGƯỜI DÙNG',
                                    font='Calibri 7 bold',
                                    foreground='#666666')
        user_label = ttk.Label(frame, text='Chọn tên người dùng', font='Calibri 20 bold')
        style = ttk.Style()
        style.configure('Register.TButton',
                        borderwidth=0,
                        padding=0)
        user_button = ttk.Button(frame,
                                 image=self.register_button,
                                 style='Register.TButton',
                                 command=onclick_user_button)

        user_label.place(relx=0.5, rely=0.2, anchor='center')
        new_username.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.1)
        user_button.place(relx=0.5, rely=0.9, anchor='s')
        user_button['state'] = 'disabled'

        pass_string = tk.StringVar(value='MẬT KHẨU')
        new_password = ttk.Entry(frame, textvariable=pass_string, font='Calibri 12 bold')
        pass_entry_label = ttk.Label(frame, text='MẬT KHẨU',
                              font='Calibri 7 bold',
                              foreground='#666666')

        pass_required = ttk.Frame(frame)
        re1 = ttk.Label(pass_required,
                       foreground='#666666',
                       text='✘ Cần phải đạt mức Trung bình trở lên.')
        re1.pack(expand=True, fill='both')
        re2 = ttk.Label(pass_required,
                       foreground='#666666',
                       text='✘ Mật khẩu phải dài ít nhất 8 kí tự.')
        re2.pack(expand=True, fill='both')
        re3 = ttk.Label(pass_required,
                       foreground='#666666',
                       text='✘ Mật khẩu phải chứa hai trong số các ký tự sau:\n chữ cái, số hoặc ký hiệu.')
        re3.pack(expand=True, fill='both')

        con_string = tk.StringVar(value='XÁC NHẬN MẬT KHẨU')
        confirm_password = ttk.Entry(frame, textvariable=con_string, font='Calibri 12 bold')
        con_entry_label = ttk.Label(frame, text='XÁC NHẬN MẬT KHẨU',
                              font='Calibri 7 bold',
                              foreground='#666666')
        self.confirm_warning = ttk.Label(frame, text='! Mật khẩu không trùng khớp',
                                         foreground='#f227cd',
                                         font='Calibri 10')

        pass_button = ttk.Button(frame, image=self.register_button,style='Register.TButton', text="Đăng Ký", command=register)
        pass_button['state'] = 'disabled'

        new_username.bind('<FocusIn>', on_entry_click_user)
        new_username.bind('<KeyRelease>', on_entry_click_user)

        new_password.bind('<FocusIn>', on_entry_click_pass)
        new_password.bind('<KeyRelease>', on_entry_click_pass)
        new_password.bind('<KeyRelease>', enable_pass_button, add='+')

        confirm_password.bind('<FocusIn>', on_entry_click_con)
        confirm_password.bind('<KeyRelease>', enable_pass_button)

    def login(self, username=None, password=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, user = self.auth_manager.login(username, password)

        if success:
            self.current_user = user
            self.setup_main_interface()
        else:
            Messagebox.show_error("Username không tồn tại hoặc password sai!", "Đăng nhập thất bại!")

    def setup_main_interface(self):
        self.clear_window()
        self.root.iconphoto(0, self.lol_logo)

        menubar = ttk.Menu(self.root)

        book_menu = ttk.Menu(menubar, tearoff=0)
        book_menu.add_command(label="Xem danh sách sách", command=self.show_books)
        if self.current_user['role'] == 'admin':
            book_menu.add_separator()
            book_menu.add_command(label="Thêm sách mới", command=self.show_add_book_dialog)
            book_menu.add_separator()
            book_menu.add_command(label="Nhập sách từ API", command=self.fetch_books_from_api)
        menubar.add_cascade(label="Sách", menu=book_menu)

        if self.current_user['role'] == 'admin':
            user_menu = ttk.Menu(menubar, tearoff=0)
            user_menu.add_command(label="Quản lý người dùng", command=self.manage_users)
            menubar.add_cascade(label="Người dùng", menu=user_menu)

        account_menu = ttk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Đổi mật khẩu", command=self.change_password)
        account_menu.add_separator()
        account_menu.add_command(label="Đăng xuất", command=self.logout)
        menubar.add_cascade(label="Tài khoản", menu=account_menu)

        def configure_theme(theme):
            self.style = ttk.Style(theme=theme)

        theme_menu = ttk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label='solar', command = lambda: configure_theme('solar'))
        theme_menu.add_separator()
        theme_menu.add_command(label='superhero', command=lambda: configure_theme('superhero'))
        theme_menu.add_separator()
        theme_menu.add_command(label='vapor', command=lambda: configure_theme('vapor'))
        theme_menu.add_separator()
        theme_menu.add_command(label='darkly', command=lambda: configure_theme('darkly'))
        theme_menu.add_separator()
        theme_menu.add_command(label='journal', command=lambda: configure_theme('journal'))
        theme_menu.add_separator()
        theme_menu.add_command(label='simplex', command=lambda: configure_theme('simplex'))
        menubar.add_cascade(label='Đổi màu nền', menu=theme_menu)

        self.root.config(menu=menubar)

        self.show_books()

        ttk.Sizegrip(self.root).place(relx=1, rely=1, anchor='se')

    def show_books(self, books=None):
        self.clear_main_area()

        if books is None:
            books = self.book_manager.get_all_books()

        ###
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('ID', 'Title', 'Author', 'Year', 'Genre', 'Description'),
            selectmode='browse',
        )

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Title', width=200, anchor=tk.W)
        self.tree.column('Author', width=150, anchor=tk.W)
        self.tree.column('Year', width=70, anchor=tk.CENTER)
        self.tree.column('Genre', width=120, anchor=tk.W)
        self.tree.column('Description', width=300, anchor=tk.W)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Tiêu đề')
        self.tree.heading('Author', text='Tác giả')
        self.tree.heading('Year', text='Năm XB')
        self.tree.heading('Genre', text='Thể loại')
        self.tree.heading('Description', text='Mô tả')

        self.tree.place(relx=0, rely=0, relwidth=1, relheight=0.5)
        for book in books:
            self.tree.insert(
                '',
                tk.END,
                values=(
                    book['id'],
                    book['title'],
                    book['author'],
                    book['year'],
                    book['genre'],
                    book.get('description', '')[:50] + '...' if 'description' in book else ''
                )
            )
        self.tree.bind('<Double-1>', self.show_book_details)

        search_frame = ttk.Frame(self.root)
        search_frame.place(relx=0, rely=0.7)
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Tìm kiếm", image=self.search_photo, relief='raised',
                  command=self.search_books).pack(side=tk.LEFT, padx=5)

        if self.current_user['role'] == 'admin':
            button_frame = ttk.Frame(self.root)
            button_frame.place(relx=0.1, rely=0.8)

            self.sua = tk.Button(button_frame, text="Sửa",compound='top', image=self.flash, command=self.edit_selected_book)
            self.sua.pack(side='left',padx=20)
            self.root.bind('<d>', self.edit_selected_book)

            self.xoa = tk.Button(button_frame, text="Xóa",compound='top', image=self.ignite, command=self.delete_selected_book)
            self.xoa.pack(side='left',padx=20)
            self.root.bind('<f>', self.delete_selected_book)
        ttk.Sizegrip(self.root).place(relx=1, rely=1, anchor='se')

    def search_books(self, event=None):
        progress_dialog = ttk.Toplevel(self.root)
        w = 300
        h = 50
        progress_dialog.geometry(f'{w}x{h}+'
                                 f'{int((self.screen_width - w) / 2)}+'
                                 f'{int((self.screen_height - h) / 2)}')
        progress_dialog.overrideredirect(True)
        progress_int = tk.IntVar()
        progress = ttk.Progressbar(progress_dialog,
                                   maximum=20,
                                   orient='horizontal',
                                   mode='determinate',
                                   length=100,
                                   variable=progress_int)
        progress.pack(expand=True, fill='both')

        def update_progress(step=0):
            progress['value'] = step
            if step < 20:
                progress_dialog.after(2, update_progress, step + 1)
            else:
                keyword = self.search_entry.get().lower()
                if not keyword:
                    self.show_books()
                    return

                all_books = self.book_manager.get_all_books()
                filtered_books = [
                    book for book in all_books
                    if (keyword in book['title'].lower() or
                        keyword in book['author'].lower() or
                        keyword in book['genre'].lower() or
                        keyword in str(book['year']))
                    ]

                self.show_books(filtered_books)
                progress_dialog.destroy()
        update_progress()

    def show_book_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        book_id = item['values'][0]

        book = self.book_manager.get_book_by_id(book_id)
        if not book:
            return

        details_window = ttk.Toplevel(self.root)
        details_window.iconphoto(0, self.riot_logo_gold)
        details_window.title(f"Chi tiết sách: {book['title']}")
        w = 500
        h = 400
        details_window.geometry(f"{w}x{h}+"
                                f"{int((self.screen_width - w)/2)}+{int((self.screen_height - h)/2)}")

        ttk.Label(details_window, text=book['title'], font=("Arial", 14, "bold")).pack(pady=10)

        info_frame = ttk.Frame(details_window)
        info_frame.pack(fill=tk.BOTH, padx=20, pady=5, expand=True)

        ttk.Label(info_frame, text=f"Tác giả: {book['author']}", anchor='w').pack(fill=tk.X)
        ttk.Label(info_frame, text=f"Năm xuất bản: {book['year']}", anchor='w').pack(fill=tk.X)
        ttk.Label(info_frame, text=f"Thể loại: {book['genre']}", anchor='w').pack(fill=tk.X)

        ttk.Label(info_frame, text="Mô tả:", anchor='w').pack(fill=tk.X, pady=(10, 0))
        description_text = ttk.Text(info_frame, height=10, wrap=tk.WORD)
        description_text.pack(fill=tk.BOTH, expand=True)
        description_text.insert(tk.END, book.get('description', 'Không có mô tả'))
        description_text.config(state=tk.DISABLED)

        if self.current_user['role'] == 'admin':
            button_frame = ttk.Frame(details_window)
            button_frame.pack(fill=tk.X, padx=10, pady=10)

            ttk.Button(button_frame, text="Sửa", command=lambda: self.edit_book(book)).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Xóa", command=lambda: self.delete_book(book, details_window)).pack(
                side=tk.LEFT, padx=5)

    def show_add_book_dialog(self):
        dialog = ttk.Toplevel(self.root)
        dialog.iconphoto(0, self.riot_logo_gold)
        dialog.title("Thêm Sách Mới")
        w = 400
        h = 550
        dialog.geometry(f"{w}x{h}+"
                        f"{int((self.screen_width - w)/2)}+"
                        f"{int((self.screen_height - h)/2)}")

        ttk.Label(dialog, text="Tiêu đề:").pack(pady=(10, 0))
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.pack(pady=5)

        ttk.Label(dialog, text="Tác giả:").pack()
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.pack(pady=5)

        ttk.Label(dialog, text="Năm xuất bản:").pack()
        year_entry = ttk.Entry(dialog, width=40)
        year_entry.pack(pady=5)

        ttk.Label(dialog, text="Thể loại:").pack()
        genre_entry = ttk.Entry(dialog, width=40)
        genre_entry.pack(pady=5)

        ttk.Label(dialog, text="Mô tả:").pack()
        description_text = ttk.Text(dialog, height=5, width=40)
        description_text.pack(pady=5)

        def save_book():
            book_data = {
                'title': title_entry.get(),
                'author': author_entry.get(),
                'year': year_entry.get(),
                'genre': genre_entry.get(),
                'description': description_text.get("1.0", tk.END).strip()
            }

            if not book_data['title'] or not book_data['author']:
                Messagebox.show_error("Lỗi", "Tiêu đề và tác giả không được để trống!")
                return

            try:
                int(book_data['year'])
            except ValueError:
                Messagebox.show_error("Lỗi", "Năm xuất bản phải là số!")
                return

            self.book_manager.add_book(book_data)
            Messagebox.show_info("Thành công", "Thêm sách thành công!")
            dialog.destroy()
            self.show_books()

        tk.Button(dialog, text="Lưu",image=self.save, command=save_book).place(relx=0.5, rely=1, anchor='s')

    def edit_selected_book(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            Messagebox.show_warning("Cảnh báo", "Vui lòng chọn sách cần sửa!")
            return

        item = self.tree.item(selected_item)
        book_id = item['values'][0]

        book = self.book_manager.get_book_by_id(book_id)
        if book:
            self.edit_book(book)

    def edit_book(self, book):
        dialog = ttk.Toplevel(self.root)
        dialog.title(f"Sửa sách: {book['title']}")
        dialog.iconphoto(0, self.riot_logo_gold)
        w = 600
        h = 600
        dialog.geometry(f"{w}x{h}+"
                        f"{int((self.screen_width - w)/2)}+"
                        f"{int((self.screen_height - h)/2)}")

        ttk.Label(dialog, text="Tiêu đề:").pack(pady=(10, 0))
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, book['title'])
        title_entry.pack(pady=5)

        ttk.Label(dialog, text="Tác giả:").pack()
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.insert(0, book['author'])
        author_entry.pack(pady=5)

        ttk.Label(dialog, text="Năm xuất bản:").pack()
        year_entry = ttk.Entry(dialog, width=40)
        year_entry.insert(0, book['year'])
        year_entry.pack(pady=5)

        ttk.Label(dialog, text="Thể loại:").pack()
        genre_entry = ttk.Entry(dialog, width=40)
        genre_entry.insert(0, book['genre'])
        genre_entry.pack(pady=5)

        ttk.Label(dialog, text="Mô tả:").pack()
        description_text = ttk.Text(dialog, height=5, width=40)
        description_text.insert(tk.END, book.get('description', ''))
        description_text.pack(pady=5)

        def update_book():
            updated_data = {
                'title': title_entry.get(),
                'author': author_entry.get(),
                'year': year_entry.get(),
                'genre': genre_entry.get(),
                'description': description_text.get("1.0", tk.END).strip()
            }

            if not updated_data['title'] or not updated_data['author']:
                Messagebox.show_error("Lỗi", "Tiêu đề và tác giả không được để trống!")
                return

            try:
                int(updated_data['year'])
            except ValueError:
                Messagebox.show_error("Lỗi", "Năm xuất bản phải là số!")
                return

            self.book_manager.update_book(book['id'], updated_data)
            Messagebox.show_info("Thành công", "Cập nhật sách thành công!")
            dialog.destroy()
            self.show_books()

        tk.Button(dialog, text="Cập nhật",image=self.save, command=update_book).place(relx=0.5, rely=1, anchor='s')

    def delete_selected_book(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            Messagebox.show_warning("Cảnh báo", "Vui lòng chọn sách cần xóa!")
            return

        item = self.tree.item(selected_item)
        book_id = item['values'][0]
        book_title = item['values'][1]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sách '{book_title}'?"):
            self.book_manager.delete_book(book_id)
            Messagebox.show_info("Thành công", "Xóa sách thành công!")
            self.show_books()

    def delete_book(self, book, parent_window=None):
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sách '{book['title']}'?"):
            self.book_manager.delete_book(book['id'])
            Messagebox.show_info("Thành công", "Xóa sách thành công!")
            if parent_window:
                parent_window.destroy()
            self.show_books()

    def fetch_books_from_api(self):
        try:
            # Sử dụng Open Library API
            response = requests.get("https://openlibrary.org/subjects/programming.json?limit=10")
            data = response.json()

            books = []
            for work in data.get('works', []):
                book_data = {
                    'title': work.get('title', 'Không có tiêu đề'),
                    'author': ''.join(work.get('authors', [{}])[0].get('name', 'Không rõ')),
                    'year': work.get('first_publish_year', 'N/A'),
                    'genre': ''.join(work.get('subject', ['Không có thể loại'])[:3]),
                    'description': work.get('description', {}).get('value', 'Không có mô tả')[:200] if isinstance(
                        work.get('description'), dict) else 'Không có mô tả'
                }
                books.append(book_data)

            confirm_dialog = ttk.Toplevel(self.root)
            confirm_dialog.iconphoto(0, self.riot_logo_gold)
            confirm_dialog.title("Nhập sách từ API")
            w = 600
            h = 600
            confirm_dialog.geometry(f"{w}x{h}+"
                                    f"{int((self.width - w)/2)}+"
                                    f"{int((self.height - h)/2)}")

            ttk.Label(confirm_dialog, text="Danh sách sách từ API", font=("Arial", 12, "bold")).pack(pady=10)

            tree_frame = ttk.Frame(confirm_dialog)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            scrollbar = ttk.Scrollbar(tree_frame,orient='horizontal')
            scrollbar.pack(side=tk.BOTTOM, fill='x')

            tree = ttk.Treeview(
                tree_frame,
                columns=('Title', 'Author', 'Year', 'Genre'),
                xscrollcommand=scrollbar.set
            )

            tree.column('#0', width=0, stretch=tk.NO)
            tree.column('Title', width=200, anchor=tk.W)
            tree.column('Author', width=150, anchor=tk.W)
            tree.column('Year', width=70, anchor=tk.CENTER)
            tree.column('Genre', width=120, anchor=tk.W)

            tree.heading('Title', text='Tiêu đề')
            tree.heading('Author', text='Tác giả')
            tree.heading('Year', text='Năm XB')
            tree.heading('Genre', text='Thể loại')

            tree.pack(fill='both', expand=True)
            scrollbar.config(command=tree.yview)

            for book in books:
                tree.insert('', tk.END, values=(
                    book['title'],
                    book['author'],
                    book['year'],
                    book['genre']
                ))

            def import_selected():
                selected_items = tree.selection()
                if not selected_items:
                    Messagebox.show_warning("Cảnh báo", "Vui lòng chọn ít nhất một sách để nhập!")
                    return

                for item in selected_items:
                    values = tree.item(item)['values']
                    book_data = {
                        'title': values[0],
                        'author': values[1],
                        'year': values[2],
                        'genre': values[3],
                        'description': "Nhập từ Open Library API"
                    }
                    self.book_manager.add_book(book_data)

                Messagebox.show_info("Thành công", f"Đã nhập {len(selected_items)} sách thành công!")
                confirm_dialog.destroy()
                self.show_books()

            button_frame = ttk.Frame(confirm_dialog)
            button_frame.pack(fill=tk.X, padx=10, pady=10)

            tk.Button(button_frame, text="Nhập sách đã chọn",image=self.photo_chon, command=import_selected).pack(side=tk.LEFT)
            tk.Button(button_frame, text="Hủy",image=self.photo_huy, command=confirm_dialog.destroy).pack(side=tk.RIGHT)

        except Exception as e:
            Messagebox.show_error("Lỗi", f"Không thể lấy dữ liệu từ API: {str(e)}")

    def manage_users(self):
        self.clear_main_area()

        users = self.auth_manager.get_all_users()

        tree_frame = ttk.Frame(self.root)
        tree_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.user_tree = ttk.Treeview(
            tree_frame,
            columns=('Username', 'Role', 'Created'),
            yscrollcommand=scrollbar.set,
            selectmode='browse'
        )

        self.user_tree.column('#0', width=0, stretch=tk.NO)
        self.user_tree.column('Username', width=150, anchor=tk.W)
        self.user_tree.column('Role', width=100, anchor=tk.CENTER)
        self.user_tree.column('Created', width=150, anchor=tk.CENTER)

        self.user_tree.heading('Username', text='Tên đăng nhập')
        self.user_tree.heading('Role', text='Vai trò')
        self.user_tree.heading('Created', text='Ngày tạo')

        self.user_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.user_tree.yview)

        for user in users:
            if user['username'] == self.current_user['username']:
                continue

            self.user_tree.insert(
                '',
                tk.END,
                values=(
                    user['username'],
                    user['role'],
                    user.get('created_at', 'N/A')
                )
            )

        button_frame = ttk.Frame(self.root)
        button_frame.place(relx=0, rely=0.8, relwidth=1)

        ttk.Button(button_frame, text="Thêm người dùng", command=self.show_add_user_dialog).pack(side='left', padx=10, ipadx=20, ipady=20)
        ttk.Button(button_frame, text="Sửa vai trò", command=self.edit_user_role).pack(side='left', padx=10, ipadx=20, ipady=20)
        ttk.Button(button_frame, text="Xóa người dùng", command=self.delete_user).pack(side='left', padx=10, ipadx=20, ipady=20)
        ttk.Button(button_frame, text="Quay lại", command=self.show_books).pack(side='right', padx=50, ipadx=20, ipady=20)
        ttk.Sizegrip(self.root).place(relx=1, rely=1, anchor='se')

    def show_add_user_dialog(self):

        dialog = tk.Toplevel(self.root)
        dialog.iconphoto(0, self.riot_logo_gold)
        dialog.title("Thêm Người Dùng Mới")
        w = 400
        h = 400
        dialog.geometry(f"{w}x{h}+"
                        f"{int((self.screen_width - w)/2)}+"
                        f"{int((self.screen_height - h)/2)}")

        ttk.Label(dialog, text="Tên đăng nhập:").pack(pady=5)
        username_entry = ttk.Entry(dialog)
        username_entry.pack(pady=5)

        ttk.Label(dialog, text="Mật khẩu:").pack(pady=5)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.pack(pady=5)

        ttk.Label(dialog, text="Vai trò:").pack(pady=5)
        role_var = tk.StringVar(value="user")
        ttk.Radiobutton(dialog, text="Người dùng", variable=role_var, value="user").pack(side='left', padx=5)
        ttk.Radiobutton(dialog, text="Quản trị", variable=role_var, value="admin").pack(side='left')

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()

            if not username or not password:
                Messagebox.show_error("Lỗi", "Tên đăng nhập và mật khẩu không được để trống!")
                return

            success, message = self.auth_manager.register_user(username, password, role)

            if success:
                Messagebox.show_info("Thành công", message)
                dialog.destroy()
                self.manage_users()
            else:
                Messagebox.show_error("Lỗi", message)

        tk.Button(dialog, text="Lưu",image=self.save, command=save_user).place(relx=0.5, rely=1, anchor='s')

    def edit_user_role(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            Messagebox.show_warning("Cảnh báo", "Vui lòng chọn người dùng cần sửa!")
            return

        item = self.user_tree.item(selected_item)
        username = item['values'][0]
        current_role = item['values'][1]

        if username == self.current_user['username']:
            Messagebox.show_warning("Cảnh báo", "Không thể sửa vai trò của chính mình!")
            return

        dialog = ttk.Toplevel(self.root)
        dialog.iconphoto(0, self.riot_logo_gold)
        dialog.title(f"Sửa vai trò: {username}")
        w = 300
        h = 300
        dialog.geometry(f"{w}x{h}+"
                        f"{int((self.screen_width - w)/2)}+"
                        f"{int((self.screen_height - h)/2)}")

        ttk.Label(dialog, text=f"Tên đăng nhập: {username}").pack(pady=5)
        ttk.Label(dialog, text="Vai trò mới:").pack()

        role_var = tk.StringVar(value=current_role)
        ttk.Radiobutton(dialog, text="Người dùng", variable=role_var, value="user").pack()
        ttk.Radiobutton(dialog, text="Quản trị", variable=role_var, value="admin").pack()

        def update_role():
            new_role = role_var.get()
            if new_role == current_role:
                dialog.destroy()
                return

            self.auth_manager.update_user_role(username, new_role)
            Messagebox.show_info("Thành công", "Cập nhật vai trò thành công!")
            dialog.destroy()
            self.manage_users()

        tk.Button(dialog, text="Cập nhật",image=self.save, command=update_role).place(relx=0.5, rely=1, anchor='s')

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            Messagebox.show_warning("Cảnh báo", "Vui lòng chọn người dùng cần xóa!")
            return

        item = self.user_tree.item(selected_item)
        username = item['values'][0]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa người dùng '{username}'?"):
            self.auth_manager.delete_user(username)
            Messagebox.show_info("Thành công", "Xóa người dùng thành công!")
            self.manage_users()

    def change_password(self):
        dialog = ttk.Toplevel(self.root)
        dialog.iconphoto(0, self.riot_logo_gold)
        dialog.title("Đổi Mật Khẩu")
        w = 400
        h = 400
        dialog.geometry(f"{w}x{h}+"
                        f"{int((self.screen_width - w)/2)}+"
                        f"{int((self.screen_height - h)/2)}")

        ttk.Label(dialog, text="Mật khẩu hiện tại:").pack(pady=5)
        current_password_entry = ttk.Entry(dialog, show="*")
        current_password_entry.pack(pady=5)

        ttk.Label(dialog, text="Mật khẩu mới:").pack(pady=5)
        new_password_entry = ttk.Entry(dialog, show="•")
        new_password_entry.pack(pady=5)

        ttk.Label(dialog, text="Xác nhận mật khẩu mới:").pack(pady=5)
        confirm_password_entry = ttk.Entry(dialog, show='•')
        confirm_password_entry.pack(pady=5)

        def update_password():
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not current_password or not new_password or not confirm_password:
                Messagebox.show_error("Lỗi", "Vui lòng điền đầy đủ thông tin!")
                return

            if new_password != confirm_password:
                Messagebox.show_error("Lỗi", "Mật khẩu mới không khớp!")
                return

            success, message = self.auth_manager.change_password(
                self.current_user['username'],
                current_password,
                new_password
            )

            if success:
                Messagebox.show_info("Thành công", message)
                dialog.destroy()
            else:
                Messagebox.show_error("Lỗi", message)

        tk.Button(dialog, text="Đổi mật khẩu",image=self.save, command=update_password).place(relx=0.5, rely=1, anchor='s')

    def logout(self):
        self.current_user = None
        self.setup_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_main_area(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()


if __name__ == "__main__":
    root = ttk.Window()
    app = LibraryApp(root)
    root.mainloop()