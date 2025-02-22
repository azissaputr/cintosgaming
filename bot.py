import requests
import random
import json
import time

# Hàm đọc danh sách ví từ file
def read_wallets(file_path):
    wallets = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) == 2:
                wallets.append(parts[0])  # Lấy địa chỉ ETH
    return wallets

# Hàm tạo referral code ngẫu nhiên
def generate_referral_code():
    return f"0x{random.randint(10**7, 10**8-1):x}"

# Hàm lấy điểm từ referral code
def get_points_from_referral_code(referral_code):
    url = f"https://boustneqsaombfmtfffq.supabase.co/rest/v1/waitlist?referral_code=eq.{referral_code}&select=points"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # Token của bạn
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # API key của bạn
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0].get('points', 0)  # Lấy điểm từ dữ liệu trả về
    return 100  # Trả về 100 nếu không tìm thấy hoặc có lỗi

# Hàm đăng ký người dùng mới
def register_user(full_name, email, eth_address, referral_code_tai_khoan_moi, referral_code_nguoi_gioi_thieu):
    points = get_points_from_referral_code(referral_code_nguoi_gioi_thieu)  # Lấy điểm từ referral code của người giới thiệu
    url = "https://boustneqsaombfmtfffq.supabase.co/rest/v1/waitlist"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # Token của bạn
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdXN0bmVxc2FvbWJmbXRmZmZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3MzA0NTQsImV4cCI6MjA1NTMwNjQ1NH0.FeSHmHVeSQvQ2hVz0PHYBhFTijOY2U_U_zl4LIxFG_w",  # API key của bạn
    }
    
    data = {
        "full_name": full_name,
        "email": email,
        "eth_address": eth_address,
        "referral_code": referral_code_tai_khoan_moi,  # Referral code của tài khoản mới
        "points": points  # Điểm từ referral code của người giới thiệu
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.text

# Hàm lưu tài khoản vào file
def save_account(file_path, email, eth_address, referral_code):
    with open(file_path, 'a') as f:
        f.write(f"{email}:{eth_address}:{referral_code}\n")

# Hàm chính để thực hiện quy trình
def main():
    wallets = read_wallets("wallet.txt")  # Đọc ví từ file
    if not wallets:
        print("Không tìm thấy ví!")
        return
    
    # Nhập referral code của người giới thiệu khi chạy script
    referral_code_nguoi_gioi_thieu = input("Nhập referral code của người giới thiệu: ").strip()
    
    while wallets:
        eth_address = wallets.pop(0)
        full_name = f"User{len(wallets)}"
        email = f"user{len(wallets)}@jobcyvn.site"
        
        # Tạo referral code ngẫu nhiên cho tài khoản mới
        referral_code_tai_khoan_moi = generate_referral_code()
        
        # Đăng ký người dùng
        status, response = register_user(full_name, email, eth_address, referral_code_tai_khoan_moi, referral_code_nguoi_gioi_thieu)
        if status == 201:
            print(f"Đã đăng ký: {email} - {eth_address} với ref: {referral_code_tai_khoan_moi}")
            save_account("data.txt", email, eth_address, referral_code_tai_khoan_moi)  # Lưu tài khoản vào file
        else:
            print(f"Thất bại: {response}")
        
        time.sleep(2)  # Tránh spam API quá nhanh

# Chạy hàm chính
if __name__ == "__main__":
    main()
