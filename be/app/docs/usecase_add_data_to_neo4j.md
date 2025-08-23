# Đặc tả Usecase: Thêm dữ liệu vào Neo4j

## 1. Thông tin chung

| Tên usecase | Thêm dữ liệu vào Neo4j |
|-------------|------------------------|
| ID | UC-NEO4J-001 |
| Mô tả ngắn | Chức năng xử lý và thêm dữ liệu từ tài liệu đã phân đoạn vào cơ sở dữ liệu đồ thị Neo4j |
| Actor chính | Hệ thống |
| Actor phụ | Người dùng (gián tiếp) |
| Điều kiện tiên quyết | - Tài liệu đã được tải lên và xử lý thành các đoạn văn bản (sentences)<br>- Đã có ID tài liệu (document_id)<br>- Các instance cần thiết đã được khởi tạo (LLM, Neo4j, PreProcessing) |
| Điều kiện sau | Dữ liệu từ tài liệu được lưu trữ trong cơ sở dữ liệu đồ thị Neo4j dưới dạng các thực thể và mối quan hệ |

## 2. Luồng sự kiện

### 2.1. Luồng cơ bản

| STT | Actor | Hệ thống |
|-----|-------|----------|
| 1 | | Nhận các đoạn văn bản (sentences) và ID tài liệu (document_id) |
| 2 | | Lấy các instance cần thiết: llama_title, llama_content, neo, pre_processing |
| 3 | | Thiết lập prompt cho mô hình LLM để tạo tiêu đề (llama_title) |
| 4 | | Với mỗi đoạn văn bản: <br>- Đặt đoạn văn bản làm đầu vào cho mô hình LLM<br>- Tạo tiêu đề cho đoạn văn bản<br>- Chuyển đổi tiêu đề thành định dạng JSON<br>- Thêm tiêu đề vào danh sách titles |
| 5 | | Thiết lập prompt cho mô hình LLM để trích xuất thực thể và mối quan hệ (llama_content) |
| 6 | | Với mỗi đoạn văn bản: <br>- Đặt đoạn văn bản làm đầu vào cho mô hình LLM<br>- Trích xuất thông tin về thực thể và mối quan hệ<br>- Chuyển đổi kết quả thành định dạng JSON<br>- Thêm kết quả vào danh sách entities_relationship |
| 7 | | Tạo mối quan hệ "BAO_GỒM" giữa nút "General" (tài liệu) và nút Document với ID tài liệu |
| 8 | | Tạo mối quan hệ "BAO_GỒM" giữa nút Document và các nút tiêu đề (Part) |
| 9 | | Tạo mối quan hệ giữa các nút tiêu đề (Part) và các thực thể được trích xuất |
| 10 | | Trả về thông báo thành công cùng với document_id |

### 2.2. Luồng thay thế

| STT | Điều kiện | Hành động |
|-----|----------|-----------|
| 4a | Quá trình tạo tiêu đề gặp lỗi | Ghi log lỗi và tiếp tục với đoạn văn bản tiếp theo |
| 6a | Quá trình trích xuất thực thể và mối quan hệ gặp lỗi | Ghi log lỗi và tiếp tục với đoạn văn bản tiếp theo |

### 2.3. Luồng ngoại lệ

| STT | Điều kiện | Hành động |
|-----|----------|-----------|
| 2a | Không thể lấy được các instance cần thiết | Ghi log lỗi và ném ngoại lệ HTTP 500 |
| 7a-9a | Lỗi khi thêm dữ liệu vào Neo4j | Ghi log lỗi và ném ngoại lệ HTTP 500 với thông báo "Error processing file in neo4j" |

## 3. Yêu cầu đặc biệt

### 3.1. Yêu cầu phi chức năng

- **Hiệu suất**: Chức năng cần xử lý hiệu quả với các tài liệu lớn
- **Độ tin cậy**: Cần đảm bảo dữ liệu được lưu trữ chính xác trong Neo4j
- **Khả năng mở rộng**: Có thể xử lý nhiều loại tài liệu khác nhau
- **Bảo mật**: Đảm bảo dữ liệu được lưu trữ an toàn

### 3.2. Yêu cầu kỹ thuật

