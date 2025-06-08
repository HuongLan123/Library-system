# Import các hàm kết nối và nạp lại dữ liệu từ cơ sở dữ liệu
from database import create_connection, reload_database_book, reload_database_loan, reload_database_reader
def connect():
      # Tạo kết nối đến cơ sở dữ liệu SQLite
    conn, cursor = create_connection("library11.db")
    # Kiểm tra kết nối thành công hay không
    if not conn:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return False, None, None
    else:
        from database import create_table_database
        create_table_database(conn, cursor)
        return True, conn, cursor
def main():
    connected, conn, cursor = connect()
    if connected: 
        # Import các hàm giao diện menu và các chức năng quản lý từ các module tương ứng
        from menu import menu, book_management, reader_management, loan_management

        # Vòng lặp chính của chương trình để xử lý các lựa chọn chức năng
        while True: 
            menu()  # Hiển thị menu chức năng
            ch = input("Nhập lựa chọn của bạn: ")
            if ch == "1":
                print("Quản lý sách")
                reload_database_book(conn, cursor)       # Nạp dữ liệu sách từ cơ sở dữ liệu vào bộ nhớ
                book_management()            # Gọi giao diện quản lý sách

            elif ch == "2":
                print("Quản lý bạn đọc")
                reload_database_reader(conn, cursor)     # Nạp dữ liệu bạn đọc từ cơ sở dữ liệu vào bộ nhớ
                reader_management()          # Gọi giao diện quản lý bạn đọc

            elif ch == "3":
                # Import lớp và trình quản lý mượn sách
                from loan import LoanRecord, LoanManager
                print("Quản lý mượn trả sách")
                reload_database_loan(LoanManager, conn, cursor)  # Nạp dữ liệu mượn trả vào bộ nhớ với LoanManager
                loan_management()                 # Gọi giao diện quản lý mượn trả sách

            elif ch == "4":
                print("Thoát chương trình")
                break # Thoát khỏi vòng lặp và kết thúc chương trình
            else:
                # Xử lý lựa chọn không hợp lệ
                print("Lựa chọn không hợp lệ, vui lòng thử lại.")
    # Đóng kết nối cơ sở dữ liệu khi kết thúc chương trình
    conn.close()
    return

# Gọi hàm main nếu file được chạy trực tiếp
if __name__ == "__main__":
    main()
