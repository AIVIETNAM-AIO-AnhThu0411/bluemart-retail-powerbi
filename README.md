# Blue Mart Retail Analytics — Streamlit Portfolio

Web dashboard tương tác xây dựng từ **dữ liệu Blue Mart thật trong project đã lưu** (không phải dữ liệu ngẫu nhiên). Ứng dụng chạy độc lập với Power BI; phù hợp để giới thiệu trong CV/Portfolio.

## 1. Bạn nhận được gì?

- **4 trang:** (1) Tổng quan & mùa vụ, (2) Kênh & điểm bán, (3) Chiến dịch & chiết khấu, (4) Danh mục sản phẩm.
- **Bộ lọc toàn cục:** khoảng thời gian, thành phố, loại cửa hàng, kênh bán, ngành hàng và thương hiệu.
- **KPI:** Doanh thu, lợi nhuận gộp, GM%, số lượng hàng bán ra, dòng bán.
- **Biểu đồ tương tác:** di chuột, zoom, lọc, xem tooltip và tải dữ liệu tổng hợp.
- **Dữ liệu đã có sẵn:** `data/sales.csv.gz`, `data/skus.csv`, `data/stores.csv`. Không cần kết nối Power BI Service và không cần file `.pbix` để chạy.

> Đây là **bản tái dựng web**, không phải bản sao pixel-perfect mọi visual, slicer, tooltip và DAX của `.pbix`. Các KPI cốt lõi đã được đối chiếu với dữ liệu nguồn.

## 2. Chạy trên Windows (dễ nhất)

1. Cài [Python](https://www.python.org/downloads/) 3.11 hoặc 3.12 và chọn **Add python.exe to PATH** khi cài.
2. Giải nén toàn bộ ZIP (không chạy trực tiếp bên trong ZIP).
3. Nhấp đúp vào **`run_windows.bat`**. Lần đầu máy sẽ tạo môi trường Python và cài các thư viện; cần kết nối Internet.
4. Khi thấy `Local URL: http://localhost:8501`, mở đường dẫn đó trong trình duyệt.
5. Để dừng web, quay lại cửa sổ lệnh và nhấn `Ctrl+C`.

### Cách chạy bằng PowerShell (nếu muốn tự gõ lệnh)

Mở PowerShell bên trong thư mục đã giải nén, chạy **lần lượt**:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**Không sao chép phần dấu nhắc `PS C:\...>`** từ hướng dẫn vào PowerShell.

Bạn cũng có thể xác minh số liệu:

```powershell
.\.venv\Scripts\python.exe validate_data.py
```

Kết quả mong đợi: `OK: Blue Mart KPI khop nguon.`

## 3. Triển khai thành link công khai miễn phí

### Bước A — Tạo GitHub repository

1. Đăng nhập [github.com](https://github.com).
2. Tạo repository mới, ví dụ `blue-mart-retail-analytics`, chọn **Public**.
3. Tải **toàn bộ nội dung sau khi giải nén** (không tải file ZIP nguyên khối) lên thư mục gốc repository. Đảm bảo giữ đường dẫn `data/` và `.streamlit/`.
4. Kiểm tra GitHub hiển thị `app.py`, `core.py`, `requirements.txt`, `data/sales.csv.gz`, `data/skus.csv`, `data/stores.csv`.

**Lưu ý bảo mật:** Khi repository công khai, file dữ liệu đi kèm cũng công khai. Chỉ làm vậy nếu bạn có quyền công bố dữ liệu Blue Mart. Nếu dữ liệu không được phép đăng, bạn cần có giải pháp ẩn dữ liệu hoặc thay dữ liệu bằng bộ công khai phù hợp trước khi triển khai.

### Bước B — Đăng lên Streamlit Community Cloud

1. Mở [share.streamlit.io](https://share.streamlit.io), đăng nhập bằng GitHub.
2. Chọn **Create app** → **Yup, I have an app**.
3. Chọn repo `blue-mart-retail-analytics`, branch `main`, entrypoint `app.py`.
4. Đặt tên URL nếu còn trống, ví dụ `blue-mart-retail-portfolio`.
5. Chọn **Deploy** và kiểm tra ứng dụng chạy được.
6. Vào link dạng `https://blue-mart-retail-portfolio.streamlit.app/` (đây là **ví dụ**, không phải link đã triển khai). Link thật sẽ được Streamlit cấp sau khi bạn deploy.
7. Mở trong chế độ ẩn danh để xác nhận **nhà tuyển dụng không cần đăng nhập**.

Tham khảo tài liệu chính thức: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 4. Cấu trúc thư mục

```text
BlueMart_Streamlit_Portfolio/
├── app.py                 # Giao diện Streamlit (4 trang)
├── core.py                # Dữ liệu, join, lọc và KPI
├── validate_data.py       # Kiểm tra số liệu
├── requirements.txt       # Thư viện cần cài
├── run_windows.bat        # Nhấp đúp để chạy trên Windows
├── .streamlit/
│   └── config.toml        # Màu sắc ứng dụng
└── data/
    ├── sales.csv.gz       # 641,126 dòng
    ├── skus.csv           # 200 SKU
    └── stores.csv         # 50 cửa hàng
```

## 5. Cách tính KPI đã đối chiếu với Power BI

```text
Revenue              = SUM(sales[total_value])
Gross Profit         = SUM(sales[total_value] - sales[quantity] * RELATED(skus[cost_price]))
Gross Margin %       = Gross Profit / Revenue
Units Sold           = SUM(sales[quantity])
Sales Rows           = COUNTROWS(sales)
Transactions         = DISTINCTCOUNT(sales[sale_id])
Campaign day         = % dòng giảm giá trong ngày >= 50% (trên toàn bộ nguồn)
```

**Mốc kiểm tra trên toàn kỳ 01/01/2021–31/10/2025:**

| Chỉ tiêu | Kết quả |
| --- | ---: |
| Doanh thu | 73,149,339.22 |
| Lợi nhuận gộp | 21,078,696.70 |
| Biên lợi nhuận gộp | 28.81598% |
| Dòng bán / Sale IDs duy nhất | 641,126 |
| Số lượng đơn vị | 1,675,836 |
| SKUs / Stores | 200 / 50 |
| Ngày chiến dịch / ngày thường | 800 / 965 |

**Lưu ý:** Doanh thu/GP giữ nguyên đơn vị tiền của dataset; không tự gán USD, VND hay AED. Năm 2025 chỉ tới tháng 10, nên không so sánh thẳng doanh thu cả năm với 2024 như hai kỳ 12 tháng tương đương.

## 6. Mẹo Portfolio

Thêm link Streamlit vào CV dưới tên **Blue Mart Retail Analytics | Interactive Dashboard**. Kèm 2–3 dòng: vấn đề kinh doanh, công cụ (Python/Streamlit/Plotly/Pandas), và insight có kiểm chứng. Có thể để ảnh chụp Power BI gốc bên cạnh web demo để nhà tuyển dụng nhìn thấy thiết kế BI nguyên bản.

## 7. Giới hạn

- Ứng dụng **không tự đồng bộ** khi bạn sửa báo cáo `.pbix` hoặc dữ liệu trong Power BI Service.
- Thiết kế web và một số biểu đồ có thể khác dashboard Power BI; KPI cốt lõi đã được kiểm tra.
- Gói Community Cloud miễn phí có giới hạn tài nguyên và ứng dụng có thể ngủ khi không được sử dụng; cần kiểm thử trên link thực tế.
- Nếu bạn phải công bố báo cáo nhưng **không được công bố dữ liệu chi tiết**, không nên đưa các CSV nguồn trong repo public.
