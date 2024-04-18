# Định nghĩa hàm tính tổng
def tinh_tong(a, b):
    return a + b

# Nhập vào hai số từ người dùng
so_a = float(input("Nhập số thứ nhất: "))
so_b = float(input("Nhập số thứ hai: "))

# Tính tổng và in kết quả
tong = tinh_tong(so_a, so_b)
print("Tổng của hai số là:", tong)

