def first_decision():
    return """
Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Với câu hỏi sau, hãy trích xuất thông tin từ câu hỏi theo yêu cầu.

### Câu hỏi: '{question}'
Lưu ý:
1. Không giải thích gì thêm chỉ làm theo hướng dẫn
2. Cần có tài liệu để trả lời câu hỏi đã cho, và mục tiêu là tìm kiếm các tài liệu hữu ích. Mỗi thực thể trong đồ thị tri thức được liên kết với một tài liệu.
3. Dựa trên các thực thể và quan hệ đã trích xuất. Hãy phản hồi theo dạng sau
{{
  "extract_01": <trích xuất như ví dụ, không được ghi chuỗi theo kiểu lồng chuỗi>,
  "extract_02": <trích xuất như ví dụ, không được ghi chuỗi theo kiểu lồng chuỗi>,
  ...
}}
4. Chỉ trích xuất các đối tượng là câu hỏi, không trích xuất các đối tượng khác

ví dụ 1: Các khoa có số điện thoại là 028372 mà giảng dạy về ngoại ngữ?
{{
  "extrac_01": "khoa có số điện thoại là 028372",
  "extrac_02": "giảng dạy về ngoại ngữ"
}}
ví dụ 2: Ngành quản trị kinh doanh do khoa nào quản lý và số điện thoại của khoa đó là gì?
{{
  "extract_01": "quản trị kinh doanh",
  "extract_01": "số điện thoại của khoa"
}}

ví dụ 3: Câu lạc bộ nào thuộc lĩnh vực học thuật, ngoại ngữ mà do Nguyễn Thị Ngọc Hân chủ nhiệm?
{{
  "extract_01": "học thuật, ngoại ngữ",
  "extract_01": "Nguyễn Thị Ngọc Hân chủ nhiệm"
}}

ví dụ 4: Ký túc xá tại Đại học Nông Lâm TP.HCM có số lượng là bao nhiêu?
{{
  "extract_01": "Ký túc xá tại Đại học Nông Lâm TP.HCM"
}}

ví dụ 5: Viện nghiên cứu tại Đại học Nông Lâm TP.HCM có số lượng là bao nhiêu?
{{
  "extract_01": "Viện nghiên cứu tại Đại học Nông Lâm TP.HCM"
}}

ví dụ 6: Số ngành đào tạo thuộc Khoa Chăn nuôi - Thú y của Đại học Nông Lâm TP.HCM là bao nhiêu?
{{
  "extract_01": "Khoa Chăn nuôi - Thú y của Đại học Nông Lâm TP.HCM"
}}

ví dụ 7: Trang web nào cung cấp thông tin về sinh hoạt công dân - sinh viên của Trường Đại học Nông Lâm TP.HCM?
{{
  "extract_01": "sinh hoạt công dân - sinh viên của Trường Đại học Nông Lâm TP.HCM"
}}

ví dụ 8: Chiến dịch Mùa hè xanh tại Trường Đại học Nông Lâm TP.HCM diễn ra vào thời điểm nào?
{{
  "extract_01": "Chiến dịch Mùa hè xanh tại Trường Đại học Nông Lâm TP.HCM"
}}

ví dụ 9: Slogan của BEC English Club tại Trường Đại học Nông Lâm TP.HCM là gì?
{{
  "extract_01": "BEC English Club tại Trường Đại học Nông Lâm TP.HCM"
}}

ví dụ 10: Hoạt động chính của CLB Nông Lâm Radio tại Đại học Nông Lâm TP.HCM là gì?
{{
  "extract_01": "CLB Nông Lâm Radio tại Đại học Nông Lâm TP.HCM"
}}
"""

def self_reflection():
    return """
Tài liệu đã truy xuất không đúng. Trả lời lại dựa trên các thực thể chủ đề mới được trích xuất. Hãy dựa vào câu hỏi và tiếp tục trích xuất theo feedback
### feedback: '{feedback}'
### Câu hỏi: '{question}'
### Câu trả lời: '{answer}'
Với câu hỏi sau hãy trích xuất các thực thể chủ đề và các quan hệ hữu ích từ câu hỏi.

Lưu ý:
1. CHỈ TRÍCH XUẤT LẠI VỚI CÂU HỎI CHƯA ĐƯỢC TRẢ LỜI HOẶC CHƯA CÓ THÔNG TIN. CÂU HỎI ĐÃ ĐƯỢC TRẢ LỜI RỒI THÌ KHÔNG CẦN ĐỂ TĂNG TỐC ĐỘ TRUY XUẤT
2. Không giải thích gì thêm chỉ làm theo hướng dẫn
3. Trích xuất tối đa 3 đối tượng
4. Chỉ trích xuất các đối tượng hữu ích có tác dụng trả lời câu hỏi, các thông tin thêm trong câu hỏi thì không quan tâm
5. Hãy phản hồi theo dạng sau:
{{
  "extract_01": <trích xuất như ví dụ, không được ghi chuỗi theo kiểu lồng chuỗi>,
  "extract_02": <trích xuất như ví dụ, không được ghi chuỗi theo kiểu lồng chuỗi>,
  ...
}}

ví dụ 1: Các khoa có số điện thoại là 028372 mà giảng dạy về ngoại ngữ?
{{
  "extrac_01": "khoa có số điện thoại là 028372",
  "extrac_02": "giảng dạy về ngoại ngữ"
}}
ví dụ 2: Ngành quản trị kinh doanh do khoa nào quản lý và số điện thoại của khoa đó là gì?
{{
  "extract_01": "quản trị kinh doanh",
  "extract_01": "số điện thoại của khoa"
}}

ví dụ 3: Câu lạc bộ nào thuộc lĩnh vực học thuật, ngoại ngữ mà do Nguyễn Thị Ngọc Hân chủ nhiệm?
{{
  "extract_01": "học thuật, ngoại ngữ",
  "extract_01": "Nguyễn Thị Ngọc Hân chủ nhiệm"
}}

ví dụ 4: Ký túc xá tại Đại học Nông Lâm TP.HCM có số lượng là bao nhiêu?
{{
  "extract_01": "Ký túc xá tại Đại học Nông Lâm TP.HCM"
}}

ví dụ 5: Viện nghiên cứu tại Đại học Nông Lâm TP.HCM có số lượng là bao nhiêu?
{{
  "extract_01": "Viện nghiên cứu tại Đại học Nông Lâm TP.HCM"
}}

ví dụ 6: Số ngành đào tạo thuộc Khoa Chăn nuôi - Thú y của Đại học Nông Lâm TP.HCM là bao nhiêu?
{{
  "extract_01": "Khoa Chăn nuôi - Thú y của Đại học Nông Lâm TP.HCM"
}}

ví dụ 7: Trang web nào cung cấp thông tin về sinh hoạt công dân - sinh viên của Trường Đại học Nông Lâm TP.HCM?
{{
  "extract_01": "sinh hoạt công dân - sinh viên của Trường Đại học Nông Lâm TP.HCM"
}}

ví dụ 8: Chiến dịch Mùa hè xanh tại Trường Đại học Nông Lâm TP.HCM diễn ra vào thời điểm nào?
{{
  "extract_01": "Chiến dịch Mùa hè xanh tại Trường Đại học Nông Lâm TP.HCM"
}}

ví dụ 9: Slogan của BEC English Club tại Trường Đại học Nông Lâm TP.HCM là gì?
{{
  "extract_01": "BEC English Club tại Trường Đại học Nông Lâm TP.HCM"
}}

ví dụ 10: Hoạt động chính của CLB Nông Lâm Radio tại Đại học Nông Lâm TP.HCM là gì?
{{
  "extract_01": "CLB Nông Lâm Radio tại Đại học Nông Lâm TP.HCM"
}}
"""


def generator():
    return """
Bạn là chuyên gia trả lời câu hỏi dựa trên tài liệu cung cấp, tuân theo khuôn mẫu. Nhiệm vụ:
1. Trả lời tất cả câu hỏi chính xác dựa trên tài liệu.
2. Trình bày rõ ràng, liệt kê (nếu có) đánh số thứ tự và in đậm.
3. Nếu thiếu thông tin, trả lời: "Không có thông tin". Nếu có, diễn đạt lại.
4. Phản hồi bằng tiếng việt theo cách tự nhiên nhất có chủ ngữ vị ngữ đầy đủ và không giải thích thêm.
### Câu hỏi: {question}
### Tài liệu: {references}
"""

# cải tiển: thêm các chỉ số để đánh giá câu trả lời
def valid_stsv():
    return """
Bạn là trợ lý phân tích câu trả lời theo khuôn mẫu.

Câu hỏi: {question}
Câu trả lời: {answer}
Nếu câu trả lời 'không có thông tin' thì trả lời no mà không cần suy nghĩ
Nhiệm vụ:
1. Xác định loại của câu trả lời (what, who, where, how, why).
2. Kiểm tra câu trả lời có khớp với câu hỏi không:
2.1 Nếu khớp, trả lời "yes".
2.2 Nếu 'không có thông tin' hoặc câu trả lời không thỏa mãn thì trả lời 'no'.
Trả lời: Chỉ 1 từ ("yes" hoặc "no")."""

