# HỆ THỐNG HỖ TRỢ TƯ VẤN ĐIỆN THOẠI

## 1. Giới thiệu

Đề tài xây dựng **Hệ thống hỗ trợ tư vấn điện thoại (Decision Support System - DSS)** bằng Python.

Hệ thống hỗ trợ người dùng tìm kiếm và lựa chọn điện thoại phù hợp dựa trên ngân sách, hãng sản xuất, thông số kỹ thuật và nhu cầu sử dụng.

Dữ liệu điện thoại được xử lý và phân tích để hỗ trợ quá trình ra quyết định. Hệ thống đồng thời ứng dụng **Machine Learning** nhằm nâng cao khả năng phân tích và tư vấn sản phẩm.

---

## 2. Chức năng chính

Hệ thống cung cấp các chức năng:

- Tìm kiếm điện thoại.
- Lọc điện thoại theo ngân sách.
- Lọc theo hãng sản xuất.
- Lựa chọn các tiêu chí và nhu cầu sử dụng.
- Xếp hạng và đề xuất điện thoại phù hợp.
- Xem thông tin chi tiết của từng điện thoại.
- So sánh các mẫu điện thoại.
- Phân tích và trực quan hóa dữ liệu.
- Ứng dụng Machine Learning hỗ trợ tư vấn.

---

## 3. Công nghệ sử dụng

- **Python** - ngôn ngữ lập trình chính.
- **Streamlit** - xây dựng giao diện web.
- **Pandas** - đọc, xử lý và phân tích dữ liệu.
- **NumPy** - hỗ trợ tính toán.
- **Scikit-learn** - xây dựng mô hình Machine Learning.
- **Matplotlib** - trực quan hóa dữ liệu.
- **Joblib** - lưu và tải mô hình Machine Learning.

---

## 4. Cấu trúc project

smartphone_dss_moi/
│
├── .streamlit/
├── data/
├── models/
│
├── app_kaggle.py
├── huan_luyen_kaggle.py
├── xu_ly_du_lieu.py
├── requirements.txt
└── README.md

Trong đó:

- `app_kaggle.py`: chương trình chính và giao diện của hệ thống.
- `xu_ly_du_lieu.py`: xử lý và làm sạch dữ liệu.
- `huan_luyen_kaggle.py`: huấn luyện mô hình Machine Learning.
- `data/`: chứa dữ liệu điện thoại.
- `models/`: chứa mô hình Machine Learning.
- `.streamlit/`: chứa cấu hình giao diện Streamlit.
- `requirements.txt`: danh sách thư viện cần thiết.

---

## 5. Yêu cầu trước khi chạy

Máy tính cần cài đặt:

- Python 3
- Visual Studio Code

Kiểm tra Python bằng lệnh:

```powershell
python --version
```

Nếu xuất hiện phiên bản Python, ví dụ:

Python 3.12.x

thì có thể tiếp tục.

---

## 6. Mở project

Mở **Visual Studio Code**.

Chọn:

File
→ Open Folder

Chọn thư mục:
smartphone_dss_moi

Sau đó mở Terminal:

Terminal
→ New Terminal

Kiểm tra đang đứng đúng thư mục bằng:

```powershell
dir
```

Trong danh sách cần nhìn thấy:

app_kaggle.py
huan_luyen.py
xu_ly_du_lieu.py
requirements.txt
data
models

---

## 7. Tạo môi trường ảo

Trong lần chạy đầu tiên, tạo môi trường ảo bằng:

```powershell
python -m venv .venv
```

Sau đó kích hoạt:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu thành công, Terminal sẽ xuất hiện:

```text
(.venv)
```

ở đầu dòng.

Nếu PowerShell báo:

running scripts is disabled on this system

chạy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Sau đó kích hoạt lại:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 8. Cài đặt thư viện

Sau khi kích hoạt `.venv`, chạy:

```powershell
python -m pip install -r requirements.txt
```

Chờ quá trình cài đặt hoàn tất.

Có thể kiểm tra Streamlit bằng:

```powershell
python -m streamlit --version
```

---

## 9. Chạy chương trình

Chạy hệ thống bằng lệnh:

```powershell
python -m streamlit run app_kaggle.py
```

Nếu chạy thành công, Terminal sẽ hiển thị:

```text
Local URL: http://localhost:8501
```

Trình duyệt sẽ mở giao diện của hệ thống hỗ trợ tư vấn điện thoại.

---

## 10. Dữ liệu

Dữ liệu được lưu trong thư mục:

```text
data/
```

Dữ liệu bao gồm các thông tin về điện thoại như:

- Tên điện thoại
- Hãng sản xuất
- Giá
- RAM
- Bộ nhớ
- Chip xử lý
- Camera
- Pin
- Màn hình
- Các thông số kỹ thuật khác

Dữ liệu được đọc, làm sạch và xử lý trước khi sử dụng trong hệ thống.

---

## 11. Machine Learning

Hệ thống ứng dụng Machine Learning để hỗ trợ quá trình phân tích và tư vấn điện thoại.

Quy trình xử lý:

```text
Dữ liệu điện thoại
        ↓
Đọc dữ liệu
        ↓
Tiền xử lý dữ liệu
        ↓
Lựa chọn đặc trưng
        ↓
Huấn luyện mô hình
        ↓
Lưu mô hình
        ↓
Sử dụng trong hệ thống tư vấn
```

File:

```text
huan_luyen.py
```

được sử dụng trong quá trình huấn luyện mô hình.

Mô hình sau khi huấn luyện được lưu tại:

```text
models/
```

---

## 12. Những lần chạy sau

Sau khi đã tạo `.venv` và cài thư viện ở lần đầu tiên, không cần thực hiện lại.

Mở Terminal và kích hoạt môi trường:

```powershell
.\.venv\Scripts\Activate.ps1
```

Sau đó chạy:

```powershell
python -m streamlit run app_kaggle.py
```

---

## 13. Một số lỗi thường gặp

### Không tìm thấy app_kaggle.py

Nếu xuất hiện lỗi liên quan đến:

app_kaggle.py

kiểm tra thư mục hiện tại:

```powershell
dir
```

Đảm bảo Terminal đang đứng trong thư mục chứa `app_kaggle.py`.

---

### Không tìm thấy Streamlit

Nếu xuất hiện:

No module named streamlit

kích hoạt `.venv`:

```powershell
.\.venv\Scripts\Activate.ps1
```

Sau đó cài lại thư viện:

```powershell
python -m pip install -r requirements.txt
```

---

### Không tìm thấy Pandas

Nếu xuất hiện:

ModuleNotFoundError: No module named 'pandas'

chạy:

```powershell
python -m pip install -r requirements.txt
```

---

## 14. Tóm tắt lệnh chạy lần đầu

```powershell
python -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

python -m streamlit run app_kaggle.py
```

---

## 15. Tóm tắt lệnh những lần sau

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1

python -m streamlit run app_kaggle.py
```

Không cần tạo lại `.venv` và không cần cài lại thư viện nếu `requirements.txt` không thay đổi.

---

## 16. Mục tiêu đề tài

Đề tài **Xây dựng hệ thống hỗ trợ tư vấn điện thoại** nhằm ứng dụng kiến thức về hệ trợ giúp quyết định, xử lý dữ liệu và Machine Learning vào bài toán thực tế.

Hệ thống hỗ trợ người dùng phân tích các lựa chọn và tìm ra những mẫu điện thoại phù hợp với nhu cầu và ngân sách, giúp quá trình lựa chọn sản phẩm trở nên nhanh chóng và thuận tiện hơn.