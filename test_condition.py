# import thư viện, cấu trúc dữ liệu 
from data_structures import BSTree
from loan import LoanRecord
from datetime import datetime

# Hàm kiểm tra tính logic trong dữ liệu sách
def test_book(isbn, title, genre, author, added_quantity, quantity, available_quantity, borrowed_quantity):
    """
    Kiểm tra dữ liệu hợp lệ của một quyển sách trước khi thêm vào hệ thống.
    
    Trả về: (True, "") nếu hợp lệ
            (False, lý do lỗi) nếu không hợp lệ
    """
    # Kiểm tra trường rỗng
    if not isbn.strip():
        return False, "ISBN không được để trống."
    if not title.strip():
        return False, "Tiêu đề sách không được để trống."
    if not genre.strip():
        return False, "Thể loại sách không được để trống."
    if not author.strip():
        return False, "Tác giả sách không được để trống."

    # Kiểm tra kiểu dữ liệu và giá trị số hợp lệ
    try:
        added_quantity = int(added_quantity)
        quantity = int(quantity)
        available_quantity = int(available_quantity)
        borrowed_quantity = int(borrowed_quantity)
    except ValueError:
        return False, "Các trường số lượng phải là số nguyên."

    # Kiểm tra giá trị âm
    if any(q < 0 for q in [added_quantity, quantity, available_quantity, borrowed_quantity]):
        return False, "Số lượng không được là số âm."

    # Kiểm tra mâu thuẫn logic
    if available_quantity > quantity:
        return False, "Số lượng có sẵn không thể lớn hơn tổng số lượng sách."
    if borrowed_quantity > quantity:
        return False, "Số lượng đã mượn không thể lớn hơn tổng số lượng sách."
    if available_quantity + borrowed_quantity != quantity:
        return False, "Tổng số lượng phải bằng đã mượn + có sẵn."

    return True, ""

# Hàm kiểm tra tính logic trong dữ liệu người đọc
def test_reader(reader_table, reader_id, name):
    # Kiểm tra về trống dữ liệu trong reader_id và name
    if not reader_id or not name:
        print("❌ Mã số sinh viên và tên không được để trống.")
        return
    # Kiểm tra sự tồn tại của bạn đọc trong bảng
    if reader_table.search(reader_id):
        print("❌ Bạn đọc đã tồn tại.")
        return
    
# Hàm kiểm tra điều kiện để tạo phiếu mượn
def can_borrow(self, reader_id, isbn):
    # Kiểm tra sự tồn tại của bạn đọc
    if reader_id not in self.reader_cache:
        print(f"❌ Bạn đọc '{reader_id}' không tồn tại.")
        return False
    # Kiểm tra sự tồn tại của sách
    if isbn not in self.book_cache:
        print(f"❌ Sách với ISBN '{isbn}' không tồn tại.")
        return False
    # Kiểm tra số lượng còn của sách
    if self.book_cache[isbn] <= 0:
        print("❌ Sách đã hết, không thể mượn.")
        return False
    # Kiểm tra về tình trạng mượn sách của bạn đọc
    for loan in self.tree.inorder():
        if loan.reader_id == reader_id and loan.isbn == isbn and loan.status == "Đang mượn":
            print("❌ Bạn đọc đang mượn sách này và chưa trả.")
            return False
    return True