def commentor():
    return """
Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. 
Hãy phản hồi sửa lỗi một cách chi tiết nhất có thể cho, chỉ ra lỗi được liệt kê dưới đây:
 - Nếu tài liệu không có ý nghĩa. Ưu tiên dự đoán lại mục lục.
 - Nếu tài liệu trống hãy yêu cầu trích xuất lại thực thể

### Câu hỏi: {question}
### Thực thể chủ đề: {entities}
### Tài liệu khả thi: {references}

Lưu ý:
1. Hiện tại chỉ có 2 nguồn là 'TEXT' và 'GRAPH'. KHÔNG ĐỀ NGHỊ NGUỒN KHÁC NGOÀI 2 CÁI TRÊN

Phản hồi theo mẫu:
1. <hãy chỉ ra lỗi>
2. <đề xuất ngắn gọn, rõ ràng, cụ thể để sửa lỗi tương ứng với 'TEXT' hoặc 'GRAPH', mỗi lần chỉ đề xuất 1 nguồn, không tính tới bước tiếp theo>
"""

def extract_entities_relationship_from_text():
    return """    
Bạn là một hệ thống trích xuất thông tin từ văn bản. Tuân theo khuôn mẫu, Nhiệm vụ của bạn là:
Văn bản tôi truyền vào có thể là một bài viết khoa học về một chủ đề chuyên môn về bất kỳ lĩnh vực nào. MỌI ĐOẠN VĂN BẢN ĐỀU PHẢI TRÍCH XUẤT, KHÔNG THAN PHIỀN, KHÔNG GIẢI THÍCH, KHÔNG MỞ ĐẦU, KHÔNG KẾT THÚC, CHỈ LÀM THEO SỰ HƯỚNG DẪN
1. Trích xuất tất cả các thực thể có trong đoạn văn bản.
   - Mỗi thực thể cần có tên(name) và loại(type).
   - Loại của thực thể (ví dụ: person, organization, location, date, v.v.) phải được ghi bằng TIÊNG ANH, nếu có 2 từ trở lên thì SỬ DỤNG PascalCase.

2. Xác định các mối quan hệ giữa các thực thể.
   - Mỗi mối quan hệ phải có nguồn(source), đích(target) và tên mối quan hệ(relation).
   - Tên mối quan hệ phải được ghi thường, TIẾNG VIỆT, CÓ DẤU, nếu có 2 từ trở lên thì PHÂN CÁCH NHAU BỞI DẤU "_".(ví dụ: "THỦ_ĐÔ_CỦA", "TẠO_RA").
   - Nếu một mối quan hệ có ý nghĩa giống nhau ở nhiều trường hợp, hãy thống nhất sử dụng một tên mối quan hệ duy nhất và không thêm từ gì khác. Ví dụ: nếu "tphcm ở việt nam" được quy định là mối quan hệ "Ở", thì với mọi trường hợp tương tự, mối quan hệ phải là "Ở".

3. Trả về kết quả dưới dạng JSON với các trường:
   - "entities": Danh sách các thực thể. Mỗi thực thể có các thuộc tính "name" và "type".
   - "relationships": Danh sách các mối quan hệ. Mỗi mối quan hệ có các thuộc tính "source", "target", "type_source", "type_target" và "relation".

Yêu cầu:
- Trả về kết quả dưới dạng JSON với các trường: relationships.
- Mỗi relationship cần có source, target, type_source, type_target và relation.
- source và target sẽ là 1 json có các thuộc tính mặc định là name, ngoài ra sẽ có từ 2 ĐẾN 5 THUỘC TÍNH KHÁC NHAU tùy theo thông tin văn bản(giống như lưu trữ của Neo4j). TYPE KHÔNG CẦN GHI LẠI Thuộc tính ghi tiếng anh, còn giá trị ghi tiếng việt
- không giải thích gì thêm, không ghi mở đầu, kết thúc, thống kê. Chỉ phản hồi theo hướng dẫn
- HÃY TRÍCH XUẤT MỘT CÁCH CHI TIẾT NHẤT CÓ THỂ VÀ KHÔNG BỎ QUA BẤT CỨ MỐI QUAN HỆ NÀO
- CHỈ TRÍCH XUẤT TỪ THÔNG TIN MÀ TÔI CUNG CẤP, KHÔNG THÊM BẤT CỨ THÔNG TIN GÌ KHÁC BÊN NGOÀI.
---
### Giải thích:
1. **Relationship**:
   - Là mối quan hệ giữa các entity, ví dụ: "Alice knows Bob" → quan hệ Biết giữa Alice và Bob.

2. **Định dạng đầu ra**:
   - Sử dụng JSON để trả về kết quả một cách có cấu trúc, dễ dàng xử lý tiếp theo.

Ví dụ: 
Văn bản: Đại sứ Iran tại LHQ cho rằng làm giàu uranium là quyền không thể tước bỏ của mỗi quốc gia, khẳng định Tehran sẽ không từ bỏ hoạt động này. Trong cuộc phỏng vấn với kênh CBS News của Mỹ ngày 29/6, đại sứ Iran tại Liên Hợp Quốc Amir Saeid Iravani được hỏi liệu Tehran có ý định "phục hồi chương trình làm giàu uranium trên lãnh thổ của mình" hay không. Ông trả lời bằng cách trích dẫn điều khoản của Hiệp ước Không phổ biến vũ khí hạt nhân (NPT), trong đó nêu rõ các quốc gia có quyền sử dụng công nghệ hạt nhân vì mục đích hòa bình, trong đó có làm giàu uranium, miễn là công nghệ này vẫn nằm trong giới hạn nhất định.
Kết quả:
{
  "relationships": [
    {
      "source": {
        "name": "Amir Saeid Iravani",
        "title": "Đại sứ Iran tại LHQ"
      },
      "target": {
        "name": "Iran"
      },
      "type_source": "Person",
      "type_target": "Country",
      "relation": "là_đại_sứ_của"
    },
    {
      "source": {
        "name": "Amir Saeid Iravani",
        "title": "Đại sứ Iran tại LHQ"
      },
      "target": {
        "name": "LHQ",
        "full_name": "Liên Hợp Quốc"
      },
      "type_source": "Person",
      "type_target": "Organization",
      "relation": "làm_việc_tại"
    },
    {
      "source": {
        "name": "Iran"
      },
      "target": {
        "name": "uranium"
      },
      "type_source": "Country",
      "type_target": "ChemicalElement",
      "relation": "làm_giàu"
    },
    {
      "source": {
        "name": "Tehran"
      },
      "target": {
        "name": "Iran"
      },
      "type_source": "Location",
      "type_target": "Country",
      "relation": "là_thủ_đô_của"
    },
    {
      "source": {
        "name": "Amir Saeid Iravani",
        "title": "Đại sứ Iran tại LHQ"
      },
      "target": {
        "name": "CBS News",
        "country": "Mỹ",
        "interview_date": "29/6"
      },
      "type_source": "Person",
      "type_target": "Organization",
      "relation": "được_phỏng_vấn_bởi"
    },
    {
      "source": {
        "name": "CBS News"
      },
      "target": {
        "name": "Mỹ"
      },
      "type_source": "Organization",
      "type_target": "Country",
      "relation": "thuộc_về"
    },
    {
      "source": {
        "name": "Iran"
      },
      "target": {
        "name": "Hiệp ước Không phổ biến vũ khí hạt nhân",
        "acronym": "NPT",
        "content": "Các quốc gia có quyền sử dụng công nghệ hạt nhân vì mục đích hòa bình"
      },
      "type_source": "Country",
      "type_target": "Treaty",
      "relation": "trích_dẫn"
    }
  ]
}
"""

def extract_question_from_text():
    return """nhiệm vụ của bạn là sẽ tạo ra TẤT CẢ các câu hỏi từ văn bản từ đầu đến cuối mà không bỏ xót 1 chi tiết nào, các câu hỏi viết chữ thường, chỉ tạo ra danh sách câu hỏi và không thêm bất cứ thông tin gì"""


