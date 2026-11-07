# Blue Mart Retail Analytics

Phân tích hiệu quả kinh doanh bán lẻ đa kênh bằng **Power BI, Python và Streamlit**.

## Tổng quan

Blue Mart Retail Analytics phân tích doanh thu, lợi nhuận gộp, hiệu quả chiết khấu và đóng góp của danh mục sản phẩm trong một chuỗi bán lẻ mô phỏng.

Dự án sử dụng dữ liệu từ **01/01/2021 đến 31/10/2025**, bao gồm **50 cửa hàng, 200 SKU và 5 kênh bán hàng**. Kết quả được trình bày qua bốn trang dashboard Power BI và phiên bản web tương tác bằng Streamlit.

## Bài toán kinh doanh

- Doanh thu và lợi nhuận gộp thay đổi như thế nào theo thời gian?
- Biến động kinh doanh tập trung ở những kênh bán và cửa hàng nào?
- Mức chiết khấu nào xuất hiện rủi ro bán dưới giá vốn?
- Những ngành hàng và SKU nào đóng góp chính vào kết quả kinh doanh?

## Dữ liệu

| Thành phần | Phạm vi |
| --- | --- |
| Thời gian | 01/01/2021–31/10/2025 |
| Dòng bán sau xử lý | 641.126 |
| Sản phẩm | 200 SKU |
| Cửa hàng | 50 |
| Thành phố | Dubai, Abu Dhabi, Sharjah |
| Kênh bán | Store, Website, MobileApp, Amazon.ae, Noon |
| Bảng dữ liệu chính | `sales`, `skus`, `stores` |

> Mỗi dòng bán ghi nhận một SKU và có thể gồm nhiều đơn vị sản phẩm. Số dòng bán không tương đương số đơn hàng hoặc số khách hàng.

## Công cụ sử dụng

| Công cụ | Vai trò |
| --- | --- |
| Python, Pandas | Chuẩn hóa, kiểm tra và tổng hợp dữ liệu |
| Power Query | Nạp dữ liệu và thiết lập kiểu dữ liệu |
| Power BI, DAX | Xây dựng mô hình, chỉ số và dashboard |
| Streamlit | Xây dựng giao diện web tương tác |
| Plotly | Trực quan hóa dữ liệu trên web |

## Quy trình thực hiện

1. **Xác định bài toán:** lựa chọn câu hỏi kinh doanh và chỉ số cần theo dõi.
2. **Chuẩn bị dữ liệu:** xử lý bản ghi trùng, chuẩn hóa ngày tháng, giá bán, chiết khấu và tên kênh.
3. **Xây dựng mô hình:** liên kết dữ liệu bán hàng với danh mục sản phẩm, cửa hàng và bảng thời gian.
4. **Thiết lập chỉ số:** tính doanh thu, lợi nhuận gộp, biên lợi nhuận gộp, sản lượng và số dòng bán.
5. **Thiết kế dashboard:** tổ chức nội dung thành bốn trang theo từng nhóm câu hỏi.
6. **Kiểm tra và phân tích:** đối chiếu tổng số liệu, kiểm tra bộ lọc và diễn giải kết quả.

## Nội dung dashboard

### 1. Tổng quan và mùa vụ

- Theo dõi doanh thu, lợi nhuận gộp, biên lợi nhuận gộp, dòng bán và sản lượng.
- Phân tích xu hướng theo tháng và so sánh cùng kỳ.
- Đánh giá đóng góp doanh thu và lợi nhuận của từng loại ngày.

### 2. Kênh và điểm bán

- So sánh cơ cấu doanh thu giữa các kênh.
- Phân tích biến động dòng bán và doanh thu bình quân mỗi dòng.
- Đối chiếu doanh thu và biên lợi nhuận gộp của cửa hàng với các mức tham chiếu.

### 3. Chiến dịch và chiết khấu

- Phân tích phân bố ngày chiến dịch theo thời gian.
- So sánh doanh thu, lợi nhuận gộp và dòng bán bình quân ngày.
- Kiểm tra lãi gộp và tỷ lệ dòng bán lỗ theo từng mức chiết khấu.

