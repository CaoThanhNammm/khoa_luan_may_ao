import os
from PreProcessing.PreProcessing import PreProcessing
from knowledge_graph.KnowledgeGraphDatabase import Neo4j
pre_processing = PreProcessing()
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    # Thay đổi thông tin kết nối theo cấu hình Neo4j của bạn
    uri = os.getenv("URI_NEO")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    # Tạo instance của class Neo4j
    neo = Neo4j(uri, user, password)

    # 1. Thêm các entities và relationships cấp cao
    # neo.add_entities_relation_highest()

    # 2. thêm entities và relationship vào neo4j
    content ={
  "relationships": [
    {
      "source": {
        "name": "Phòng Công tác sinh viên",
        "type": "organization",
        "role_description": "Lập danh sách sinh viên đủ điều kiện xét học bổng",
        "action_frequency": "Sau mỗi học kỳ",
        "basis_of_action": "Các tiêu chí quy định"
      },
      "target": {
        "name": "danh sách sinh viên đủ điều kiện xét học bổng",
        "type": "document",
        "content_summary": "Sinh viên đủ điều kiện xét học bổng khuyến khích học tập",
        "preparation_guideline": "Theo các tiêu chí quy định",
        "submission_target": "Hội đồng xét duyệt"
      },
      "type_source": "organization",
      "type_target": "document",
      "relation": "lập"
    },
    {
      "source": {
        "name": "Phòng Công tác sinh viên",
        "type": "organization",
        "action_performed": "Trình danh sách",
        "document_involved": "Danh sách sinh viên đủ điều kiện xét học bổng",
        "recipient_authority": "Hội đồng xét duyệt"
      },
      "target": {
        "name": "Hội đồng xét duyệt",
        "type": "organization",
        "function_performed": "Xét duyệt học bổng",
        "input_document_source": "Phòng Công tác sinh viên",
        "decision_framework": "Quỹ học bổng, thứ tự ưu tiên"
      },
      "type_source": "organization",
      "type_target": "organization",
      "relation": "trình_danh_sách_cho"
    },
    {
      "source": {
        "name": "danh sách sinh viên đủ điều kiện xét học bổng",
        "type": "document",
        "structuring_criterion_1": "Theo từng khối học bổng",
        "originator": "Phòng Công tác sinh viên",
        "overall_purpose": "Xét duyệt học bổng khuyến khích học tập"
      },
      "target": {
        "name": "khối học bổng",
        "type": "scholarship_category",
        "role_in_listing": "Phân loại danh sách sinh viên",
        "funding_relevance": "Được cấp quỹ học bổng riêng",
        "application_context": "Xét duyệt học bổng"
      },
      "type_source": "document",
      "type_target": "scholarship_category",
      "relation": "được_lập_theo"
    },
    {
      "source": {
        "name": "danh sách sinh viên đủ điều kiện xét học bổng",
        "type": "document",
        "structuring_criterion_2": "Theo thứ tự ưu tiên loại học bổng",
        "priority_order_direction": "Từ cao xuống thấp",
        "contextual_use": "Xếp hạng sinh viên cho việc xét học bổng"
      },
      "target": {
        "name": "loại học bổng",
        "type": "scholarship_level",
        "basis_for_ranking": "Mức độ học bổng (cao, trung bình, thấp)",
        "list_ordering_principle": "Ưu tiên từ cao xuống thấp",
        "usage_in_process": "Xếp thứ tự ưu tiên trong danh sách xét duyệt"
      },
      "type_source": "document",
      "type_target": "scholarship_level",
      "relation": "xếp_theo_thứ_tự_ưu_tiên_của"
    },
    {
      "source": {
        "name": "loại học bổng",
        "type": "scholarship_level",
        "tie_breaking_trigger": "Nhiều sinh viên đạt cùng loại học bổng",
        "prioritization_sequence": "Tiêu chí phụ thứ nhất",
        "application_scenario": "Khi xếp ưu tiên sinh viên có cùng mức học bổng"
      },
      "target": {
        "name": "điểm trung bình chung học bổng",
        "type": "academic_criteria",
        "function_in_tie_breaking": "Tiêu chí ưu tiên phụ hàng đầu",
        "nature_of_criterion": "Điểm trung bình chung của học kỳ xét học bổng",
        "scope_of_application": "Khi có nhiều sinh viên cùng loại học bổng"
      },
      "type_source": "scholarship_level",
      "type_target": "academic_criteria",
      "relation": "có_tiêu_chí_ưu_tiên_phụ_là"
    },
    {
      "source": {
        "name": "loại học bổng",
        "type": "scholarship_level",
        "tie_breaking_trigger": "Nhiều sinh viên đạt cùng loại học bổng",
        "prioritization_sequence": "Tiêu chí phụ thứ hai",
        "application_scenario": "Khi xếp ưu tiên sinh viên có cùng mức học bổng"
      },
      "target": {
        "name": "điểm rèn luyện",
        "type": "conduct_criteria",
        "function_in_tie_breaking": "Tiêu chí ưu tiên phụ thứ hai",
        "nature_of_criterion": "Điểm đánh giá hạnh kiểm và rèn luyện",
        "scope_of_application": "Khi có nhiều sinh viên cùng loại học bổng"
      },
      "type_source": "scholarship_level",
      "type_target": "conduct_criteria",
      "relation": "có_tiêu_chí_ưu_tiên_phụ_là"
    },
    {
      "source": {
        "name": "loại học bổng",
        "type": "scholarship_level",
        "tie_breaking_trigger": "Nhiều sinh viên đạt cùng loại học bổng",
        "prioritization_sequence": "Tiêu chí phụ thứ ba",
        "application_scenario": "Khi xếp ưu tiên sinh viên có cùng mức học bổng"
      },
      "target": {
        "name": "số tín chỉ đã học trong học kỳ",
        "type": "academic_criteria",
        "function_in_tie_breaking": "Tiêu chí ưu tiên phụ thứ ba",
        "nature_of_criterion": "Số lượng tín chỉ hoàn thành trong học kỳ đang xét",
        "scope_of_application": "Khi có nhiều sinh viên cùng loại học bổng"
      },
      "type_source": "scholarship_level",
      "type_target": "academic_criteria",
      "relation": "có_tiêu_chí_ưu_tiên_phụ_là"
    },
    {
      "source": {
        "name": "loại học bổng",
        "type": "scholarship_level",
        "tie_breaking_trigger": "Nhiều sinh viên đạt cùng loại học bổng",
        "prioritization_sequence": "Tiêu chí phụ thứ tư",
        "application_scenario": "Khi xếp ưu tiên sinh viên có cùng mức học bổng"
      },
      "target": {
        "name": "điểm trung bình chung tích lũy",
        "type": "academic_criteria",
        "function_in_tie_breaking": "Tiêu chí ưu tiên phụ thứ tư",
        "nature_of_criterion": "Điểm trung bình chung của tất cả các học kỳ đã học",
        "scope_of_application": "Khi có nhiều sinh viên cùng loại học bổng"
      },
      "type_source": "scholarship_level",
      "type_target": "academic_criteria",
      "relation": "có_tiêu_chí_ưu_tiên_phụ_là"
    },
    {
      "source": {
        "name": "Hội đồng xét duyệt",
        "type": "organization",
        "primary_action": "Xét duyệt học bổng",
        "key_reference_resource": "Quỹ học bổng khuyến khích học tập",
        "scope_of_decision": "Các khối học bổng"
      },
      "target": {
        "name": "quỹ học bổng khuyến khích học tập",
        "type": "financial_resource",
        "main_purpose": "Cấp học bổng khuyến khích học tập",
        "managing_entity": "Hội đồng xét duyệt",
        "allocation_granularity": "Theo khối học bổng"
      },
      "type_source": "organization",
      "type_target": "financial_resource",
      "relation": "căn_cứ_vào"
    },
    {
      "source": {
        "name": "Hội đồng xét duyệt",
        "type": "organization",
        "specific_action": "Xét duyệt học bổng cho từng khối",
        "operational_method": "Theo thứ tự ưu tiên từ cao xuống thấp",
        "limiting_factor": "Đến khi hết quỹ học bổng của khối đó",
        "reference_fund": "Quỹ học bổng khuyến khích học tập"
      },
      "target": {
        "name": "khối học bổng",
        "type": "scholarship_category",
        "status_in_process": "Đối tượng được Hội đồng xét duyệt",
        "associated_fund": "Quỹ học bổng khuyến khích học tập cấp cho khối",
        "review_logic": "Theo thứ tự ưu tiên cho đến khi hết quỹ"
      },
      "type_source": "organization",
      "type_target": "scholarship_category",
      "relation": "xét_duyệt_cho"
    },
    {
      "source": {
        "name": "danh sách sinh viên đủ điều kiện xét học bổng",
        "type": "document",
        "specific_purpose": "Cung cấp thông tin cho việc xét học bổng khuyến khích học tập",
        "main_content": "Sinh viên đáp ứng tiêu chí học bổng",
        "relevance_to_scholarship": "Học bổng khuyến khích học tập"
      },
      "target": {
        "name": "học bổng khuyến khích học tập",
        "type": "scholarship_type",
        "description_value": "Học bổng nhằm khuyến khích thành tích học tập",
        "key_input_document": "Danh sách sinh viên đủ điều kiện xét học bổng",
        "awarding_authority": "Hội đồng xét duyệt"
      },
      "type_source": "document",
      "type_target": "scholarship_type",
      "relation": "là_danh_sách_cho"
    }
  ]
}

    part = "quy trình xét học bổng"
    type_part = "Article"

    neo.import_relationships(content, part, type_part)
    neo.close()


