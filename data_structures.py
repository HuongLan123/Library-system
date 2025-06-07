# Định nghĩa các cấu trúc dữ liệu và function cần dùng trong hệ thống:
# Bao gồm: Bảng băm (HashTable), Cây cân bằng AVL, thuật toán Merge Sort và hàm in bảng dữ liệu
import textwrap

# Hàm hiển thị bảng dữ liệu với nội dung được tự động xuống dòng theo chiều rộng cột
def print_wrapped_table(headers, rows, col_widths, padding_char='-'):
    def wrap_row(row):
        # Bọc từng ô dữ liệu để đảm bảo vừa chiều rộng cột
        wrapped_cells = [
            textwrap.wrap(str(cell), width=col_widths[i]) for i, cell in enumerate(row)
        ]
        max_lines = max(len(cell) for cell in wrapped_cells)
        lines = []
        for i in range(max_lines):
            line = []
            for j, cell_lines in enumerate(wrapped_cells):
                content = cell_lines[i] if i < len(cell_lines) else ''
                line.append(f"{content:<{col_widths[j]}}")
            lines.append(" | ".join(line))
        return lines

    # In tiêu đề bảng
    header_line = " | ".join([f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)])
    print(header_line)
    print(padding_char * len(header_line))

    # In từng dòng dữ liệu với định dạng
    for row in rows:
        wrapped_lines = wrap_row(row)
        for line in wrapped_lines:
            print(line)
        print(padding_char * len(header_line))  # Dòng ngăn cách giữa các bản ghi

def yes_no():
    answer= input("Bạn có muốn tiếp tục (có/không)")
    if answer.strip().lower() == "có":
        return True
    else: 
        return False

# ================= HASH TABLE ====================

# Lớp đại diện cho một nút trong danh sách liên kết dùng cho bảng băm
class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None  # Trỏ đến phần tử kế tiếp trong danh sách

# Danh sách liên kết dùng để xử lý va chạm trong bảng băm (chaining)
class LinkedListForHash:
    def __init__(self):
        self.head = None # Tham chiếu đến HashNode đầu tiên
    # Thêm/Cập nhật cặp (key, value)
    def insert(self, key, value): 
        # Nếu key đã tồn tại, cập nhật lại giá trị
        node = self.head
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next
        # Thêm node mới vào đầu danh sách
        new_node = HashNode(key, value)
        new_node.next = self.head
        self.head = new_node
    # Tìm kiếm value dựa trên key
    def search(self, key): 
        node = self.head
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None
    # Xóa HashNode theo key
    def delete(self, key): 
        prev = None
        node = self.head
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.head = node.next
                return
            prev = node
            node = node.next
    # Lấy tất cả các cặp (key, value) trong chuỗi
    def get_all_key_value_pairs(self): 
        result = []
        node = self.head
        while node:
            result.append((node.key, node.value))
            node = node.next
        return result

# Lớp HashTable sử dụng danh sách liên kết để xử lý va chạm
class HashTable:
    # Khởi tạo một list Python cố định với capacity phần tử, mỗi phần tử là một đối tượng LinkedLishForHash rỗng.
    # Lưu capacity và size
    def __init__(self, capacity= 100):
        self.capacity = capacity
        self.size = 0
        self.table = [LinkedListForHash() for _ in range(capacity)]

    # Hàm chuyển đổi key thành chỉ số hash_value_index
    def _hash_function(self, key):
        key = str(key)
        hash_value_index = 0
        for char in key:
            hash_value_index = (hash_value_index * 31 + ord(char)) % self.capacity
        return hash_value_index

    # Hàm thêm cặp (key, value) 
    def insert(self, key, value):
        index = self._hash_function(key)           
        if self.table[index].search(key) is None:   # Kiểm tra nếu không có sự tồn tại của cặp (key, value) theo key
            self.size += 1                          # Cập nhật size
        self.table[index].insert(key, value)   

    # Hàm tìm value dựa trên key
    def search(self, key):
        index = self._hash_function(key)
        return self.table[index].search(key)

    # Hàm xóa key 
    def delete(self, key):
        index = self._hash_function(key)
        if self.table[index].search(key) is not None:
            self.size -= 1
        self.table[index].delete(key)

    # Hàm trả về list Python chứa tất cả value
    def get_all_values(self):
        result = []
        for bucket in self.table:
            result.extend([value for _, value in bucket.get_all_key_value_pairs()])
        return result