# yêu cầu llm dự đoán câu hỏi sẽ thuộc về phần nào trong sổ tay sinh viên
def predict_question_belong_to_stsv():
    return """
Bạn là trợ lý thông minh, có quyền truy cập vào mục lục chi tiết của tài liệu (dưới dạng các câu lệnh Neo4j) và các đoạn trích nội dung liên quan.  
Mục tiêu: trả lời câu hỏi của người dùng chính xác nhất dựa trên cả mục lục và nội dung được cung cấp.

QUY TẮC:
1. Mục lục thể hiện cấu trúc phân cấp của tài liệu.
   - Node có thể là Part, Section, Article.
   - Quan hệ :BAO_GỒM nghĩa là node cha chứa node con.
   - Lệnh MERGE chỉ để tạo node/quan hệ, bạn chỉ cần hiểu tên và mối quan hệ.

2. Khi nhận câu hỏi:
   a. Dựa vào mục lục, xác định phần/mục có khả năng chứa thông tin trả lời nhất.
   b. Đọc các đoạn văn bản được cung cấp (retrieved context).
   c. Kết hợp thông tin từ context và hiểu biết về vị trí trong mục lục để đưa ra câu trả lời.

3. Nếu câu hỏi thuộc về một phần không xuất hiện trong context được cung cấp, hãy chỉ ra rằng thông tin không có trong ngữ cảnh.

DỮ LIỆU MỤC LỤC:
     MERGE (a:Part {{name: 'nlu - định hướng trường đại học nghiên cứu'}})
            MERGE (b:Section {{name: 'quá trình hình thành và phát triển'}})
            MERGE (c:Section {{name: 'sứ mạng'}})
            MERGE (d:Section {{name: 'tầm nhìn'}})
            MERGE (e:Section {{name: 'giá trị cốt lõi'}})
            MERGE (f:Section {{name: 'mục tiêu chiến lược'}})
            MERGE (g:Section {{name: 'cơ sở vật chất'}})
            MERGE (h:Section {{name: 'các đơn vị trong trường'}})
            MERGE (i:Section {{name: 'các khoa - ngành đào tạo'}})
            MERGE (j:Section {{name: 'tuần sinh hoạt công dân - sinh viên'}})
            MERGE (k:Section {{name: 'hoạt động phong trào sinh viên'}})
            MERGE (l:Section {{name: 'câu lạc bộ (clb) - đội, nhóm'}})
            MERGE (m:Section {{name: 'cơ sở đào tạo'}})
            MERGE (a)-[:BAO_GỒM]->(b)
            MERGE (a)-[:BAO_GỒM]->(c)
            MERGE (a)-[:BAO_GỒM]->(d)
            MERGE (a)-[:BAO_GỒM]->(e)
            MERGE (a)-[:BAO_GỒM]->(f)
            MERGE (a)-[:BAO_GỒM]->(g)
            MERGE (a)-[:BAO_GỒM]->(h)
            MERGE (a)-[:BAO_GỒM]->(i)
            MERGE (a)-[:BAO_GỒM]->(j)
            MERGE (a)-[:BAO_GỒM]->(k)
            MERGE (a)-[:BAO_GỒM]->(l)
            MERGE (a)-[:BAO_GỒM]->(m)
            
            MERGE (n:Part {{name: 'học tập và rèn luyện'}})

            MERGE (o:Section {{name: 'quy chế sinh viên'}})
            MERGE (o2:Part {{name: 'chương 2: quyền và nghĩa vụ của sinh viên'}})
            MERGE (o2_4:Article {{name: 'điều 4: quyền của sinh viên'}})
            MERGE (o2_5:Article {{name: 'điều 5: nghĩa vụ của sinh viên'}})
            MERGE (o2_6:Article {{name: 'điều 6: các hành vi sinh viên không được làm'}})

            MERGE (p:Section {{name: 'quy chế học vụ'}})
            MERGE (p2:Part {{name: 'chương 2: lập kế hoạch và tổ chức giảng dạy'}})
            MERGE (p2_9:Article {{name: 'điều 9: tổ chức đăng ký học tập'}})
            MERGE (p2_10:Article {{name: 'điều 10: tổ chức lớp học phần'}})
            MERGE (p3:Part {{name: 'chương 3: đánh giá kết quả học tập và cấp bằng tốt nghiệp'}})
            MERGE (p3_12:Article {{name: 'điều 12: tổ chức thi kết thúc học phần'}})
            MERGE (p3_13:Article {{name: 'điều 13: đánh giá và tính điểm học phần'}})
            MERGE (p3_14:Article {{name: 'điều 14: xét tương đường và công nhận học phần của các cơ sở đào tạo khác'}})
            MERGE (p3_15:Article {{name: 'điều 15: đánh giá kết quả học tập theo học kỳ, năm học'}})
            MERGE (p3_16:Article {{name: 'điều 16: thông báo kết quả học tập'}})
            MERGE (p3_17:Article {{name: 'điều 17: điểm rèn luyện(đrl)'}})
            MERGE (p3_18:Article {{name: 'điều 18: xử lý kết quả học tập'}})
            MERGE (p3_19:Article {{name: 'điều 19: khóa luận, tiểu luận, tích lũy tín chỉ tốt nghiệp'}})
            MERGE (p3_20:Article {{name: 'điều 20: công nhận tốt nghiệp và cấp bằng tốt nghiêp'}})
            MERGE (p4:Part {{name: 'chương 4: những quy định khác đối với sinh viên'}})
            MERGE (p4_21:Article {{name: 'điều 21: nghỉ học tạm thời, thôi học'}})
            MERGE (p4_24:Article {{name: 'điều 24: học cùng lúc hai chương trình'}})

            MERGE (q:Section {{name: 'quy định về việc đào tạo trực tuyến'}})
            MERGE (q0_3:Article {{name: 'điều 3: hệ thống đào tạo trực tuyến tại trường đại học nông lâm tp.hcm'}})
            MERGE (q0_9:Article {{name: 'điều 9: đánh giá kết quả học tập trực tuyến'}})
            MERGE (q0_13:Article {{name: 'điều 13: quyền và trách nhiệm của sinh viên'}})

            MERGE (r:Section {{name: 'quy định khen thưởng, kỷ luật sinh viên'}})
            MERGE (r2:Part {{name: 'chương 2: khen thưởng'}})
            MERGE (r2_4:Article {{name: 'điều 4: nội dung khen thưởng'}})
            MERGE (r2_5:Article {{name: 'điều 5: khen thưởng đối với cá nhân và tập thể sinh viên đạt thành tích xứng đánh để biểu dương, khen thưởng'}})
            MERGE (r2_6:Article {{name: 'điều 6: khen thưởng đối với sinh viên tiêu biểu(svtb) vào cuối mỗi năm học'}})
            MERGE (r2_7:Article {{name: 'điều 7: khen thưởng đối với sinh viên là thủ khoa, á khoa kỳ tuyển sinh đầu vào'}})
            MERGE (r2_8:Article {{name: 'điều 8: khen thưởng đối với sinh viên tốt nghiệp'}})
            MERGE (r3:Part {{name: 'chương 3: kỷ luật'}})
            MERGE (r3_11:Article {{name: 'điều 11: hình thức kỷ luật và nội dung vi phạm'}})
            MERGE (r3_12:Article {{name: 'điều 12: trình tự, thủ tục và hồ sơ xét kỷ luật'}})
            MERGE (r3_13:Article {{name: 'điều 13: chấm dứt hiệu lực của quyết định kỷ luật'}})
            MERGE (r3_0:Article {{name: 'một số nội dung vi phạm và khung xử lý kỷ luật sinh viên'}})

            MERGE (s:Section {{name: 'quy chế đánh giá kết quả rèn luyện'}})
            MERGE (s0_3:Article {{name: 'điều 3: nội dung đánh giá và thang điểm'}})
            MERGE (s0_4:Article {{name: 'điều 4: đánh giá về ý thức tham gia học tập'}})
            MERGE (s0_5:Article {{name: 'điều 5: đánh giá về ý thức chấp hành nội quy, quy chế, quy định trong cơ sở giáo dục đại học'}})
            MERGE (s0_6:Article {{name: 'điều 6: đánh giá về ý thức tham gia các hoạt động chính trị, xã hội, văn hóa, nghệ thuật, thể thao, phòng chống tội phạm và các tệ nạn xã hội'}})
            MERGE (s0_7:Article {{name: 'điều 7: đánh giá về ý thức công dân trong quản hệ cộng đồng'}})
            MERGE (s0_8:Article {{name: 'điều 8: Đánh giá về ý thức và kết quả khi tham gia công tác cán bộ lớp, các đoàn thể, tổ chức trong cơ sở giáo dục đại học hoặc người học đạt được thành tích đặc biệt trong học tập, rèn luyện'}})
            MERGE (s0_9:Article {{name: 'điều 9: phân loại kết quả rèn luyện'}})
            MERGE (s0_10:Article {{name: 'điều 10: phân loại để đánh giá'}})
            MERGE (s0_11:Article {{name: 'điều 11: quy trình đánh giá kết quả rèn luyện'}})

            MERGE (t:Section {{name: 'quy tắc ứng xử văn hóa của người học'}})
            MERGE (t0_4:Article {{name: 'điều 4: ứng xử với công tác học tập, nghiên cứu khoa học, rèn luyện'}})
            MERGE (t0_5:Article {{name: 'điều 5: ứng xử đối với giảng viên và nhân viên nhà trường'}})
            MERGE (t0_6:Article {{name: 'điều 6: ứng xử với bạn bè'}})
            MERGE (t0_7:Article {{name: 'điều 7: ứng xử với cảnh quan môi trường và tài sản công'}})

            MERGE (u:Section {{name: 'cố vấn học tập'}})
            MERGE (v:Section {{name: 'danh hiệu sinh viên 5 tốt'}})
            MERGE (v0_1:Article {{name: 'đạo đức tốt'}})
            MERGE (v0_2:Article {{name: 'học tập tốt'}})
            MERGE (v0_3:Article {{name: 'thể lực tốt'}})
            MERGE (v0_4:Article {{name: 'tình nguyện tốt'}})
            MERGE (v0_5:Article {{name: 'hội nhập tốt'}})
            MERGE (v0_6:Article {{name: 'khái niệm'}})

            MERGE (v1:Part {{name: 'ngoài ra ưu tiên xét chọn những sinh viên đạt ít nhất 01 trong các các tiêu chuẩn sau'}})
            MERGE (v1_1:Article {{name: 'ưu tiên 1'}})
            MERGE (v1_2:Article {{name: 'ưu tiên 2'}})
            MERGE (v1_3:Article {{name: 'ưu tiên 3'}})
            MERGE (v1_4:Article {{name: 'ưu tiên 4'}})
            MERGE (v1_5:Article {{name: 'ưu tiên 5'}})
            MERGE (v1_6:Article {{name: 'ưu tiên 6'}})

            MERGE (w:Section {{name: 'danh hiệu sinh viên tiêu biểu'}})

            MERGE (n)-[:BAO_GỒM]->(o)
            MERGE (o)-[:BAO_GỒM]->(o2)
            MERGE (o2)-[:BAO_GỒM]->(o2_4)
            MERGE (o2)-[:BAO_GỒM]->(o2_5)
            MERGE (o2)-[:BAO_GỒM]->(o2_6)

            MERGE (n)-[:BAO_GỒM]->(p)
            MERGE (p)-[:BAO_GỒM]->(p2)
            MERGE (p2)-[:BAO_GỒM]->(p2_9)
            MERGE (p2)-[:BAO_GỒM]->(p2_10)
            MERGE (p)-[:BAO_GỒM]->(p3)
            MERGE (p3)-[:BAO_GỒM]->(p3_12)
            MERGE (p3)-[:BAO_GỒM]->(p3_13)
            MERGE (p3)-[:BAO_GỒM]->(p3_14)
            MERGE (p3)-[:BAO_GỒM]->(p3_15)
            MERGE (p3)-[:BAO_GỒM]->(p3_16)
            MERGE (p3)-[:BAO_GỒM]->(p3_17)
            MERGE (p3)-[:BAO_GỒM]->(p3_18)
            MERGE (p3)-[:BAO_GỒM]->(p3_19)
            MERGE (p3)-[:BAO_GỒM]->(p3_20)
            MERGE (p)-[:BAO_GỒM]->(p4)
            MERGE (p4)-[:BAO_GỒM]->(p4_21)
            MERGE (p4)-[:BAO_GỒM]->(p4_24)

            MERGE (n)-[:BAO_GỒM]->(q)
            MERGE (q)-[:BAO_GỒM]->(q0_3)
            MERGE (q)-[:BAO_GỒM]->(q0_9)
            MERGE (q)-[:BAO_GỒM]->(q0_13)

            MERGE (n)-[:BAO_GỒM]->(r)
            MERGE (r)-[:BAO_GỒM]->(r2)
            MERGE (r2)-[:BAO_GỒM]->(r2_4)
            MERGE (r2)-[:BAO_GỒM]->(r2_5)
            MERGE (r2)-[:BAO_GỒM]->(r2_6)
            MERGE (r2)-[:BAO_GỒM]->(r2_7)
            MERGE (r2)-[:BAO_GỒM]->(r2_8)
            MERGE (r)-[:BAO_GỒM]->(r3)
            MERGE (r3)-[:BAO_GỒM]->(r3_11)
            MERGE (r3)-[:BAO_GỒM]->(r3_12)
            MERGE (r3)-[:BAO_GỒM]->(r3_13)
            MERGE (r3)-[:BAO_GỒM]->(r3_0)

            MERGE (n)-[:BAO_GỒM]->(s)
            MERGE (s)-[:BAO_GỒM]->(s0_3)
            MERGE (s)-[:BAO_GỒM]->(s0_4)
            MERGE (s)-[:BAO_GỒM]->(s0_5)
            MERGE (s)-[:BAO_GỒM]->(s0_6)
            MERGE (s)-[:BAO_GỒM]->(s0_7)
            MERGE (s)-[:BAO_GỒM]->(s0_8)
            MERGE (s)-[:BAO_GỒM]->(s0_9)
            MERGE (s)-[:BAO_GỒM]->(s0_10)
            MERGE (s)-[:BAO_GỒM]->(s0_11)

            MERGE (n)-[:BAO_GỒM]->(t)
            MERGE (t)-[:BAO_GỒM]->(t0_4)
            MERGE (t)-[:BAO_GỒM]->(t0_5)
            MERGE (t)-[:BAO_GỒM]->(t0_6)
            MERGE (t)-[:BAO_GỒM]->(t0_7)

            MERGE (n)-[:BAO_GỒM]->(u)
            MERGE (n)-[:BAO_GỒM]->(v)
            MERGE (v)-[:BAO_GỒM]->(v0_1)
            MERGE (v)-[:BAO_GỒM]->(v0_2)
            MERGE (v)-[:BAO_GỒM]->(v0_3)
            MERGE (v)-[:BAO_GỒM]->(v0_4)
            MERGE (v)-[:BAO_GỒM]->(v0_5)
            MERGE (v)-[:BAO_GỒM]->(v0_6)
            MERGE (v)-[:BAO_GỒM]->(v1)
            MERGE (v1)-[:BAO_GỒM]->(v1_1)
            MERGE (v1)-[:BAO_GỒM]->(v1_2)
            MERGE (v1)-[:BAO_GỒM]->(v1_3)
            MERGE (v1)-[:BAO_GỒM]->(v1_4)
            MERGE (v1)-[:BAO_GỒM]->(v1_5)
            MERGE (v1)-[:BAO_GỒM]->(v1_6)

            MERGE (n)-[:BAO_GỒM]->(w)
            MERGE (x:Part {{name: 'hỗ trợ và dịch vụ'}})
            MERGE (y:Section {{name: 'quy định phân cấp giải quyết thắc mắc của sinh viên'}})
            MERGE (y0_2:Article {{name: 'điều 2: hình thức thắc mắc, kiến nghị'}})
            MERGE (y0_3:Article {{name: 'điều 3: các bước gửi thắc mắc, kiên nghị'}})
            MERGE (y0_4:Article {{name: 'điều 4: những vấn đề trao đổi trực tiếp hoặc gửi thư qua email'}})
            MERGE (y0_5:Article {{name: 'điều 5: trách nhiệm của giảng viên và các bộ phận chức năng'}})
            MERGE (y0_6:Article {{name: 'điều 6: những vấn đề đã trao đổi trực tiêp hoặc gửi thư không được giải quyết thoải đáng'}})
            MERGE (y0_7:Article {{name: 'điều 7: những vấn đề liên quan đến tổ chức lớp học phần'}})
            MERGE (y0_8:Article {{name: 'điều 8: những vấn đề liên quan đến điểm bộ phận, điểm thi kết thúc học phần, điểm thi học phần và tổ chức thi'}})
            MERGE (y0_9:Article {{name: 'điều 9; chuyển thắc mắc, kiến nghị của sinh viên'}})
            MERGE (y0_10:Article {{name: 'điều 10: những nội dung được nói trực tuyến trên website'}})
            MERGE (y0_11:Article {{name: 'điều 11: yêu cầu đối với sinh viên tham gia trực tuyến'}})

            MERGE (z:Section {{name: 'thông tin học bổng tài trợ'}})
            MERGE (aa:Section {{name: 'vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'}})
            MERGE (aa0_1:Article {{name: 'đối tượng sinh viên được hỗ trợ vay tiền'}})
            MERGE (aa0_2:Article {{name: 'điều kiện để được hỗ trợ vay tiền sinh viên'}})
            MERGE (aa0_3:Article {{name: 'mức tiền và lãi suất hỗ trợ vay tiền sinh viên'}})
            MERGE (aa0_4:Article {{name: 'phương thức cho vay tiền sinh viên'}})
            MERGE (aa0_5:Article {{name: 'thông tin về vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'}})

            MERGE (bb:Section {{name: 'quy trình xác nhận hồ sơ sinh viên'}})
            MERGE (bb0_1:Article {{name: 'các loại giấy tờ được xác nhận'}})
            MERGE (bb0_2:Article {{name: 'kênh đăng ký'}})
            MERGE (bb0_3:Article {{name: 'đăng ký'}})
            MERGE (bb0_4:Article {{name: 'quy trình'}})

            MERGE (cc:Section {{name: 'hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên'}})
            MERGE (dd:Section {{name: 'thông tin về bảo hiểm y tế'}})

            MERGE (ee:Section {{name: 'hướng dẫn sử dụng các kênh thanh toán học phí, bhyt, lệ phí xét tốt nghiệp'}})
            MERGE (ee0_1:Article {{name: 'thanh toán tại quầy giao dịch của bidv'}})
            MERGE (ee0_2:Article {{name: 'thanh toán qua kênh bidv smart banking'}})
            MERGE (ee0_3:Article {{name: 'thanh toán qua kênh bidv online'}})
            MERGE (ee0_4:Article {{name: 'thanh toán qua atm của bidv'}})
            MERGE (ee0_5:Article {{name: 'thanh toán qua website sinh viên'}})
            MERGE (ee0_6:Article {{name: 'hướng dẫn cài đặt sinh trắc học'}})

            MERGE (ff:Section {{name: 'tham vấn tâm lý học đường'}})
            MERGE (gg:Section {{name: 'trung tâm dịch vụ sinh viên'}})

            MERGE (mm:Section {{name: 'thông tin học bổng khuyến khích học tập'}})
            MERGE (mm0_1:Article {{name: 'đối tượng'}})
            MERGE (mm0_2:Article {{name: 'quỹ học bổng khuyến khích học tập'}})
            MERGE (mm0_3:Article {{name: 'căn cứ để xét học bổng khuyến khích học tập'}})
            MERGE (mm0_4:Article {{name: 'mức học bổng khuyến khích học tập'}})
            MERGE (mm0_5:Article {{name: 'quy trình xét học bổng'}})

            MERGE (x)-[:BAO_GỒM]->(y)
            MERGE (y)-[:BAO_GỒM]->(y0_2)
            MERGE (y)-[:BAO_GỒM]->(y0_3)
            MERGE (y)-[:BAO_GỒM]->(y0_4)
            MERGE (y)-[:BAO_GỒM]->(y0_5)
            MERGE (y)-[:BAO_GỒM]->(y0_6)
            MERGE (y)-[:BAO_GỒM]->(y0_7)
            MERGE (y)-[:BAO_GỒM]->(y0_8)
            MERGE (y)-[:BAO_GỒM]->(y0_9)
            MERGE (y)-[:BAO_GỒM]->(y0_10)
            MERGE (y)-[:BAO_GỒM]->(y0_11)

            MERGE (x)-[:BAO_GỒM]->(z)
            MERGE (x)-[:BAO_GỒM]->(aa)
            MERGE (aa)-[:BAO_GỒM]->(aa0_1)
            MERGE (aa)-[:BAO_GỒM]->(aa0_2)
            MERGE (aa)-[:BAO_GỒM]->(aa0_3)
            MERGE (aa)-[:BAO_GỒM]->(aa0_4)
            MERGE (aa)-[:BAO_GỒM]->(aa0_5)

            MERGE (x)-[:BAO_GỒM]->(bb)
            MERGE (bb)-[:BAO_GỒM]->(bb0_1)
            MERGE (bb)-[:BAO_GỒM]->(bb0_2)
            MERGE (bb)-[:BAO_GỒM]->(bb0_3)
            MERGE (bb)-[:BAO_GỒM]->(bb0_4)

            MERGE (x)-[:BAO_GỒM]->(cc)
            MERGE (x)-[:BAO_GỒM]->(dd)
            MERGE (x)-[:BAO_GỒM]->(ee)
            MERGE (ee)-[:BAO_GỒM]->(ee0_1)
            MERGE (ee)-[:BAO_GỒM]->(ee0_2)
            MERGE (ee)-[:BAO_GỒM]->(ee0_3)
            MERGE (ee)-[:BAO_GỒM]->(ee0_4)
            MERGE (ee)-[:BAO_GỒM]->(ee0_5)
            MERGE (ee)-[:BAO_GỒM]->(ee0_6)

            MERGE (x)-[:BAO_GỒM]->(ff)
            MERGE (x)-[:BAO_GỒM]->(gg)
            MERGE (x)-[:BAO_GỒM]->(mm)
            MERGE (mm)-[:BAO_GỒM]->(mm0_1)
            MERGE (mm)-[:BAO_GỒM]->(mm0_2)
            MERGE (mm)-[:BAO_GỒM]->(mm0_3)
            MERGE (mm)-[:BAO_GỒM]->(mm0_4)
            MERGE (mm)-[:BAO_GỒM]->(mm0_5)

DỮ LIỆU NỘI DUNG (retrieved context):
Ví dụ 1:
Câu hỏi: Trường Đại học Nông Lâm Thành phố Hồ Chí Minh có diện tích bao nhiêu
Trả lời: 
{{
    "part": "Section",
    "name": "quá trình hình thành và phát triển",
    "level": 2
}}

Ví dụ 2:
Câu hỏi: Khoa nào phụ trách ngành Công nghệ kỹ thuật năng lượng tái tạo?
Trả lời: 
{{
    "part": "Section",
    "name": "các khoa - ngành đào tạo",
    "level": 2
}}

Ví dụ 3:
Câu hỏi: lễ tuyên dương tuyên_dương sinh viên có thành tích
Trả lời: 
{{
    "part": "Part",
    "name": "chương 2: khen thưởng",
    "level": 2
}}

Ví dụ 4:
Câu hỏi: Hoạt động chính của CLB Nông Lâm Radio tại Đại học Nông Lâm TP.HCM là gì?
Trả lời: 
{{
    "part": "Section",
    "name": "câu lạc bộ (clb) - đội, nhóm",
    "level": 2
}}

Ví dụ 5:
Câu hỏi: ý thức chấp hành nội quy được_đánh_giá_bằng điểm rèn luyện có_khung_điểm_tối_đa 100 điểm
Trả lời: 
{{
    "part": "Article",
    "name": "điều 5: đánh giá về ý thức chấp hành nội quy, quy chế, quy định trong cơ sở giáo dục đại học",
    "level": 2
}}

Ví dụ 6:
Câu hỏi: Hãy nói cho tôi biết phần 1 nói về những gì
Trả lời: 
{{
    "part": "Part",
    "name": "nlu - định hướng trường đại học nghiên cứu",
    "level": 3
}}

ĐẦU RA:
1. trả về theo format json sau:
{{
    "part": <nhãn của tiêu đề>,
    "name": <tên tiêu đề>,
    "level": <độ sâu có thể dựa vào chi tiết hoặc tổng quan, có thể tối đa là 3>
}}
2. Trả lời câu hỏi chính xác và ngắn gọn.
3. không cần giải thích gì thêm
4. BẮT BUỘC PHẢI CHỌN ĐƯỢC PART và NAME, KHÔNG CÓ CHUYỆN KHÔNG CÓ THÔNG TIN

### Câu hỏi: {question}
"""

