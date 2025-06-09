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
