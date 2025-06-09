# Hệ thống quản lý thư viện

Đây là một hệ thống quản lý thư viện đơn giản được xây dựng bằng Python, sử dụng SQLite làm cơ sở dữ liệu và triển khai các cấu trúc dữ liệu hiệu quả để quản lý dữ liệu.

## Tổng quan chức năng của hệ thống

Hệ thống cung cấp các chức năng cơ bản và cần thiết cho việc quản lý thư viện, được chia thành các phân hệ chính:

* **Quản lý Sách:**
    * Thêm sách mới vào thư viện.
    * Xóa sách khỏi hệ thống.
    * Tìm kiếm sách theo nhiều tiêu chí.
    * Cập nhật thông tin chi tiết của sách (tiêu đề, thể loại, tác giả, số lượng, v.v.).
    * Sắp xếp danh sách sách theo các tiêu chí khác nhau (ISBN, tiêu đề, thể loại, tác giả).
    * Hiển thị danh sách tất cả các sách hiện có trong thư viện.
    * Xuất dữ liệu sách ra tệp CSV để dễ dàng báo cáo hoặc sao lưu.

* **Quản lý Bạn đọc:**
    * Thêm bạn đọc mới vào hệ thống.
    * Xóa thông tin bạn đọc.
    * Tìm kiếm bạn đọc theo mã số hoặc tên.
    * Cập nhật thông tin cá nhân của bạn đọc.
    * Sắp xếp danh sách bạn đọc theo mã số hoặc tên.
    * Hiển thị danh sách tất cả bạn đọc.
    * Xuất dữ liệu bạn đọc ra tệp CSV.

* **Quản lý Mượn/Trả Sách:**
    * Tạo phiếu mượn sách, ghi nhận thông tin bạn đọc và sách được mượn.
    * Ghi nhận việc trả sách, cập nhật tình trạng sách và phiếu mượn.
    * Xóa phiếu mượn (ví dụ: trong trường hợp nhập sai hoặc hủy bỏ).
    * Xem danh sách tất cả các phiếu mượn hiện có.
    * Lọc phiếu mượn theo bạn đọc hoặc theo mã ISBN của sách.
    * Hiển thị danh sách các phiếu mượn đã quá hạn.
    * Xuất dữ liệu mượn/trả ra tệp CSV để theo dõi và báo cáo.

## Cấu trúc dự án

Dự án được tổ chức thành các tệp Python riêng biệt, mỗi tệp chịu trách nhiệm cho một phần cụ thể của hệ thống:
```plaintext
project/
├── main.py             # Điểm khởi chạy chính của chương trình, chứa vòng lặp menu chính.
├── menu.py             # Định nghĩa cấu trúc các menu và các lựa chọn chức năng.
├── database.py         # Xử lý kết nối, tạo bảng và tương tác với cơ sở dữ liệu SQLite.
├── data_structures.py  # Chứa cài đặt các cấu trúc dữ liệu (HashTable, AVL Tree) và thuật toán (Merge Sort).
├── book.py             # Định nghĩa lớp Book và các hàm quản lý sách.
├── reader.py           # Định nghĩa lớp Reader và các hàm quản lý bạn đọc.
├── loan.py             # Định nghĩa lớp LoanRecord và các hàm quản lý mượn/trả sách
├── test_condition.py   # Chứa các hàm kiểm tra điều kiện và tính hợp lệ của dữ liệu đầu vào.
├── bookinput_export.csv   # File dữ liệu mẫu để thêm sách từ file
├── readerinput_export.csv # File dữ liệu mẫu để thêm người đọc từ file
├── README.md              # File hướng dẫn (chính là file này)
└──library11.db         # Cơ sở dữ liệu mặc định của hệ thống
```

</details>

---
## Yêu cầu cài đặt

Để chạy hệ thống này, bạn cần có:

* **Python 3.x** (khuyến nghị phiên bản 3.6 trở lên)

Hệ thống sử dụng các thư viện chuẩn của Python như `sqlite3`, `datetime`, `csv`, `textwrap` và `locale`, do đó bạn không cần cài đặt thêm thư viện bên ngoài nào.

## Hướng dẫn sử dụng

Thực hiện các bước sau để chạy và sử dụng hệ thống quản lý thư viện:

1.  **Sao chép mã nguồn (Clone Repository):**
    Nếu bạn đang sử dụng Git, hãy sao chép kho lưu trữ này về máy tính của mình:
    ```bash
    git clone [https://github.com/yourusername/library-system.git](https://github.com/yourusername/library-system.git)
    cd library-system
    ```
    (Thay `https://github.com/yourusername/library-system.git` bằng URL thực tế của repository nếu có.)

2.  **Chạy chương trình:**
    Mở terminal hoặc command prompt, điều hướng đến thư mục dự án và chạy tệp `main.py`:
    ```bash
    python main.py
    ```

Sau khi chương trình khởi chạy, bạn sẽ thấy một menu chính hiển thị các lựa chọn chức năng. Bạn có thể nhập số tương ứng với chức năng muốn thực hiện và làm theo hướng dẫn trên màn hình.

---