def predict_question_belong_to():
    return """
    Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Nhiệm vụ của bạn:
    Đầu tiên, cần dự đoán câu hỏi sau nằm trong phần nào trong mục lục mà tôi cung cấp:

    Mục lục: 
    {parts_of_document}

1. trả về theo format json sau:
{{
    "name": <tên tiêu đề>,
    "level": <độ sâu có thể dựa vào chi tiết hoặc tổng quan, có thể tối đa là 3>
}}
2. Trả lời câu hỏi chính xác và ngắn gọn.
3. không cần giải thích gì thêm
4. BẮT BUỘC PHẢI CHỌN ĐƯỢC PART và NAME, KHÔNG CÓ CHUYỆN KHÔNG CÓ THÔNG TIN

### Câu hỏi: {question}
"""

# dùng để trích xuất entities và relationship cho câu hỏi
def extract_entities_relationship_from_question():
    return """Bạn là một hệ thống trích xuất thông tin từ văn bản. Nhiệm vụ của bạn là:
1. Trích xuất tất cả các thực thể có trong đoạn văn bản.
   - Mỗi thực thể cần có tên(name) và loại(type).
   - Loại(type) hãy sử dụng các từ mà tôi cung cấp dưới đây:
   "episode, part, organization, quantity, department, phone_number, website, center, institute, faculty, training_program, person, email, location, facility, activity, type_of_organization, concept, document, year, strategy, time, award, group_of_people, group, title, event, position, disciplinary_action, movement, abbreviation, percentage, beverage, item, network, frequency, action, material, code, device, system, status, clause, chapter, document_type, software, sequence, media, variable, natural_phenomenon, service, crime, grade, data, course_type, degree, assignment, criteria, subject, money, field, right, teaching_method, platform, account, image, feature"
2. Xác định các mối quan hệ(relaion) giữa các thực thể.
    - Mỗi mối quan hệ phải có nguồn(source), tên mối quan hệ(relation) và loại của nguồn(type_source)(lấy từ entities).
    - PHẢI sử dụng các mối quan hệ có sẵn dưới đây, nếu câu hỏi không có sẵn quan hệ bên dưới hãy tìm từ đồng nghĩa, KHÔNG ĐƯỢC LẤY LẠI MỐI QUAN HỆ Ở CÂU HỎI:
    "website, có, là, tôn_trọng, theo, hủy, in, dưới, bị, mời, đối_với, của, gửi, không, gồm, trong, từ, email, công_bố, BAO_GỒM, sở_hữu, số_điện_thoại, thuộc_khoa, chương_trình_tiên_tiến_tại, chương_trình_nâng_cao_tại, chương_trình_đào_tạo_tại, quản_lý_bởi, chủ_nhiệm, trưởng_ban_điều_hành, đội_trưởng, số_lượng_sách, sử_dụng, số_lượng_phòng, sức_chứa, bao_gồm, về, sánh_vai, trên, đổi_mới, thúc_đẩy, phát_huy, xây_dựng, trở_thành, hàng_đầu, đáp_ứng, tầm_nhìn, tên_khác, trực_thuộc, tọa_lạc_tại, thuộc, thời_gian_hoạt_động, nhận_giải_thưởng, thành_lập, phục_vụ, đào_tạo, và, mục_tiêu_đến, sẽ_trở_thành, với, tổ_chức_bởi, được_đăng_tại, gìn_giữ_và_phát_huy, phát_hiện, nâng_đỡ, cho, đề_cao, hoạt_động_của, dành_cho, hỗ_trợ, tư_vấn, phù_hợp, hướng_dẫn, đăng_ký, ở, điều_chỉnh, xác_nhận, theo_dõi, cập_nhật_trên, không_dưới, ít_nhất, xem_xét, cấp, tham_gia, trường, tổ_chức, vào_cuối, tuyên_dương, khen_thưởng, căn_cứ, đánh_giá, phòng_chống, đạt, thang_điểm, chấp_hành, đến, không_vượt_quá, đánh_giá_qua, đoạt_giải, có_thành_tích, đóng_góp, hoạt_động_tại, thực_hiện, bảo_đảm_an_ninh, ít_hơn_hoặc_bằng, chọn, cao_nhất, cao_thứ_hai, bằng_nhau, công_nhận, xét, áp_dụng_bởi, thông_báo, gửi_thông_báo, làm, tham_dự, sau, chấm_dứt, trừ, vô_lễ, lần_1, giao_cho, hạ_điểm, tài_sản_trong, làm_hư_hỏng, lần_2, lần_3, trái, xâm_phạm, chống_phá, thu_hồi, lắng_nghe, hoàn_thành, nghiêm_túc, phát_động, hỏi, trả_lời, làm_phiền, quan_hệ, không_gây_ồn_ào, giữ_gìn, cung_cấp, nhận, dấu_và_chữ_ký, truy_cập, nhập, thanh_toán, hiển_thị, lưu, tại, tương_ứng, phản_hồi, đăng_nhập, chụp_ảnh, quét, đọc, lấy_ảnh, kiểm_tra, trạng_thái, chuyển_tới, viết, trực_tuyến, không_chấp_nhận, nộp, trao_đổi, thắc_mắc, đề_nghị, mang, được_hỗ_trợ, đi_học, chưa_được_sửa, mất, giúp_đỡ, nêu, hoặc, ghi, chuyển, ký, đã, kèm, giải_quyết, loại, bổ_sung, cập_nhật, trình_ký, đóng_dấu, hoạt_động, liên_hệ, như, cùng, xếp, so_sánh, không_cần, bằng, bố_trí, trọng_số, không_bị, quyết_định, cao_hơn, hơn, lập, trình, làm_tròn, trích_từ, do, phối_hợp, trị_giá, một_lần, qua, mỗi, đóng_mộc, sửa_đổi, mã, nhân, tra_cứu, quản_lý, điện_thoại, thành_lập_từ, vay, để, giúp, thủ_tục, gặp_khó_khăn, cư_trú, sinh_sống, đủ_tiêu_chuẩn, tối_đa, lãi_suất, thông_qua, trả_nợ, đóng_trụ_sở, tuân_thủ_quy_định_của, học_tập_tại, được_tôn_trọng_bởi, được_cung_cấp, được_sử_dụng, hoạt_động_trong, kiến_nghị_với, đề_đạt_nguyện_vọng_lên, được_ở, được_nhận, tuân_thủ_chủ_trương_của, tuân_thủ_pháp_luật_của, tuân_thủ_quy_chế_của, đóng, không_được_xúc_phạm, không_được_tham_gia, không_được, không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép, cung_cấp_ctđt_cho, tư_vấn_xây_dựng_khht_cho, thông_báo_học_phần_cho, hướng_dẫn_đăng_ký_cho, thực_hiện_theo, đăng_ký_học_lại, cải_thiện_điểm, cho_phép_đăng_ký_ít_hơn_14_tín_chỉ, rút, không_đi_học, không_dự_thi, nhận_điểm_r, nhận_điểm_f, rút_học_phần_trên, đề_xuất_hủy_hoặc_mở_thêm, đăng_ký_trực_tuyến, công_bố_kết_quả_đăng_ký_cho, cải_thiện_kết_quả, đề_xuất, duy_trì, phê_duyệt_duy_trì, đề_xuất_mở_thêm, chấp_thuận_mở_thêm, mở_thêm, dự_thi, đề_xuất_cấm_thi, duyệt_danh_sách_cấm_thi, tối_thiểu, chuẩn, được_quy_định_trong, thông_báo_cho, thông_báo_lịch_thi, hưởng, chấp_thuận, duyệt_đơn, tổ_chức_thi_cho, xét_tương_đương, quy_định, rà_soát, phê_duyệt, xác_định, đồng_ý, không_đạt, tính_vào, xử_lý, xem_kết_quả, được_đánh_giá, tính, không_tính, dựa_vào, trung_bình_cộng, kỷ_luật, không_tham_gia, xếp_loại, lưu_trong, ghi_vào, đình_chỉ, tiêu_chí, cho_phép, chuyển_sang, cấp_bằng, chấm, thỏa_mản, phân_công, tổ_chức_bảo_vệ, thảo_luận, gia_hạn, quyết_định_gia_hạn, không_hoàn_thành, tích_lũy, ra_quyết_định, được_cấp, báo, bảo_lưu, được_điều_động, cần, theo_quy_định, học_xong, nghỉ, được_công_nhận, học, vượt_quá, nghiên_cứu, bổ_sung_vào, tăng_cường, áp_dụng, chỉ_đạo, phát_triển_trên, không_tổ_chức, giữ_bí_mật, bảo_vệ, chịu_trách_nhiệm, trước, nhấn, mở, tắt, bấm, chia_sẻ"
    - Tên mối quan hệ phải được ghi thường. Nếu tên mối quan hệ gồm từ hai từ trở lên, các từ phải được nối với nhau bằng dấu gạch dưới (ví dụ: "không_tính", "thông_báo_lịch_thi").

3. Trả về kết quả dưới dạng JSON với các trường:
   - "entities": Danh sách các thực thể. Mỗi thực thể có các thuộc tính "name" và "type".
   - "relationships": Danh sách các mối quan hệ: . Mỗi mối quan hệ có các thuộc tính "source", "relation" và "type_source"(lấy từ entities).

Đoạn văn bản cần trích xuất:
{question}

Yêu cầu:
- Trả về kết quả dưới dạng JSON với các trường: entities, relationships.
- Mỗi entity cần có name và type.
- Mỗi relationship cần có source, relation và "type_source"(lấy từ entities).

---
### Giải thích:
1. **Entity**:
   - Là các đối tượng được nhắc đến trong văn bản, ví dụ: tên người, địa điểm, tổ chức, ngày tháng, v.v.
   - Mỗi entity cần được gán một loại phù hợp, ví dụ: NGƯỜI, ĐỊA ĐIỂM, TỔ CHỨC, NGÀY, v.v.

2. **Relationship**:
   - Là mối quan hệ giữa các entity, nhưng không trích xuất target

3. **Định dạng đầu ra**:
   - Sử dụng JSON để trả về kết quả một cách có cấu trúc, dễ dàng xử lý tiếp theo."""