- Cần có kết nối ổn định đến cơ sở dữ liệu Neo4j
- Mô hình LLM cần được cấu hình đúng để tạo tiêu đề và trích xuất thông tin
- Cần xử lý giới hạn tốc độ API của mô hình LLM (sleep 45 giây sau mỗi 2 lần gọi)
- Cần xử lý đúng định dạng JSON cho dữ liệu trích xuất

## 4. Mô tả chi tiết

### 4.1. Cấu trúc dữ liệu

#### 4.1.1. Đầu vào
- `sentences`: Danh sách các đoạn văn bản đã được phân đoạn từ tài liệu
- `document_id`: ID của tài liệu

#### 4.1.2. Đầu ra
- Thông báo thành công và document_id
- Trong trường hợp lỗi: HTTP Exception với mã 500 và thông báo lỗi

### 4.2. Quy trình xử lý

1. **Tạo tiêu đề**:
   - Sử dụng prompt `create_title()` để hướng dẫn mô hình LLM tạo tiêu đề
   - Với mỗi đoạn văn bản, tạo một tiêu đề phù hợp
   - Chuyển đổi tiêu đề thành định dạng JSON
   - Thêm vào danh sách `titles`

2. **Trích xuất thực thể và mối quan hệ**:
   - Sử dụng prompt `extract_entities_relationship_from_text()` để hướng dẫn mô hình LLM trích xuất thông tin
   - Với mỗi đoạn văn bản, trích xuất các thực thể và mối quan hệ
   - Chuyển đổi kết quả thành định dạng JSON
   - Thêm vào danh sách `entities_relationship`

3. **Xây dựng đồ thị**:
   - Tạo mối quan hệ giữa nút "General" (tài liệu) và nút Document
   - Tạo mối quan hệ giữa nút Document và các nút tiêu đề (Part)
   - Tạo mối quan hệ giữa các nút tiêu đề và các thực thể được trích xuất

### 4.3. Xử lý lỗi

- Ghi log chi tiết về lỗi
- Ném ngoại lệ HTTP với mã 500 và thông báo lỗi cụ thể
- Đảm bảo tài nguyên được giải phóng đúng cách

## 5. Ví dụ

### 5.1. Ví dụ đầu vào

```python
sentences = [
    "Đại sứ Iran tại LHQ cho rằng làm giàu uranium là quyền không thể tước bỏ của mỗi quốc gia, khẳng định Tehran sẽ không từ bỏ hoạt động này.",
    "Trong cuộc phỏng vấn với kênh CBS News của Mỹ ngày 29/6, đại sứ Iran tại Liên Hợp Quốc Amir Saeid Iravani được hỏi liệu Tehran có ý định phục hồi chương trình làm giàu uranium trên lãnh thổ của mình hay không."
]
document_id = "doc_123456"
```

### 5.2. Ví dụ đầu ra

```json
{
  "message": "File uploaded and processed successfully for neo4j",
  "data": "doc_123456"
}
```

### 5.3. Ví dụ dữ liệu trong Neo4j

```
(General {name: "tài liệu"}) -[:BAO_GỒM]-> (Document {name: "doc_123456"})
(Document {name: "doc_123456"}) -[:BAO_GỒM]-> (Part {name: "quan điểm của iran về làm giàu uranium"})
(Part {name: "quan điểm của iran về làm giàu uranium"}) -[:BAO_GỒM]-> (Person {name: "Amir Saeid Iravani", title: "Đại sứ Iran tại LHQ"})
(Person {name: "Amir Saeid Iravani"}) -[:là_đại_sứ_của]-> (Country {name: "Iran"})
...
```

## 6. Ghi chú

- Chức năng này là một phần của quy trình xử lý tài liệu, được gọi sau khi tài liệu đã được tải lên và xử lý thành các đoạn văn bản
- Cần đảm bảo rằng các instance cần thiết đã được khởi tạo trước khi gọi chức năng này
- Cần xử lý giới hạn tốc độ API của mô hình LLM để tránh bị chặn
- Cấu trúc đồ thị trong Neo4j cần được thiết kế để hỗ trợ truy vấn hiệu quả