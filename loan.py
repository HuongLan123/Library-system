# Import thư viện, cấu trúc dữ liệu, các giải thuật
from data_structures import BSTree, yes_no
from database import create_connection
from datetime import datetime, timedelta
from main import connect
import csv

# Kết nối cơ sở dữ liệu
connected, conn, cursor = connect()

# Hàm gọi lại các chức năng quản lý mượn-trả
def call_loan_management():
    from menu import loan_management
    loan_management()

# Hàm định dạng kiểu dữ liệu thời gian
def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if isinstance(dt, datetime) else ""

# Khai báo đối tượng LoanRecord (phiếu mượn/trả sách)
class LoanRecord:
    def __init__(self, loan_id, reader_id, isbn, borrow_date, due_date, return_date=None, status="Đang mượn"):
        self.loan_id = loan_id
        self.reader_id = reader_id
        self.isbn = isbn
        self.borrow_date = borrow_date if isinstance(borrow_date, datetime) else datetime.strptime(borrow_date, "%Y-%m-%d %H:%M:%S.%f")
        self.due_date = due_date if isinstance(due_date, datetime) else datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S.%f")
        self.return_date = return_date if isinstance(return_date, datetime) else (datetime.strptime(return_date, "%Y-%m-%d %H:%M:%S.%f") if return_date else None)
        self.status = status

    # Hàm định dạng biểu diễn đối tượng LoanRecord
    def __str__(self):
        return (f"[Loan ID: {self.loan_id}] Reader: {self.reader_id}, ISBN: {self.isbn}, "
                f"Borrowed: {self.borrow_date.date()}, Due: {self.due_date.date()}, "
                f"Returned: {self.return_date.date() if self.return_date else 'N/A'}, Status: {self.status}")