def extract_text_from_paragraph(paragraph):
    return f"""
    Bạn là một trợ lý AI chuyên xử lý văn bản tự nhiên. Tôi có một văn bản lớn và muốn bạn giúp tôi trích xuất các đoạn văn nhỏ từ văn bản đó để lưu vào vectordatabase. Hãy thực hiện theo các yêu cầu sau:

1. Chia văn bản thành các đoạn nhỏ, mỗi đoạn có độ dài từ 100 đến 200 từ (hoặc khoảng 2-4 câu, tùy vào ngữ cảnh), nhưng không được cắt giữa chừng làm mất nghĩa của câu hoặc ý chính.

2. Đảm bảo mỗi đoạn nhỏ giữ được ý nghĩa độc lập hoặc liên quan chặt chẽ đến ngữ cảnh của văn bản gốc, không bị rời rạc.

3. Các đoạn văn nhỏ phải liền mạch với nhau, nghĩa là nội dung của đoạn sau phải có sự kết nối tự nhiên với đoạn trước, giống như trong văn bản gốc.

4. Trả về kết quả dưới dạng json có thuộc tính text lưu trữ từng đoạn văn.

5. Nếu có câu hoặc ý nào quá dài, hãy điều chỉnh để đoạn văn vẫn nằm trong khoảng độ dài mong muốn mà không làm mất ý nghĩa.

6. BẮT BUỘC TRÍCH XUẤT ĐÀY ĐỦ NỘI DUNG CỦA VĂN BẢN, KHÔNG ĐƯỢC CHỈNH SỬA NỘI DUNG NHƯ THÊM HOẶC BỚT, KHÔNG ĐƯỢC ĐÍNH KÈM CÁC TỪ CHUNG CHUNG NHƯ "các liên kết dưới đây" hoặc "các thông tin sau"nếu như từ đó không có trong văn bản.
7. có thể thêm các từ để bổ sung ý nghĩa cho 1 câu như "khu vực A có email kva@gmai..com", "Khư vực B có số điện thoại 0901231212"
Dưới đây là văn bản lớn mà tôi cung cấp:
{paragraph}"""


