# Import thư viện, cấu trúc dữ liệu, chức năng in bảng dữ liệu
from main import connect
from data_structures import HashTable, merge_sort, print_wrapped_table, yes_no
from test_condition import test_reader
import csv

# Kết nối đến cơ sở dữ liệu
connected, conn, cursor = connect()

# Hàm gọi lại danh sách lựa chọn chức năng quản lý người đọc: reader_management()
def call_reader_management():
    from menu import reader_management
    reader_management()

# Định nghĩa lớp Reader
class Reader:
    # Hàm khởi tạo reader
    def __init__(self, reader_id, name):
        self.reader_id = reader_id
        self.name = name

    # Hàm biểu diễn đối tượng Reader
    def __str__(self):
        return f"{self.reader_id} | {self.name}"

    # Hàm kiểm tra sự tồn tại của reader_id; đảm bảo reader_id là duy nhất
    def __eq__(self, other):
        return isinstance(other, Reader) and self.reader_id == other.reader_id

    # Hàm trả về giá trị băm của thuộc tính
    def __hash__(self):
        return hash(self.reader_id)

# Hàm khởi tạo reader_table theo cấu trúc HashTable
reader_table = HashTable()

# Khai báo tiêu đề của dữ liệu bảng Reader
headers = ["Reader_IDID", "Tên bạn đọc"]
col_widths = [15, 30]

# Hàm chọn lựa các chức năng trong quản lý người đọc
def reader_choice():
    ch = input("👉 Nhập lựa chọn của bạn (1-8): ")
    while True:
        if ch not in map(str, range(1, 9)):
            print("❌ Lựa chọn không hợp lệ.")
            ch = input("👉 Nhập lựa chọn của bạn (1-8): ")
            continue
        if ch == "1":
            add_reader()
        elif ch == "2":
            delete_reader()
        elif ch == "3":
            search_reader()
        elif ch == "4":
            update_reader()
        elif ch == "5":
            sort_readers()
        elif ch == "6":
            display_readers()
        elif ch == "7":
            export_to_csv()
            call_reader_management()
        elif ch == "8":
            print("🏠 Trở về menu chính.")
            from main import main
            main()
            break