# Khai báo đổi tượng LoanManager (cậu ghi hộ t)
class LoanManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.tree = BSTree()
        self.book_cache = {}     # isbn -> available_quantity
        self.reader_cache = set()  # reader_id set
        self.load_all_data()

    # Hàm xử lý load dữ liệu từ bảng books, readers, loans từ database vào bộ nhớ RAM
    def load_all_data(self):
        self.reader_cache.clear()
        self.book_cache.clear()
        self.tree.clear()
        self.cursor.execute("SELECT * FROM readers")
        for reader_id, _ in self.cursor.fetchall(): 
            self.reader_cache.add(reader_id)
        self.cursor.execute("SELECT isbn, available_quantity FROM books")
        for isbn, qty in self.cursor.fetchall():
            self.book_cache[isbn] = qty
        self.cursor.execute("SELECT * FROM loans")
        for row in self.cursor.fetchall():
            loan = LoanRecord(*row)
            self.tree.insert(loan.loan_id, loan)

    # Hàm cập nhật loan_id tự động, mỗi lần tạo thì loan_id + 1
    def get_next_id(self):
        max_id = 0
        for loan in self.tree.inorder():
            if loan.loan_id > max_id:
                max_id = loan.loan_id
        return max_id + 1

    # Hàm tạo phiếu mượn
    def create_loan(self):
        reader_id = input("✍️ Nhập mã bạn đọc: ").strip()
        isbn = input("✍️ Nhập mã ISBN sách: ").strip()
        duedays = int(input("✍️ Nhập số ngày mượn: ").strip() or 30)
        from test_condition import can_borrow
        if not can_borrow(self,reader_id, isbn): # Kiểm tra điều kiện trước khi tạo phiếu mượn
            if not yes_no():
                call_loan_management()
            else:
                self.create_loan()
            return
        loan_id = self.get_next_id()
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=duedays)
        record = LoanRecord(loan_id, reader_id, isbn, borrow_date, due_date)
        self.tree.insert(loan_id, record)        # Thêm dữ liệu phiếu mượn vào cây
        self.book_cache[isbn] -= 1          
        self.cursor.execute("""
            INSERT INTO loans (loan_id, reader_id, isbn, borrow_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (loan_id, reader_id, isbn, borrow_date.strftime("%Y-%m-%d %H:%M:%S.%f"), due_date.strftime("%Y-%m-%d %H:%M:%S.%f"), "Đang mượn"))
        self.cursor.execute("UPDATE books SET available_quantity = available_quantity - 1, borrowed_quantity = borrowed_quantity + 1 WHERE isbn = ?", (isbn,))
        self.conn.commit()
        print("✅ Tạo phiếu mượn thành công.")
        if not yes_no():
            call_loan_management()
        else:
            self.create_loan()
        return True
    # Hàm trả sách
    def return_book(self):
        loan_id = int(input("✍️ Nhập ID phiếu mượn: ").strip())
        record = self.tree.search(loan_id)
        if not record or record.status != "Đang mượn":
            print("❌ Không tìm thấy phiếu hoặc sách đã được trả.")
        else:
            record.status = "Đã trả"
            record.return_date = datetime.now()
            self.book_cache[record.isbn] += 1
            self.cursor.execute("""
            UPDATE loans SET return_date=?, status=? WHERE loan_id=?
        """, (record.return_date.strftime("%Y-%m-%d %H:%M:%S.%f"), "Đã trả", loan_id))
            self.cursor.execute("UPDATE books SET available_quantity = available_quantity + 1 , borrowed_quantity = borrowed_quantity -1 WHERE isbn = ?", (record.isbn,))
            self.conn.commit()
            print("✅ Trả sách thành công.")
        if not yes_no():
            call_loan_management()
        else:
            self.return_book()
    # Hàm xóa phiếu mượn
    def delete_loan(self):
        loan_id = int(input("✍️ Nhập ID phiếu mượn: ").strip())
        record = self.tree.search(loan_id)
        if not record or record.status == "Đang mượn":
            print("❌ Không thể xoá phiếu chưa trả.")
        else:
            self.tree.delete(loan_id)
            self.cursor.execute("DELETE FROM loans WHERE loan_id=?", (loan_id,))
            self.conn.commit()
            print("✅ Xoá phiếu thành công.")
        if not yes_no():
            call_loan_management()
        else:
            self.delete_loan()
    # Hàm in danh sách phiếu mượn
    def view_loans(self):
        for loan in self.tree.inorder():
            print(loan)
        call_loan_management()

    # Hàm lọc dữ liệu phiếu mượn theo bạn đọc
    def filter_by_reader(self):
        reader_id = input("✍️ Nhập mã bạn đọc: ").strip()
        print(f"Lịch sử mượn của bạn đọc {reader_id}:")
        for loan in self.tree.inorder():
            if loan.reader_id == reader_id:
                print(loan)
        if not yes_no():
            call_loan_management()
        else:
            self.filter_by_reader()
    # Hàm lọc dữ liệu phiếu mượn theo sách
    def filter_by_isbn(self):
        isbn = input("✍️ Nhập mã ISBN sách: ").strip()
        print(f"Lịch sử mượn của sách ISBN {isbn}:")
        for loan in self.tree.inorder():
            if loan.isbn == isbn:
                print(loan)
        if not yes_no():
            call_loan_management()
        else:
            self.filter_by_isbn()
    # Hàm in ra danh sách sách quá hạn
    def view_overdue(self):
        print("Danh sách sách quá hạn:")
        today = datetime.now()
        for loan in self.tree.inorder():
            if loan.status == "Đang mượn" and loan.due_date < today:
                print(loan)
        call_loan_management()

# Hàm chọn chức năng quản lý mượn trả
def loan_choice():
    manager = LoanManager(conn)
    ch = input("👉 Nhập lựa chọn của bạn (1 - 9): ").strip()
    while True:
        if ch == "1":
            manager.create_loan()
        elif ch == "2":
            manager.return_book()
        elif ch == "3":
            manager.delete_loan()
        elif ch == "4":
            manager.view_loans()
        elif ch == "5":
            manager.filter_by_reader()
        elif ch == "6":
            manager.filter_by_isbn()
        elif ch == "7":
            manager.view_overdue()
        elif ch == "8":
            export_to_csv(manager)
        elif ch == "9":
            print("🏠 Trở về menu chính.")
            break
        else:
            print("❌ Lựa chọn không hợp lệ. Hãy thử lại.")
            ch = input("👉 Nhập lựa chọn của bạn (1 - 9): ").strip()
            continue
        break
    return

# Hàm xuất dữ liệu mượn trả sang file csvcsv
def export_to_csv(self):
    with open("loan_export.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Loan ID",  "Reader", "ISBN","Borrowed","Due date","Returned","Status"])
        for loan in self.tree.inorder():
            writer.writerow([loan.loan_id, loan.reader_id, loan.isbn, format_datetime(loan.borrow_date), format_datetime(loan.due_date), format_datetime(loan.return_date), loan.status])
    print("✅ Xuất CSV", "Đã lưu file loan_export.csv")
    call_loan_management()