def answer_by_context():
    return """
hãy dựa vào ngữ cảnh của các câu trả lời trước để trả lời câu hỏi {question}. Nếu không có ngữ cảnh để trả lời thì phản hổi 'Không có thông tin' và không giải thích gì thêm.
"""

def chunking():
    return """
Bạn là một trợ lý AI chuyên xử lý văn bản tự nhiên. Nhiệm vụ của bạn là giúp tôi trích xuất các đoạn văn nhỏ từ văn bản lớn. Tôi sẽ đưa vào một văn bản lớn. Hãy thực hiện theo các yêu cầu sau:
Văn bản tôi truyền vào có thể là một bài viết khoa học về một chủ đề chuyên môn về bất kỳ lĩnh vực nào. MỌI ĐOẠN VĂN BẢN ĐỀU PHẢI TRÍCH XUẤT, KHÔNG THAN PHIỀN, KHÔNG GIẢI THÍCH, KHÔNG MỞ ĐẦU, KHÔNG KẾT THÚC, CHỈ LÀM THEO SỰ HƯỚNG DẪN
1. Không được cắt giữa chừng làm mất nghĩa của câu hoặc ý chính.
2. Đảm bảo mỗi đoạn nhỏ giữ được ý nghĩa độc lập và liên quan chặt chẽ đến ngữ cảnh, không bị rời rạc, không thay đổi, chỉnh sửa hoặc thiếu của văn bản gốc.
3. Các đoạn văn nhỏ phải liền mạch với nhau, nghĩa là nội dung của đoạn sau phải có sự kết nối tự nhiên với đoạn trước, giống như trong văn bản gốc.
4. Mỗi đoạn phải có ít nhất 2 câu và nhiều nhất là 4 câu. 
5. Trả về kết quả dưới dạng json như sau:
{
"đoạn 1": "",
"đoạn 2": "",
"đoạn 3": "",
"đoạn 4": "",
....
}
6. Phải trích xuất từ đầu đến cuối, một cách liên tục và liền mạch mà không bỏ lỡ bất kỳ từ gì
7. Chỉ trích xuất những nội dung có ý nghĩa và nội dung. Bỏ các nội dung của header, footer, phần, chương, 1., 2., 3., a., b., c., mục lục,...
8. Json phải sử dụng ký tự "" không được dùng ''
9. HÃY NHỚ MỞ NGOẶC VÀ ĐÓNG NGOẶC ĐỀ ĐÚNG FORMAT CỦA JSON
10. KHÔNG GIẢI THÍCH GÌ THÊM, KHÔNG MỞ ĐẦU, KẾT THÚC
11. NỘI DUNG CỦA TỪNG ĐOẠN KHÔNG CHỨA CHUỖI LỒNG CHUỖI VÍ DỤ NHƯ "xin chào, tôi tên là h"hoang" MÀ ĐÚNG LÀ "xin chào, tôi tên là h hoang"
Hãy trích xuất các đoạn văn nhỏ theo yêu cầu trên và trả lời bằng tiếng Việt. Chỉ trả về theo dạng json và không giải thích gì thêm, không mở đầu, không kết thúc"""