# lấy tất cả quan hệ
# MATCH (n)-[r]->(m)
# RETURN n, r, m;



# xóa tất cả quan hệ
# MATCH (n)
# DETACH DELETE n;

# bac 2
# MATCH (first:part {name: 'phần 3: hỗ trợ và dịch vụ'})-[:bao_gồm]->(second:section {name: 'trung tâm dịch vụ sinh viên'})-[r*1..3]->(e)
# RETURN r as relation, e as target

# bac 3
# MATCH (first:part {name: 'phần 3: hỗ trợ và dịch vụ'})-[:bao_gồm]->(second:section {name: 'vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})-[:bao_gồm]->(four:article {name: 'thông tin về vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên'})-[r*1..3]->(e)
# RETURN r as relation, e as target

# bac 4
# MATCH (first:part {name: 'phần 3: hỗ trợ và dịch vụ'})-[:bao_gồm]->(second:section {name: 'quy định phân cấp giải quyết thắc mắc của sinh viên'})-[:bao_gồm]->(third:part {name: 'ngoài ra ưu tiên xét chọn những sinh viên đạt ít nhất 01 trong các các tiêu chuẩn sau'})-[:bao_gồm]->(four:article {name: 'ưu tiên 6'})-[r*1..3]->(e)
# RETURN r as relation, e as target


# xoa tat ca cac node tu node co san
# MATCH (a:article {name: 'phương thức cho vay tiền sinh viên'})-[r]->(b)
# DETACH DELETE b


# tạo dump neo4j aura
# CALL apoc.export.cypher.all(null, {stream: true, format: "cypher"})
# YIELD cypherStatements
# RETURN cypherStatements