# Hàm thêm người đọc từ file csv
def add_reader_file():
    filename = input("Nhập tên file (VD: readerreader.csv): ").strip()
    try:
        with open(filename, newline='', encoding='utf-8-sig') as csvfile:
            readerss = csv.DictReader(csvfile)
            for row in readerss:
                reader_id = row["Mã người đọc"]
                name = row["Họ và tên"]
                test_reader = test_reader(reader_table, reader_id, name)
                if test_reader:
                    reader = Reader(reader_id, name)
                    if not reader_table.search(reader_id):
                        reader_table.insert(reader_id, reader)
                        cursor.execute("""
        INSERT INTO readers (reader_id, namename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (reader_id, name))
                        print(f"✅ Thêm bạn đọc '{reader_id}' thành công.")
                        conn.commit()
                    else:
                        print(f"❌ Bạn đọc có mã bạn đọc '{reader_id}' đã tồn tại.")
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file '{filename}'")
        return 
    except Exception as e:
        print(f"❌ Lỗi khi thêm sách từ file: {e}")
        return

# Hàm thêm người đọc từ màn hình
def add_reader_terminal():
    reader_id = input("Nhập MSSV làm reader_id: ").strip()
    name = input("Nhập tên bạn đọc: ").strip()
    if test_reader(reader_table, reader_id, name):
        reader = Reader(reader_id, name)
        reader_table.insert(reader_id, reader)
        cursor.execute("INSERT INTO readers (reader_id, name) VALUES (?, ?)", (reader_id, name))
        conn.commit()
        print("✅ Thêm bạn đọc thành công.")

# Hàm gọi để thêm người đọc
def add_reader():
    print("Chọn phương thức thêm người đọc:")
    print("1. Thêm người đọc từ file")
    print("2. Thêm người đọc từ bàn phím")
    print("3. Trở về menu chính")
    while True:
        choice = input("👉 Nhập lựa chọn của bạn (1 - 3): ")
        if choice == "1":
            add_reader_file()
        elif choice == "2":
            add_reader_terminal()        
        elif choice == "3":
            call_reader_management()
            break
        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng thử lại.")

# Hàm xóa người đọc
def delete_reader():
    reader_id = input("Nhập mã bạn đọc cần xóa: ").strip()
    if reader_table.search(reader_id):
        reader_table.delete(reader_id)
        cursor.execute("DELETE FROM readers WHERE reader_id = ?", (reader_id,))
        conn.commit()
        print("✅ Xóa bạn đọc thành công.")
    else:
        print("❌ Không tìm thấy bạn đọc.")
    if not yes_no():
        call_reader_management()

# Hàm tìm kiếm người đọc theo mã bạn đọcđọc / Tên
def search_reader():
    keyword = input("Nhập từ khóa tìm kiếm theo mã bạn đọc hoặc tên: ").strip().lower()
    result = []
    for reader in reader_table.get_all_values():
        if keyword in reader.reader_id.lower() or keyword in reader.name.lower():
            result.append([reader.reader_id, reader.name])
    if result:
        print_wrapped_table(headers, result, col_widths)
    else:
        print("❌ Không tìm thấy bạn đọc nào.")
    if not yes_no():
        call_reader_management()

# Hàm chỉnh sửa thông tin người đọc
def update_reader():
    reader_id = input("Nhập mã bạn đọc cần cập nhật: ").strip()
    reader = reader_table.search(reader_id)
    if not reader:
        print("❌ Không tìm thấy bạn đọc.")
        return
    print(f"Thông tin hiện tại: Reader_ID = {reader.reader_id}, Tên = {reader.name}")
    new_name = input("Nhập tên mới (Enter để giữ nguyên): ").strip()
    if new_name:
        reader.name = new_name
        cursor.execute("UPDATE readers SET name = ? WHERE reader_id = ?", (new_name, reader_id))
        conn.commit()
        print("✅ Cập nhật thành công.")
    else:
        print("✅ Không có thay đổi.")
    reader_table.insert(reader.reader_id, reader)
    if not yes_no():
        call_reader_management()

# Hàm sắp xếp người đọc theo Mã bạn đọc/Tên
def sort_readers():
    readers = reader_table.get_all_values()
    print("Sắp xếp theo phương thức nào: ")
    print("1. Sắp xếp theo mã bạn đọc")
    print("2. Sắp xếp theo họ tên")
    while True:
        get_choice = input("👉 Nhập lựa chọn của bạn (1 - 2):")
        if get_choice.strip() == "1":
            key_func = lambda r: r.reader_id
            break
        elif get_choice.strip() == "2":
            key_func = lambda r: r.name
            break
        else:
            print("❌ Lựa chọn không hợp lệ. Hãy nhập lại.")
            continue
    reverse = input("Sắp xếp giảm dần? (True/False): ").strip().lower() == "true"
    sorted_readers = merge_sort(readers, key_func, reverse=reverse)
    data = [[r.reader_id, r.name] for r in sorted_readers]
    print_wrapped_table(headers, data, col_widths)
    if not yes_no():
        call_reader_management()

# Hàm biểu diễn bảng danh sách người đọc
def display_readers():
    all_readers = reader_table.get_all_values()
    data = [[r.reader_id, r.name] for r in all_readers]
    print_wrapped_table(headers, data, col_widths) 
    call_reader_management()

# Hàm xuất dữ liệu người đọc sang file csv
def export_to_csv():
    with open("readers_export.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Mã người đọc","Họ và tên"])
        for reader in reader_table.get_all_values():
            writer.writerow([reader.reader_id, reader.name])
    print("Xuất CSV", "Đã lưu file reader_export.csv")