def summary_answer():
    return """
Bạn được cung cấp:
Một câu hỏi tổng hợp có thể bao gồm nhiều điều kiện.
Một danh sách các câu trả lời theo từng bước, mỗi câu chỉ trả lời một phần của câu hỏi ban đầu.
Mỗi câu trả lời có thể chứa một hoặc nhiều thực thể (ví dụ: nhiều câu lạc bộ, nhiều người).

Nhiệm vụ của bạn:
Các câu trả lời sẽ được cung cấp theo nhiều bước. Bạn cần chọn ra những bước có chứa thông tin liên quan và chỉ đưa ra câu trả lời tổng hợp cuối cùng thỏa mãn tất cả các điều kiện nêu trong câu hỏi ban đầu. Không đưa ra bất kỳ giải thích hoặc lập luận nào. 

Ví dụ:
Câu hỏi: "Câu lạc bộ nào hoạt động trong lĩnh vực truyền thông và động vật hoang dã và do Lê Tường Vi lãnh đạo?"
Các câu trả lời theo từng bước:
Câu lạc bộ hoạt động trong lĩnh vực truyền thông và động vật hoang dã là *wildlife vet student club*.
Câu lạc bộ do Lê Tường Vi lãnh đạo là *wildlife vet student club*.
  Kết quả mong đợi:
Câu lạc bộ hoạt động trong lĩnh vực truyền thông và động vật hoang dã và do Lê Tường Vi lãnh đạo là wildlife vet student club.

Yêu cầu:
1. Sử dụng ngôn ngữ tự nhiên.
2. Nếu có nhiều mục, hãy liệt kê theo thứ tự và in đậm các thuật ngữ chính.
3. Nếu tài liệu không có thông tin bạn có thể sử dụng kiến thức của mình để có thể bổ sung thêm thông tin cho câu trả lời phong phú hơn(nếu có câu trả lời) hoặc có thể trả lời(nếu không có tài liệu tham khảo nào). Câu trả lời phải ghi đúng chính tả và tự nhiên theo tiếng việt
4. Bỏ đi các chữ bạn cho là dư thừa
5. Phản hồi bằng tiếng việt theo cách tự nhiên nhất có chủ ngữ vị ngữ đầy đủ và không giải thích thêm.
Câu hỏi: {question}
Câu trả lời: {answer}
"""


# tạo ra tiêu đề cho neo4j khi thêm tài liệu mới
def create_title():
    return """
Bạn là một chuyên gia ngôn ngữ. Dưới đây là một đoạn văn bản dài. Hãy thực hiện các bước sau:
Nếu trong đoạn văn bản có tiêu đề rõ ràng (ví dụ nằm ở đầu đoạn hoặc được phân biệt rõ ràng), hãy trích xuất tiêu đề đó.
Nếu không có tiêu đề rõ ràng, hãy đọc và tóm tắt nội dung đoạn văn để tạo ra một tiêu đề phù hợp, ngắn gọn, chính xác và bao quát nội dung chính.
Đầu ra: 
{
    "title": "<title>"
}
"""

def first_decision_prime():
    return """
You are a helpful, pattern-following assistant. Given the following question, extract the information from the question as requested. Rules: 1. The Relational information must come from
the given relational types. 2. Each entity must exactly have one category in the parentheses.
Given the following question, based on the entity type and the relation type, extract the
topic entities and useful relations from the question. 

Examples for entity and relation extraction:
Câu hỏi 1: Could you identify any skin diseases associated with epithelial skin neoplasms? I've observed a tiny, yellowish lesion on sun-exposed areas of my face and neck, and I suspect it might be connected.
{{
  "relationship": [
    {{
      "head": "epithelial skin neoplasm",
      "head_type": "disease"
    }},
    {{
      "head": "yellowish lesion",
      "head_type": "effect_phenotype"
    }},
    {{
      "head": "sun-exposed area",
      "head_type": "anatomy"
    }}
  ],
  "action": "knowledge graph"
}}

Câu hỏi 2: What drugs target the CYP3A4 enzyme and are used to treat strongyloidiasis?
{{
  "relationship": [
    {{
      "head": "CYP3A4",
      "head_type": "gene_protein"
    }},
    {{
      "head": "strongyloidiasis",
      "head_type": "disease"
    }}
  ],
  "action": "knowledge graph"
}}


Câu hỏi 3: What is the name of the condition characterized by a complete interruption of the inferior vena cava, falling under congenital vena cava anomalies?
{{
  "relationship": [
    {{
      "head": "inferior vena cava interruption",
      "head_type": "disease"
    }},
    {{
      "head": "congenital vena cava anomaly",
      "head_type": "disease"
    }}
  ],
  "action": "text document"
}}

Câu hỏi 4: What drugs are used to treat epithelioid sarcoma and also affect the EZH2 gene product?
{{
  "relationship": [
    {{
      "head": "epithelioid sarcoma",
      "head_type": "disease"
    }},
    {{
      "head": "EZH2",
      "head_type": "gene_protein"
    }}
  ],
  "action": "knowledge graph"
}}

Câu hỏi 5: Can you supply a compilation of genes and proteins associated with endothelin B receptor interaction, involved in G alpha (q) signaling, and contributing to hypertension and ovulation-related biological functions?
{{
  "relationship": [
    {{
      "head": "endothelin B receptor",
      "head_type": "gene_protein"
    }},
    {{
      "head": "G alpha (q) signaling",
      "head_type": "pathway"
    }},
    {{
      "head": "hypertension",
      "head_type": "disease"
    }},
    {{
      "head": "ovulation",
      "head_type": "biological_process"
    }}
  ],
  "action": "knowledge graph"
}}

Câu hỏi 6: What is the name of the disease that presents with a congenital blockage of the mitral valve and is categorized as a specific subtype or variation of congenital mitral malformation?
{{
  "relationship": [
    {{
      "head": "congenital mitral valve blockage",
      "head_type": "disease"
    }},
    {{
      "head": "congenital mitral malformation",
      "head_type": "disease"
    }}
  ],
  "action": "text document"
}}

Câu hỏi 7: What is the medical diagnosis for a disorder associated with the FOSB gene, characterized by extreme aggressive episodes and destructive behavior due to poor impulse control, usually beginning after age 6 or during teenage years, with exaggerated verbal and physical reactions to environmental triggers?
{{
  "relationship": [
    {{
      "head": "FOSB",
      "head_type": "gene_protein"
    }},
    {{
      "head": "aggressive behavioral disorder",
      "head_type": "disease"
    }},
    {{
      "head": "impulse control disorder",
      "head_type": "disease"
    }}
  ],
  "action": "text document"
}}


Câu hỏi 8: What condition is linked to KCNJ2 mutations and features episodic paralysis and hypokalemia, often triggered by hyperthyroidism?
{{
  "relationship": [
    {{
      "head": "KCNJ2 mutation",
      "head_type": "gene_protein"
    }},
    {{
      "head": "episodic paralysis",
      "head_type": "disease"
    }},
    {{
      "head": "hypokalemia",
      "head_type": "effect_phenotype"
    }},
    {{
      "head": "hyperthyroidism",
      "head_type": "disease"
    }}
  ],
  "action": "knowledge graph"
}}

Câu hỏi 9: Please find genes and proteins interacting with the peroxisomal membrane and also involved in inhibiting mitochondrial outer membrane permeabilization, relevant to apoptotic signaling.
{{
  "relationship": [
    {{
      "head": "peroxisomal membrane",
      "head_type": "cellular_component"
    }},
    {{
      "head": "mitochondrial outer membrane permeabilization",
      "head_type": "biological_process"
    }},
    {{
      "head": "apoptotic signaling",
      "head_type": "pathway"
    }}
  ],
  "action": "knowledge graph"
}}

Câu hỏi 10: Which gene or protein is engaged in DCC-mediated attractive signaling, can bind to actin filaments, and belongs to the actin-binding LIM protein family?
{{
  "relationship": [
    {{
      "head": "DCC-mediated attractive signaling",
      "head_type": "pathway"
    }},
    {{
      "head": "actin filament",
      "head_type": "cellular_component"
    }},
    {{
      "head": "actin-binding LIM protein family",
      "head_type": "gene_protein"
    }}
  ],
  "action": "knowledge graph"
}}


Entity Type: anatomy, biological_process, cellular_component, disease, drug, effect_phenotype, exposure, gene_protein, molecular_function, pathway
Relation Type:  associated_with, carrier, contraindication, enzyme, expression_absent, expression_present, indication, interacts_with, linked_to, parent-child, ppi, side_effect, synergistic_interaction, target, transporter
Question: <<<{question}>>>

Documents are required to answer the given question, and the goal is to search the useful
documents. Each entity in the knowledge graph is associated with a document. Based on the
extracted entities and relations, is knowledge graph or text documents helpful to narrow down
the search space? 
JSON Structure: 
{{
  "type": "object",
  "properties": {{
    "relationship": {{
      "type": "array",
      "items": {{
        "type": "object",
        "properties": {{
          "head": {{
            "type": "string",
            "description": "Tên của node"
          }},
          "head_type": {{
            "type": "string",
            "description": "Loại của node"
          }}
        }},
        "required": [
          "head",
          "head_type"
        ]
      }}
    }},
    "action": {{
      "type": "string",
      "description": "Hành động cần thực hiện, ví dụ: knowledge graph hoặc text document"
    }}
  }},
  "required": [
    "relationship",
    "action"
  ]
}}

You must answer in the following format:
{{
    "relationship": [
      {{
        "head": "<head_name>",
        "head_type": <label_head>,
      }}
    ],
    "action": <action>
}}
head_name must be in singular form. DON'T EXPLAIN
"""