> Ngày chiến dịch được quy ước là ngày có ít nhất 50% dòng bán được chiết khấu trên toàn chuỗi. Đây là nhãn suy ra từ dữ liệu, chưa phải lịch chiến dịch được xác nhận.

### 4. Danh mục sản phẩm

- Đánh giá đóng góp của ngành hàng, thương hiệu và SKU.
- So sánh tỷ trọng doanh thu với tỷ trọng sản lượng.
- Phân tích biên lợi nhuận gộp và phân nhóm ABC theo doanh thu.

## Kết quả tổng quan

Các chỉ số sử dụng toàn kỳ và tất cả kênh bán.

| Chỉ số | Kết quả |
| --- | ---: |
| Doanh thu | 73.149.339,22 |
| Lợi nhuận gộp | 21.078.696,70 |
| Biên lợi nhuận gộp | 28,82% |
| Dòng bán | 641.126 |
| Sản lượng | 1.675.836 đơn vị |
| Ngày chiến dịch | 800 |
| Ngày thường | 965 |

Giá trị tiền giữ nguyên đơn vị của bộ dữ liệu.

## Insight nổi bật

### Lợi nhuận gộp giảm nhanh hơn doanh thu

Trong **T1–T10/2025 so với T1–T10/2024**, doanh thu giảm **3,37%**, trong khi lợi nhuận gộp giảm **6,60%**. Biên lợi nhuận gộp giảm từ **29,47% xuống 28,49%**.

Kết quả cho thấy cần theo dõi phần lãi giữ lại bên cạnh quy mô bán hàng.

### Ngày chiến dịch có quy mô bán lớn nhưng biên thấp hơn

Nhóm ngày chiến dịch chiếm **45,3% số ngày**, tạo **61,7% doanh thu**. Doanh thu bình quân ngày cao hơn ngày thường **94,49%**, nhưng lợi nhuận gộp bình quân ngày chỉ cao hơn **50,60%**.

Đây là khác biệt quan sát được, chưa chứng minh tác động nhân quả của khuyến mãi.

### SKU doanh thu cao vẫn có rủi ro chiết khấu

**Chargers_1072** đứng thứ **2 về doanh thu** nhưng thứ **19 về lợi nhuận gộp**, với biên **15,85%**.

Các mức giảm **25–35%** tạo **263 dòng bán lỗ**, tương ứng tổng lỗ gộp **9.667,08**. Kết quả hỗ trợ việc rà soát giá vốn và giới hạn ưu đãi theo từng SKU.

### Doanh thu tập trung vào một phần danh mục

**62/200 SKU tạo 69,72% doanh thu**, trong khi Electronics đóng góp **55,72% doanh thu toàn chuỗi**.

Tuy nhiên, nhóm C vẫn tạo khoảng **2,13 triệu lợi nhuận gộp**, nên tỷ trọng doanh thu thấp chưa đủ để quyết định loại sản phẩm.

## Đề xuất kinh doanh

- **Kiểm soát chiết khấu theo SKU:** rà soát giá vốn và giới hạn ưu đãi, ưu tiên các mã có dòng bán dưới giá vốn.
- **Đánh giá toàn giai đoạn:** theo dõi tổng lợi nhuận gộp, doanh thu và sản lượng thay vì chỉ nhìn tháng tăng trưởng.
- **Theo dõi sản phẩm chủ lực:** kết hợp doanh thu, lợi nhuận gộp, biên lợi nhuận và rủi ro chiết khấu.
- **Đánh giá cửa hàng theo nhóm tương đồng:** xem xét quy mô chênh lệch và xu hướng trước khi đề xuất can thiệp.

Các hành động trên là đề xuất kiểm tra và thử nghiệm; dự án chưa đo lường hiệu quả sau triển khai.

## Phạm vi và giới hạn

- Dữ liệu mô phỏng, phục vụ phân tích tình huống kinh doanh.
- Năm 2025 chỉ có dữ liệu đến tháng 10; so sánh tăng trưởng sử dụng cùng kỳ.
- Lợi nhuận gộp chưa trừ phí sàn, giao hàng và chi phí vận hành.
- Không có mã đơn hàng hoặc khách hàng để tính AOV và retention.
- Phiên bản Streamlit tái dựng nội dung phân tích; giao diện và một số tương tác có thể khác Power BI.