# ================= AVL TREE ====================

# Node của cây AVL
class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Chiều cao mặc định của node mới là 1

# Cây nhị phân tìm kiếm cân bằng AVL
class BSTree:
    # Hàm khởi tạo gốc cây
    def __init__(self):
        self.root = None
    
    # Hàm xóa toàn bộ cây
    def clear(self):
        self.root = None
    
    # Hàm lấy chiều cao của cây
    def _get_height(self, node):
        return node.height if node else 0
    
    # Hàm tính hệ số cân bằng
    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0
    
    # Hàm xoay trái
    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    # Hàm xoay phải
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x

    # Hàm thêm node 
    def insert(self, key, value):
        self.root = self._insert_recursive(self.root, key, value)

    # Hàm xử lý thêm phần tử vào cây
    def _insert_recursive(self, node, key, value):
        if node is None:
            return TreeNode(key, value)
        # So sánh key và node key, thực hiện chèn
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            node.value = value
            return node

        # Cập nhật chiều cao và cân bằng cây
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Cân bằng cây nếu mất cân bằng
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    # Hàm tìm kiếm phần tử theo key
    def search(self, key):
        return self._search_recursive(self.root, key)

    # Hàm xử lý tìm kiếm phần tử theo keykey
    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node.value if node else None
        return self._search_recursive(node.left, key) if key < node.key else self._search_recursive(node.right, key)

    # Hàm xóa phần tử theo key
    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    # Hàm xử lý xóa phần tử theo key
    def _delete_recursive(self, node, key):
        if not node:
            return node
        # So sánh key và node key, xử lý xóa dữ liệu
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key, node.value = temp.key, temp.value
            node.right = self._delete_recursive(node.right, temp.key)

        # Cập nhật chiều cao và cân bằng cây sau khi xoá
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Cân bằng lại cây nếu cần
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    # Hàm tìm node có key nhỏ nhất trong cây
    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    # Hàm duyệt cây theo thứ tự giữa
    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    # Hàm xử lý duyệt cây theo thứ tự giữa
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

# ================= MERGE SORT ====================

# Hàm sắp xếp danh sách theo thuộc tính chỉ định bằng Merge Sort
def merge_sort(arr, key_func, reverse=False):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_func)
    right = merge_sort(arr[mid:], key_func)
    return merge(left, right, key_func, reverse)

# Gộp hai danh sách đã sắp xếp
def merge(left, right, key_func, reverse):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Nếu key_func(left[i]) <= key_func(right[j]); sắp xếp tăng dần : result thêm left[i]
        # Nếu key_func(left[i]) > key_func(right[j]); sắp xếp giảm dần: result thêm left[i]
        if (key_func(left[i]) <= key_func(right[j]) and not reverse) or \
           (key_func(left[i]) > key_func(right[j]) and reverse):
            result.append(left[i])
            i += 1
        # Nếu key_func(left[i]) > key_func(right[j]); sắp xếp tăng dần: result thêm right[j]
        # Nếu key_func(left[i]) <= key_func(right[j]); sắp xếp giảm dần: result thêm right[j]
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:]) # Nối tất cả phần tử còn lại từ left[i] đến hết (left[i:]) vào danh sách result.
    result.extend(right[j:]) #Nối tất cả phần tử còn lại từ right[j] đến hết (right[j:]) vào danh sách result.
    return result