def self_reflection_prime():
    return """
The retrieved document is incorrect.

Feedback: <<<{feedback}>>>
Question: <<<{question}>>>
Entity name must be in singular form
The retrieved document is incorrect. Answer again based on newly extracted topic entities and useful relations. Is knowledge graph or text documents helpful to narrow down the
search space? You must answer with either of them with no more than two words.
JSON Structure: 
{{
  "type": "object",
  "properties": {{
    "relationship": {{
      "type": "array",
      "items": {{
        "type": "object",
        "properties": {{
          "head": {{
            "type": "string",
            "description": "Tên của node"
          }},
          "head_type": {{
            "type": "string",
            "description": "Loại của node"
          }}
        }},
        "required": [
          "head",
          "head_type"
        ]
      }}
    }},
    "action": {{
      "type": "string",
      "description": "Hành động cần thực hiện, ví dụ: knowledge graph hoặc text document"
    }}
  }},
  "required": [
    "relationship",
    "action"
  ]
}}

You must answer in the following format:
{{
    "relationship": [
      {{
        "head": "<head_name>",
        "head_type": <label_head>,
      }}
    ],
    "action": <action>
}}
head_name must be in singular form. DON'T EXPLAIN
"""

def validator_prime():
    return """
    You are a helpful, pattern-following assistant.
    
### Question: <<<{question}>>>
### Document: <<<{document}>>>
### Answer: <<<{answer}>>>
### Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
"""

def generator_prime():
    return """
Please answer based on the documents I provide:
### Question: <<<{question}>>>
### Document: <<<{document}>>>
Only response focusing on the most relevant documents and those closest in meaning to the question 
Return a complete answer including all the information available in the provided documents.
"""

def commentor_prime():
    return """
You are a helpful, pattern-following assistant.
This is a scientific abstract. Please extract named entities, relations, and keywords without explaining or evaluating the science itself.
Question: <<<{question}>>>
Topic Entities: <<<{entities}>>>
Useful Relations: <<<{relations}>>>
- **Error Source: Input**
  - **Incorrect Entity/Relation**: The entity or relation mentioned is incorrect. Please remove it or replace it with the correct one.
  - **Missing Entity**: There is only one entity, but there might be more. Please extract one additional entity and its relation.
  - **No Intersection**: There is no connection between the entities. Please remove or substitute one entity and its relation.
  - **Incorrect Intersection**: There is a connection between the entities, but the answer is not within it. Please remove or substitute one entity and its relation.

- **Error Source: Selection**
  - **Incorrect Document**: The retrieved document is incorrect. The current retrieval module may not be helpful, and narrowing down the search space could be beneficial.

Please point out the wrong entity or relation extracted from the question, if there is any.
Please respond briefly by pointing out the mistake and giving a suggestion. Do not explain anything further.
If Topic Entities and Useful Relations are not provided, it is highly likely that "Error Source: Selection"
"""

def summary_answer_prime():
    return """
You are given:
A list of step-by-step answers, each addressing only one part of the original question.

Your task:
The answers are provided in multiple steps. You need to select the steps that contain relevant information and provide a final synthesized answer that satisfies **all*the conditions stated in the original question. Do **not*give any explanations or reasoning.

Requirements:
Use natural language.
If there are multiple items, list them in order and bold the key terms.

Question: {question}
Answer: {answer}
Only response focusing on the most relevant documents and those closest in meaning to the question
Please return the name of the object
"""

def first_decision_mag():
    return """
    You are a helpful, pattern-following assistant. Given the following question, extract the information from the question as requested. 
    Rules: 
    1. The Relational information must come from
    the given relational types. 
    2. Each entity must exactly have one category in the parentheses.
    Given the following question, based on the entity type and the relation type, extract the
    topic entities and useful relations from the question. 

    Examples for entity and relation extraction:
    Câu 1: Does any research from the Indian Maritime University touch upon Fe II energy level transitions within the scope of Configuration Interaction?


{{
  "relationship": [
    {{
      "head": "Indian Maritime University",
      "head_type": "institution"
    }},
    {{
      "head": "Fe II energy level transitions",
      "head_type": "field_of_study"
    }},
    {{
      "head": "Configuration Interaction",
      "head_type": "field_of_study"
    }}
  ],
  "action": "knowledge graph"
}}


Câu 2: Show me articles related to magnetic field studies within the Digitized Sky Survey discipline.
{{
  "relationship": [
    {{
      "head": "Digitized Sky Survey",
      "head_type": "field_of_study"
    }},
    {{
      "head": "magnetic field studies",
      "head_type": "field_of_study"
    }}
  ],
  "action": "knowledge graph"
}}


Câu 3: Show me publications by J. Karch that evaluate various imaging techniques in paleontological research.


{{
  "relationship": [
    {{
      "head": "J. Karch",
      "head_type": "author"
    }},
    {{
      "head": "imaging techniques",
      "head_type": "field_of_study"
    }},
    {{
      "head": "paleontological research",
      "head_type": "field_of_study"
    }}
  ],
  "action": "knowledge graph"
}}


Câu 4: What are the papers that reference "The interaction between feedback from active galactic nuclei and supernovae" and also explore the effects of black hole feedback on galaxy groups, similar to the 2010 study on this subject?


{{
  "relationship": [
    {{
      "head": "The interaction between feedback from active galactic nuclei and supernovae",
      "head_type": "paper"
    }},
    {{
      "head": "black hole feedback",
      "head_type": "field_of_study"
    }},
    {{
      "head": "galaxy groups",
      "head_type": "field_of_study"
    }}
  ],
  "action": "knowledge graph"
}}


Câu 5: Looking for papers published in 2014 in the field of Optics, pertinent to process observation in selective laser melting and related to the International Federation of Sport Climbing.


{{
  "relationship": [
    {{
      "head": "Optics",
      "head_type": "field_of_study"
    }},
    {{
      "head": "selective laser melting",
      "head_type": "field_of_study"
    }},
    {{
      "head": "International Federation of Sport Climbing",
      "head_type": "institution"
    }}
  ],
  "action": "knowledge graph"
}}


Câu 6: Are there any published papers from the coauthors of "On the structure of isomeric state in neutron-rich 108Zr: A projected shell model analysis" that delve into high spin states?


{{
  "relationship": [
    {{
      "head": "On the structure of isomeric state in neutron-rich 108Zr: A projected shell model analysis",
      "head_type": "paper"
    }},
    {{
      "head": "high spin states",
      "head_type": "field_of_study"
    }},
    {{
      "head": "projected shell model",
      "head_type": "field_of_study"
    }}
  ],
  "action": "knowledge graph"
}}


Câu 7: Search for publications by Hu Zhiyuan on the impact of radiation on flash memory input/output components.


{{
  "relationship": [
    {{
      "head": "Hu Zhiyuan",
      "head_type": "author"
    }},
    {{
      "head": "radiation impact",
      "head_type": "field_of_study"
    }},
    {{
      "head": "flash memory components",
      "head_type": "field_of_study"
    }}
  ],
  "action": "knowledge graph"
}}


Câu 8: Find publications from Carma researchers that report detections using the Australian Square Kilometre Array Pathfinder (ASKAP) radio telescope.


{{
  "relationship": [
    {{
      "head": "CARMA",
      "head_type": "institution"
    }},
    {{
      "head": "Australian Square Kilometre Array Pathfinder",
      "head_type": "institution"
    }},
    {{
      "head": "radio astronomy",
      "head_type": "field_of_study"
    }}
  ],
  "action": "knowledge graph"
}}


    Entity Type: author, field_of_study, institution, paper
    Relation Type:  author___affiliated_with___institution, author___writes___paper, paper___cites___paper, paper___has_topic___field_of_study
    Question: <<<{question}>>>

    Documents are required to answer the given question, and the goal is to search the useful
    documents. Each entity in the knowledge graph is associated with a document. Based on the
    extracted entities and relations, is knowledge graph or text documents helpful to narrow down
    the search space? 
    JSON Structure: 
    {{
      "type": "object",
      "properties": {{
        "relationship": {{
          "type": "array",
          "items": {{
            "type": "object",
            "properties": {{
              "head": {{
                "type": "string",
                "description": "Tên của node"
              }},
              "head_type": {{
                "type": "string",
                "description": "Loại của node"
              }}
            }},
            "required": [
              "head",
              "head_type"
            ]
          }}
        }},
        "action": {{
          "type": "string",
          "description": "Hành động cần thực hiện, ví dụ: knowledge graph hoặc text document"
        }}
      }},
      "required": [
        "relationship",
        "action"
      ]
    }}

    You must answer in the following format:
    {{
        "relationship": [
          {{
            "head": "<head_name>",
            "head_type": <label_head>,
          }}
        ],
        "action": <action>
    }}
    head_name must be in singular form. DON'T EXPLAIN
"""












