import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch.nn.functional as F
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer, util
import torch


class Neo4j:
    def __init__(self, uri, user, password):
        """Khởi tạo kết nối tới Neo4j"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.sentence_model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

    def close(self):
        """Đóng kết nối tới Neo4j"""
        self.driver.close()

    def execute_cypher(self, query):
        """Thực thi một truy vấn Cypher"""
        with self.driver.session() as session:
            session.run(query)

    def add_entities_relation_highest(self):
        """Thêm các entities và relationships cấp cao"""
        cypher_queries = [
            # Episode 1: nlu - định hướng trường đại học nghiên cứu
            """
            MERGE (highest:General {name: 'tài liệu'})
            MERGE (document:Document {name: 'sổ tay sinh viên 2024'})
            MERGE (highest)-[:bao_gồm]->(document)

            MERGE (a:part {name: 'phần 1: nlu - định hướng trường đại học nghiên cứu'})
            MERGE (b:section {name: 'quá trình hình thành và phát triển'})
            MERGE (c:section {name: 'sứ mạng'})
            MERGE (d:section {name: 'tầm nhìn'})
            MERGE (e:section {name: 'giá trị cốt lõi'})
            MERGE (f:section {name: 'mục tiêu chiến lược'})
            MERGE (g:section {name: 'cơ sở vật chất'})
            MERGE (h:section {name: 'các đơn vị trong trường'})
            MERGE (i:section {name: 'các khoa - ngành đào tạo'})
            MERGE (j:section {name: 'tuần sinh hoạt công dân - sinh viên'})
            MERGE (k:section {name: 'hoạt động phong trào sinh viên'})
            MERGE (l:section {name: 'câu lạc bộ (clb) - đội, nhóm'})
            MERGE (m:section {name: 'cơ sở đào tạo'})
            MERGE (document)-[:bao_gồm]->(a)
            MERGE (a)-[:bao_gồm]->(b)
            MERGE (a)-[:bao_gồm]->(c)
            MERGE (a)-[:bao_gồm]->(d)
            MERGE (a)-[:bao_gồm]->(e)
            MERGE (a)-[:bao_gồm]->(f)
            MERGE (a)-[:bao_gồm]->(g)
            MERGE (a)-[:bao_gồm]->(h)
            MERGE (a)-[:bao_gồm]->(i)
            MERGE (a)-[:bao_gồm]->(j)
            MERGE (a)-[:bao_gồm]->(k)
            MERGE (a)-[:bao_gồm]->(l)
            MERGE (a)-[:bao_gồm]->(m)
            """,
            # Episode 2: học tập và rèn luyện
            """
            MERGE (n:part {name: 'phần 2: học tập và rèn luyện'})

            MERGE (o:section {name: 'quy chế sinh viên'})
            MERGE (o2:part {name: 'chương 2: quyền và nghĩa vụ của sinh viên'})
            MERGE (o2_4:article {name: 'điều 4: quyền của sinh viên'})
            MERGE (o2_5:article {name: 'điều 5: nghĩa vụ của sinh viên'})
            MERGE (o2_6:article {name: 'điều 6: các hành vi sinh viên không được làm'})

            MERGE (p:section {name: 'quy chế học vụ'})
            MERGE (p2:part {name: 'chương 2: lập kế hoạch và tổ chức giảng dạy'})
            MERGE (p2_9:article {name: 'điều 9: tổ chức đăng ký học tập'})
            MERGE (p2_10:article {name: 'điều 10: tổ chức lớp học phần'})
            MERGE (p3:part {name: 'chương 3: đánh giá kết quả học tập và cấp bằng tốt nghiệp'})
            MERGE (p3_12:article {name: 'điều 12: tổ chức thi kết thúc học phần'})
            MERGE (p3_13:article {name: 'điều 13: đánh giá và tính điểm học phần'})
            MERGE (p3_14:article {name: 'điều 14: xét tương đường và công nhận học phần của các cơ sở đào tạo khác'})
            MERGE (p3_15:article {name: 'điều 15: đánh giá kết quả học tập theo học kỳ, năm học'})
            MERGE (p3_16:article {name: 'điều 16: thông báo kết quả học tập'})
            MERGE (p3_17:article {name: 'điều 17: điểm rèn luyện(đrl)'})
            MERGE (p3_18:article {name: 'điều 18: xử lý kết quả học tập'})
            MERGE (p3_19:article {name: 'điều 19: khóa luận, tiểu luận, tích lũy tín chỉ tốt nghiệp'})
            MERGE (p3_20:article {name: 'điều 20: công nhận tốt nghiệp và cấp bằng tốt nghiêp'})
            MERGE (p4:part {name: 'chương 4: những quy định khác đối với sinh viên'})
            MERGE (p4_21:article {name: 'điều 21: nghỉ học tạm thời, thôi học'})
            MERGE (p4_24:article {name: 'điều 24: học cùng lúc hai chương trình'})

            MERGE (q:section {name: 'quy định về việc đào tạo trực tuyến'})
            MERGE (q0_3:article {name: 'điều 3: hệ thống đào tạo trực tuyến tại trường đại học nông lâm tp.hcm'})
            MERGE (q0_9:article {name: 'điều 9: đánh giá kết quả học tập trực tuyến'})
            MERGE (q0_13:article {name: 'điều 13: quyền và trách nhiệm của sinh viên'})

            MERGE (r:section {name: 'quy định khen thưởng, kỷ luật sinh viên'})
            MERGE (r2:part {name: 'chương 2: khen thưởng'})
            MERGE (r2_4:article {name: 'điều 4: nội dung khen thưởng'})
            MERGE (r2_5:article {name: 'điều 5: khen thưởng đối với cá nhân và tập thể sinh viên đạt thành tích xứng đánh để biểu dương, khen thưởng'})
            MERGE (r2_6:article {name: 'điều 6: khen thưởng đối với sinh viên tiêu biểu(svtb) vào cuối mỗi năm học'})
            MERGE (r2_7:article {name: 'điều 7: khen thưởng đối với sinh viên là thủ khoa, á khoa kỳ tuyển sinh đầu vào'})
            MERGE (r2_8:article {name: 'điều 8: khen thưởng đối với sinh viên tốt nghiệp'})
            MERGE (r3:part {name: 'chương 3: kỷ luật'})
            MERGE (r3_11:article {name: 'điều 11: hình thức kỷ luật và nội dung vi phạm'})
            MERGE (r3_12:article {name: 'điều 12: trình tự, thủ tục và hồ sơ xét kỷ luật'})
            MERGE (r3_13:article {name: 'điều 13: chấm dứt hiệu lực của quyết định kỷ luật'})
            MERGE (r3_0:article {name: 'một số nội dung vi phạm và khung xử lý kỷ luật sinh viên'})

            MERGE (s:section {name: 'quy chế đánh giá kết quả rèn luyện'})
            MERGE (s0_3:article {name: 'điều 3: nội dung đánh giá và thang điểm'})
            MERGE (s0_4:article {name: 'điều 4: đánh giá về ý thức tham gia học tập'})
            MERGE (s0_5:article {name: 'điều 5: đánh giá về ý thức chấp hành nội quy, quy chế, quy định trong cơ sở giáo dục đại học'})
            MERGE (s0_6:article {name: 'điều 6: đánh giá về ý thức tham gia các hoạt động chính trị, xã hội, văn hóa, nghệ thuật, thể thao, phòng chống tội phạm và các tệ nạn xã hội'})
            MERGE (s0_7:article {name: 'điều 7: đánh giá về ý thức công dân trong quản hệ cộng đồng'})
            MERGE (s0_8:article {name: 'điều 8: Đánh giá về ý thức và kết quả khi tham gia công tác cán bộ lớp, các đoàn thể, tổ chức trong cơ sở giáo dục đại học hoặc người học đạt được thành tích đặc biệt trong học tập, rèn luyện'})
            MERGE (s0_9:article {name: 'điều 9: phân loại kết quả rèn luyện'})
            MERGE (s0_10:article {name: 'điều 10: phân loại để đánh giá'})
            MERGE (s0_11:article {name: 'điều 11: quy trình đánh giá kết quả rèn luyện'})

            MERGE (t:section {name: 'quy tắc ứng xử văn hóa của người học'})
            MERGE (t0_4:article {name: 'điều 4: ứng xử với công tác học tập, nghiên cứu khoa học, rèn luyện'})
            MERGE (t0_5:article {name: 'điều 5: ứng xử đối với giảng viên và nhân viên nhà trường'})
            MERGE (t0_6:article {name: 'điều 6: ứng xử với bạn bè'})
            MERGE (t0_7:article {name: 'điều 7: ứng xử với cảnh quan môi trường và tài sản công'})

            MERGE (u:section {name: 'cố vấn học tập'})
            MERGE (v:section {name: 'danh hiệu sinh viên 5 tốt'})
            MERGE (v0_1:article {name: 'đạo đức tốt'})
            MERGE (v0_2:article {name: 'học tập tốt'})
            MERGE (v0_3:article {name: 'thể lực tốt'})
            MERGE (v0_4:article {name: 'tình nguyện tốt'})
            MERGE (v0_5:article {name: 'hội nhập tốt'})
            MERGE (v0_6:article {name: 'khái niệm'})

            MERGE (v1:part {name: 'ngoài ra ưu tiên xét chọn những sinh viên đạt ít nhất 01 trong các các tiêu chuẩn sau'})
            MERGE (v1_1:article {name: 'ưu tiên 1'})
            MERGE (v1_2:article {name: 'ưu tiên 2'})
            MERGE (v1_3:article {name: 'ưu tiên 3'})
            MERGE (v1_4:article {name: 'ưu tiên 4'})
            MERGE (v1_5:article {name: 'ưu tiên 5'})
            MERGE (v1_6:article {name: 'ưu tiên 6'})

            MERGE (w:section {name: 'danh hiệu sinh viên tiêu biểu'})

            MERGE (document)-[:bao_gồm]->(n)
            MERGE (n)-[:bao_gồm]->(o)
            MERGE (o)-[:bao_gồm]->(o2)
            MERGE (o2)-[:bao_gồm]->(o2_4)
            MERGE (o2)-[:bao_gồm]->(o2_5)
            MERGE (o2)-[:bao_gồm]->(o2_6)

            MERGE (n)-[:bao_gồm]->(p)
            MERGE (p)-[:bao_gồm]->(p2)
            MERGE (p2)-[:bao_gồm]->(p2_9)
            MERGE (p2)-[:bao_gồm]->(p2_10)
            MERGE (p)-[:bao_gồm]->(p3)
            MERGE (p3)-[:bao_gồm]->(p3_12)
            MERGE (p3)-[:bao_gồm]->(p3_13)
            MERGE (p3)-[:bao_gồm]->(p3_14)
            MERGE (p3)-[:bao_gồm]->(p3_15)
            MERGE (p3)-[:bao_gồm]->(p3_16)
            MERGE (p3)-[:bao_gồm]->(p3_17)
            MERGE (p3)-[:bao_gồm]->(p3_18)
            MERGE (p3)-[:bao_gồm]->(p3_19)
            MERGE (p3)-[:bao_gồm]->(p3_20)
            MERGE (p)-[:bao_gồm]->(p4)
            MERGE (p4)-[:bao_gồm]->(p4_21)
            MERGE (p4)-[:bao_gồm]->(p4_24)

            MERGE (n)-[:bao_gồm]->(q)
            MERGE (q)-[:bao_gồm]->(q0_3)
            MERGE (q)-[:bao_gồm]->(q0_9)
            MERGE (q)-[:bao_gồm]->(q0_13)

            MERGE (n)-[:bao_gồm]->(r)
            MERGE (r)-[:bao_gồm]->(r2)
            MERGE (r2)-[:bao_gồm]->(r2_4)
            MERGE (r2)-[:bao_gồm]->(r2_5)
            MERGE (r2)-[:bao_gồm]->(r2_6)
            MERGE (r2)-[:bao_gồm]->(r2_7)
            MERGE (r2)-[:bao_gồm]->(r2_8)
            MERGE (r)-[:bao_gồm]->(r3)
            MERGE (r3)-[:bao_gồm]->(r3_11)
            MERGE (r3)-[:bao_gồm]->(r3_12)
            MERGE (r3)-[:bao_gồm]->(r3_13)
            MERGE (r3)-[:bao_gồm]->(r3_0)

            MERGE (n)-[:bao_gồm]->(s)
            MERGE (s)-[:bao_gồm]->(s0_3)
            MERGE (s)-[:bao_gồm]->(s0_4)
            MERGE (s)-[:bao_gồm]->(s0_5)
            MERGE (s)-[:bao_gồm]->(s0_6)
            MERGE (s)-[:bao_gồm]->(s0_7)
            MERGE (s)-[:bao_gồm]->(s0_8)
            MERGE (s)-[:bao_gồm]->(s0_9)
            MERGE (s)-[:bao_gồm]->(s0_10)
            MERGE (s)-[:bao_gồm]->(s0_11)

            MERGE (n)-[:bao_gồm]->(t)
            MERGE (t)-[:bao_gồm]->(t0_4)
            MERGE (t)-[:bao_gồm]->(t0_5)
            MERGE (t)-[:bao_gồm]->(t0_6)
            MERGE (t)-[:bao_gồm]->(t0_7)

            MERGE (n)-[:bao_gồm]->(u)
            MERGE (n)-[:bao_gồm]->(v)
            MERGE (v)-[:bao_gồm]->(v0_1)
            MERGE (v)-[:bao_gồm]->(v0_2)
            MERGE (v)-[:bao_gồm]->(v0_3)
            MERGE (v)-[:bao_gồm]->(v0_4)
            MERGE (v)-[:bao_gồm]->(v0_5)
            MERGE (v)-[:bao_gồm]->(v0_6)
            MERGE (v)-[:bao_gồm]->(v1)
            MERGE (v1)-[:bao_gồm]->(v1_1)
            MERGE (v1)-[:bao_gồm]->(v1_2)
            MERGE (v1)-[:bao_gồm]->(v1_3)
            MERGE (v1)-[:bao_gồm]->(v1_4)
            MERGE (v1)-[:bao_gồm]->(v1_5)
            MERGE (v1)-[:bao_gồm]->(v1_6)

            MERGE (n)-[:bao_gồm]->(w)
            """,
            # Episode 3: hỗ trợ và dịch vụ
            """
            MERGE (x:part {name: 'phần 3: hỗ trợ và dịch vụ'})
            MERGE (y:section {name: 'quy định phân cấp giải quyết thắc mắc của sinh viên'})
            MERGE (y0_2:article {name: 'điều 2: hình thức thắc mắc, kiến nghị'})
            MERGE (y0_3:article {name: 'điều 3: các bước gửi thắc mắc, kiên nghị'})
            MERGE (y0_4:article {name: 'điều 4: những vấn đề trao đổi trực tiếp hoặc gửi thư qua email'})
            MERGE (y0_5:article {name: 'điều 5: trách nhiệm của giảng viên và các bộ phận chức năng'})
            MERGE (y0_6:article {name: 'điều 6: những vấn đề đã trao đổi trực tiêp hoặc gửi thư không được giải quyết thoải đáng'})
            MERGE (y0_7:article {name: 'điều 7: những vấn đề liên quan đến tổ chức lớp học phần'})
            MERGE (y0_8:article {name: 'điều 8: những vấn đề liên quan đến điểm bộ phận, điểm thi kết thúc học phần, điểm thi học phần và tổ chức thi'})
            MERGE (y0_9:article {name: 'điều 9; chuyển thắc mắc, kiến nghị của sinh viên'})
            MERGE (y0_10:article {name: 'điều 10: những nội dung được nói trực tuyến trên website'})
            MERGE (y0_11:article {name: 'điều 11: yêu cầu đối với sinh viên tham gia trực tuyến'})

            MERGE (z:section {name: 'thông tin học bổng tài trợ'})
            MERGE (aa:section {name: 'vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})
            MERGE (aa0_1:article {name: 'đối tượng sinh viên được hỗ trợ vay tiền'})
            MERGE (aa0_2:article {name: 'điều kiện để được hỗ trợ vay tiền sinh viên'})
            MERGE (aa0_3:article {name: 'mức tiền và lãi suất hỗ trợ vay tiền sinh viên'})
            MERGE (aa0_4:article {name: 'phương thức cho vay tiền sinh viên'})
            MERGE (aa0_5:article {name: 'thông tin về vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})

            MERGE (bb:section {name: 'quy trình xác nhận hồ sơ sinh viên'})
            MERGE (bb0_1:article {name: 'các loại giấy tờ được xác nhận'})
            MERGE (bb0_2:article {name: 'kênh đăng ký'})
            MERGE (bb0_3:article {name: 'đăng ký'})
            MERGE (bb0_4:article {name: 'quy trình'})

            MERGE (cc:section {name: 'hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên'})
            MERGE (dd:section {name: 'thông tin về bảo hiểm y tế'})

            MERGE (ee:section {name: 'hướng dẫn sử dụng các kênh thanh toán học phí, bhyt, lệ phí xét tốt nghiệp'})
            MERGE (ee0_1:article {name: 'thanh toán tại quầy giao dịch của bidv'})
            MERGE (ee0_2:article {name: 'thanh toán qua kênh bidv smart banking'})
            MERGE (ee0_3:article {name: 'thanh toán qua kênh bidv online'})
            MERGE (ee0_4:article {name: 'thanh toán qua atm của bidv'})
            MERGE (ee0_5:article {name: 'thanh toán qua website sinh viên'})
            MERGE (ee0_6:article {name: 'hướng dẫn cài đặt sinh trắc học'})

            MERGE (ff:section {name: 'tham vấn tâm lý học đường'})
            MERGE (gg:section {name: 'trung tâm dịch vụ sinh viên'})

            MERGE (mm:section {name: 'thông tin học bổng khuyến khích học tập'})
            MERGE (mm0_1:article {name: 'đối tượng'})
            MERGE (mm0_2:article {name: 'quỹ học bổng khuyến khích học tập'})
            MERGE (mm0_3:article {name: 'căn cứ để xét học bổng khuyến khích học tập'})
            MERGE (mm0_4:article {name: 'mức học bổng khuyến khích học tập'})
            MERGE (mm0_5:article {name: 'quy trình xét học bổng'})

            MERGE (document)-[:bao_gồm]->(x)
            MERGE (x)-[:bao_gồm]->(y)
            MERGE (y)-[:bao_gồm]->(y0_2)
            MERGE (y)-[:bao_gồm]->(y0_3)
            MERGE (y)-[:bao_gồm]->(y0_4)
            MERGE (y)-[:bao_gồm]->(y0_5)
            MERGE (y)-[:bao_gồm]->(y0_6)
            MERGE (y)-[:bao_gồm]->(y0_7)
            MERGE (y)-[:bao_gồm]->(y0_8)
            MERGE (y)-[:bao_gồm]->(y0_9)
            MERGE (y)-[:bao_gồm]->(y0_10)
            MERGE (y)-[:bao_gồm]->(y0_11)

            MERGE (x)-[:bao_gồm]->(z)
            MERGE (x)-[:bao_gồm]->(aa)
            MERGE (aa)-[:bao_gồm]->(aa0_1)
            MERGE (aa)-[:bao_gồm]->(aa0_2)
            MERGE (aa)-[:bao_gồm]->(aa0_3)
            MERGE (aa)-[:bao_gồm]->(aa0_4)
            MERGE (aa)-[:bao_gồm]->(aa0_5)

            MERGE (x)-[:bao_gồm]->(bb)
            MERGE (bb)-[:bao_gồm]->(bb0_1)
            MERGE (bb)-[:bao_gồm]->(bb0_2)
            MERGE (bb)-[:bao_gồm]->(bb0_3)
            MERGE (bb)-[:bao_gồm]->(bb0_4)

            MERGE (x)-[:bao_gồm]->(cc)
            MERGE (x)-[:bao_gồm]->(dd)
            MERGE (x)-[:bao_gồm]->(ee)
            MERGE (ee)-[:bao_gồm]->(ee0_1)
            MERGE (ee)-[:bao_gồm]->(ee0_2)
            MERGE (ee)-[:bao_gồm]->(ee0_3)
            MERGE (ee)-[:bao_gồm]->(ee0_4)
            MERGE (ee)-[:bao_gồm]->(ee0_5)
            MERGE (ee)-[:bao_gồm]->(ee0_6)

            MERGE (x)-[:bao_gồm]->(ff)
            MERGE (x)-[:bao_gồm]->(gg)
            MERGE (x)-[:bao_gồm]->(mm)
            MERGE (mm)-[:bao_gồm]->(mm0_1)
            MERGE (mm)-[:bao_gồm]->(mm0_2)
            MERGE (mm)-[:bao_gồm]->(mm0_3)
            MERGE (mm)-[:bao_gồm]->(mm0_4)
            MERGE (mm)-[:bao_gồm]->(mm0_5)
            """
        ]
        for query in cypher_queries:
            self.execute_cypher(query)

    def add_entities(self, entities):
        def _add_entities(tx, entities):
            for entity in entities:
                print(entity)
                name = entity["name"]
                entity_type = entity["type"]
                query = f"MERGE (e:{entity_type} {{name: $name}})"
                tx.run(query, name=name)

        with self.driver.session() as session:
            session.execute_write(_add_entities, entities)

    def stringify_node_properties(self, props):
        return "; ".join(f"{k} {v}" for k, v in props.items())

    def encode(self, texts):
        return self.sentence_model.encode(texts, convert_to_tensor=True)

    def re_ranking(self, embed_question, embed_documents, documents):
        if embed_question.dim() == 1:
            embed_question = embed_question.unsqueeze(0)

        similarities = F.cosine_similarity(embed_question, embed_documents, dim=-1)

        results = [doc for sim, doc in zip(similarities.tolist(), documents) if sim > 0]

        return results

    def fetch_subgraph(self, query):
        def _fetch_subgraph(tx, query):
            result = tx.run(query)
            nodes = {}
            edges = []

            for record in result:
                path = record["p"]

                # Lấy tất cả nodes trong path
                for node in path.nodes:
                    node_id = node.element_id
                    if node_id not in nodes:
                        nodes[node_id] = {
                            'properties': dict(node.items())
                        }

                # Lấy tất cả relationships trong path
                for rel in path.relationships:
                    src_id = rel.start_node.element_id
                    tgt_id = rel.end_node.element_id

                    edge_info = {
                        'source': src_id,
                        'target': tgt_id,
                        'type': rel.type,
                        'properties': dict(rel.items())
                    }

                    edges.append(edge_info)

                    # Đảm bảo start_node và end_node cũng được thêm vào nodes
                    if src_id not in nodes:
                        nodes[src_id] = {
                            'properties': dict(rel.start_node.items())
                        }

                    if tgt_id not in nodes:
                        nodes[tgt_id] = {
                            'properties': dict(rel.end_node.items())
                        }

            return nodes, edges

        # Lấy data từ Neo4j
        with self.driver.session() as session:
            # Sử dụng execute_read thay vì read_transaction (deprecated)
            nodes, edges = session.execute_read(_fetch_subgraph, query)

        return nodes, edges

    def add_relationships(self, relationships, type_part, part):
        def _add_relationships(tx, relationships, part):
            for rel in relationships:
                source = rel["source"]
                target = rel["target"]
                relation = rel["relation"]
                type_source = rel["type_source"]
                type_target = rel["type_target"]

                # Sử dụng APOC để merge mối quan hệ với nhãn động
                query = """
                    MATCH (source:%s {name: $source})
                    MATCH (target:%s {name: $target})
                    CALL apoc.merge.relationship(source, $relation, {}, {}, target)
                    YIELD rel
                    RETURN rel
                """ % (type_source, type_target)
                tx.run(query, source=source, target=target, relation=relation)

                # Chỉ tạo mối quan hệ bao_gồm nếu part được cung cấp
                if part:
                    part_query = """
                        MATCH (p:%s {name: $part})
                        MATCH (s:%s {name: $source})
                        MERGE (p)-[:bao_gồm]->(s)
                    """ % (type_part, type_source)
                    tx.run(part_query, part=part, source=source)

        with self.driver.session() as session:
            session.execute_write(_add_relationships, relationships, part)

    def get_owned_entities(self, type, source, relation):
        query = f"""
            MATCH (o:{type} {{name: "{source}"}})-[r:{relation}]->(e)
            RETURN o AS source, r AS relationship, e AS target
        """

        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

    def get_path(self, cypher_query):
        with self.driver.session() as session:
            result = session.run(cypher_query)
            return [record for record in result]

    def create_documents(self, records):
        documents = []

        for record in records:
            relations = record["relation"]

            for rel in relations:
                source_node = rel.start_node
                target_node = rel.end_node
                relation_type = rel.type

                # Lấy thuộc tính của nguồn và đích
                source_properties = dict(source_node)
                target_properties = dict(target_node)

                # Chuyển thuộc tính thành chuỗi
                source_str = str(source_properties) if source_properties else "{}"
                target_str = str(target_properties) if target_properties else "{}"

                # Tạo triplet dạng chuỗi
                triplet = f"{source_str} {relation_type} {target_str}"
                documents.append(triplet)

        return documents

    def import_relationships(self, content, part, type_Part):
        relationships = content["relationships"]
        with self.driver.session() as session:
            for rel in relationships:
                source = rel["source"]
                target = rel["target"]
                relation = rel["relation"].upper().replace(" ", "_").replace("-", "_")
                print(f'{source} {relation} {target}')
                type_source = self._capitalize_label(rel["type_source"])
                type_target = self._capitalize_label(rel["type_target"])
                type_Part_cap = self._capitalize_label(type_Part)

                session.execute_write(
                    self._create_relation_with_Part,
                    source, type_source,
                    target, type_target,
                    relation,
                    part, type_Part_cap
                )

    @staticmethod
    def _capitalize_label(label):
        # Chuyển thành PascalCase: "university branch" -> "UniversityBranch"
        return ''.join(word.capitalize() for word in label.split(' '))

    @staticmethod
    def _create_relation_with_Part(tx, source, type_source, target, type_target, relation, Part, type_Part):
        query = f"""
           MERGE (src:{type_source} {{name: $source_name}})
           SET src += $source_props

           MERGE (tgt:{type_target} {{name: $target_name}})
           SET tgt += $target_props

           MERGE (Part:{type_Part} {{name: $Part}})
           MERGE (src)-[:{relation}]->(tgt)
           MERGE (Part)-[:BAO_GỒM]->(src)
           """
        tx.run(query,
               source_name=source["name"],
               source_props=source,
               target_name=target["name"],
               target_props=target,
               Part=Part
               )

    def add_single_relationship(self, source_name, source_type, target_name, target_type, relation_type):
        source_name = source_name.lower()
        target_name = target_name.lower()

        source_type = self._capitalize_label(source_type)
        target_type = self._capitalize_label(target_type)

        query = f"""
            MERGE (a:{source_type} {{name: $source_name}})
            MERGE (b:{target_type} {{name: $target_name}})
            MERGE (a)-[r:{relation_type}]->(b)
            RETURN r
        """
        with self.driver.session() as session:
            session.run(query, source_name=source_name, target_name=target_name)

    def get_part_of_document(self, document_id: str) -> str:
        query = """
            MATCH (a:Document {name: $document_id})-[]->(e)
            RETURN e
        """
        with self.driver.session() as session:
            result = session.run(query, document_id=document_id)
            nodes = [record["e"] for record in result]

            if not nodes:
                return ""

            # Lấy danh sách part names, loại bỏ trùng lặp
            part_names = []
            for node in nodes:
                part_name = node.get("name")
                if part_name and part_name not in part_names:
                    part_names.append(part_name)

            # Format Cypher
            lines = []
            lines.append("MERGE (highest:General {name: 'tài liệu'})")
            lines.append(f"MERGE (document:Document {{name: '{document_id}'}})")
            lines.append("MERGE (highest)-[:BAO_GỒM]->(document)\n")

            var_names = [chr(i) for i in range(ord('a'), ord('a') + len(part_names))]

            for var, part in zip(var_names, part_names):
                lines.append(f"MERGE ({var}:Part {{name: '{part}'}})")

            lines.append("")

            for var in var_names:
                lines.append(f"MERGE (document)-[:BAO_GỒM]->({var})")

            return "\n".join(lines)

    def delete_part_of_document(self, document_id):
        query = """
            MATCH (a:Document {name: $document_id})-[*0..]->(b)
            DETACH DELETE a, b
        """
        with self.driver.session() as session:
            session.run(query, document_id=document_id)

    def add_to_neo4j(self, source, target, relation, source_type, target_type):
        if source_type == 'paper':
            source_name = source['title']
        else:
            source_name = source['name']

        if target_type == 'paper':
            target_name = target['title']
        else:
            target_name = target['name']

        with self.driver.session() as session:
            session.execute_write(
                lambda tx: tx.run(
                    f"""
                    MERGE (s:{source_type} {{name: $source_name}})
                    SET s += $source_props

                    MERGE (t:{target_type} {{name: $target_name}})
                    SET t += $target_props

                    MERGE (s)-[r:`{relation}`]->(t)
                    """,
                    source_name=source_name,
                    target_name=target_name,
                    source_props=source,
                    target_props=target,
                )
            )

    def add_to_neo4j_02(self, source, target, relation, source_type, target_type):
        """
        Add source and target node into Neo4j using full JSON string as unique key.
        """
        with self.driver.session() as session:
            session.execute_write(
                lambda tx: tx.run(
                    f"""
                    MERGE (s:{source_type} {{raw_json: $source_json}})
                    MERGE (t:{target_type} {{raw_json: $target_json}})
                    MERGE (s)-[r:`{relation}`]->(t)
                    """,
                    source_json=json.dumps(source, ensure_ascii=False),
                    target_json=json.dumps(target, ensure_ascii=False),
                )
            )

    def run_cypher(self, query):
        node_names = []
        rel_names = []
        triplets = []

        with self.driver.session() as session:
            result = session.run(query)
            if result:
                for record in result:
                    path_obj = record["p"]

                    # Lấy tên các node
                    for node in path_obj.nodes:
                        name = node.get("name")
                        if name and name not in node_names:
                            node_names.append(name)

                    # Lấy tên các quan hệ và tạo triplets với tất cả thuộc tính node
                    for rel in path_obj.relationships:
                        rel_type = rel.type
                        if rel_type and rel_type not in rel_names:
                            rel_names.append(rel_type)

                        # Lấy tất cả thuộc tính của node nguồn và node đích
                        source_node = self.remove_id_fields(dict(rel.start_node))
                        target_node = self.remove_id_fields(dict(rel.end_node))

                        triplets.append({
                            "source": source_node,
                            "relation": rel_type,
                            "target": target_node
                        })

        self.driver.close()
        return node_names, rel_names, triplets

    def remove_id_fields(self, data):
        if isinstance(data, dict):
            new_data = {}
            for k, v in data.items():
                if "id" not in k.lower():  # bỏ qua key chứa "id"
                    new_data[k] = self.remove_id_fields(v)
            return new_data
        elif isinstance(data, list):
            return [self.remove_id_fields(item) for item in data]
        else:
            return data
