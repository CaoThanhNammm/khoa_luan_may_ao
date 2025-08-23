import pandas as pd
import ast
import re
import unicodedata
from typing import List, Set, Dict, Tuple

GT_PATH = r"D:\dataset_benchmark_khoa_luan\prime\prime_auto_qa.csv"
PRED_PATH = r"C:\Users\Nam\Desktop\my_qa_prime.csv"
DETAILS_OUT = r".\eval_details_prime.csv"  # file chi tiết kết quả từng query


def strip_accents_lower(s: str) -> str:
    """Bỏ dấu tiếng Việt/Unicode và đưa về lowercase."""
    if s is None:
        return ""
    s = str(s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.lower()

def normalize_basic(s: str) -> str:
    """Chuẩn hoá cơ bản: bỏ dấu, lowercase, loại ký tự ngoài [a-z0-9 ] và gộp khoảng trắng."""
    s = strip_accents_lower(s)
    # thay các ký tự không phải chữ/số bằng khoảng trắng
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def split_candidates(text: str) -> List[str]:
    """
    Tách 1 chuỗi dự đoán thành nhiều mục theo các dấu ngắt phổ biến:
    xuống dòng, dấu phẩy, chấm phẩy, dấu gạch đầu dòng/bullet.
    """
    if pd.isna(text):
        return []
    # bỏ markdown như ** **, *
    text = re.sub(r"\*+", "", str(text))
    # tách bởi xuống dòng, dấu phẩy, chấm phẩy, hoặc đầu dòng có '-' '•'
    parts = re.split(r"[\n,;]|(?:^\s*[-•]\s*)", text)
    parts = [p.strip() for p in parts if p and p.strip()]
    return parts

def generate_variants(s: str) -> Set[str]:
    """
    Sinh tập biến thể chuẩn hoá để so khớp:
    - full string đã chuẩn hoá
    - bản loại bỏ toàn bộ phần trong ngoặc (nếu có)
    - tất cả nội dung trong ngoặc (thường là viết tắt như EDN1, EDNRA)
    """
    variants = set()
    s = str(s)

    # 1) full
    variants.add(normalize_basic(s))

    # 2) bỏ toàn bộ ngoặc
    no_paren = re.sub(r"\([^)]*\)", "", s)
    variants.add(normalize_basic(no_paren))

    # 3) lấy nội dung trong ngoặc, tách thêm theo / , ; | hoặc ' or '
    inside = re.findall(r"\(([^)]*)\)", s)
    for chunk in inside:
        # tách theo nhiều ký tự phân cách
        for piece in re.split(r"[/,;|]|(?:\bor\b)", chunk):
            piece = piece.strip()
            if piece:
                variants.add(normalize_basic(piece))

    # 4) nếu trong chuỗi có các token viết hoa (trước khi lower), coi như viết tắt → thêm biến thể
    upper_tokens = re.findall(r"\b([A-Z0-9]{3,})\b", s)
    for tok in upper_tokens:
        variants.add(normalize_basic(tok))

    # Loại rỗng nếu có
    variants.discard("")
    return variants

ground_truth = pd.read_csv(GT_PATH)
predictions = pd.read_csv(PRED_PATH)

# Đồng bộ tên cột
ground_truth = ground_truth.rename(columns={"query": "question"})
# cột 'question' của predictions đã đúng tên rồi

# Parse ground truth answer từ string -> list
def parse_ground_truth(ans):
    try:
        val = ast.literal_eval(ans)
        # đảm bảo là list
        if isinstance(val, list):
            return val
        return [str(val)]
    except Exception:
        return [str(ans)]

ground_truth["answer"] = ground_truth["answer"].apply(parse_ground_truth)

# Làm sạch predicted answer: tách thành list (giữ thứ tự như là rank)
predictions["answer"] = predictions["answer"].apply(split_candidates)

def evaluate_metrics(gt_df: pd.DataFrame, pred_df: pd.DataFrame) -> Tuple[Dict[str, float], pd.DataFrame]:
    # Merge theo question
    df = pd.merge(
        gt_df[["question", "answer"]],
        pred_df[["question", "answer"]],
        on="question",
        suffixes=("_true", "_pred"),
        how="inner",
    )

    hit1 = hit5 = recall20 = mrr = 0.0
    details_rows = []

    Q = len(df)
    if Q == 0:
        raise ValueError("Không có query nào trùng giữa ground truth và predictions sau khi merge theo 'question'.")

    for idx, row in df.iterrows():
        true_items: List[str] = [str(x) for x in row["answer_true"]]
        pred_items: List[str] = [str(x) for x in row["answer_pred"]]

        # Tạo map: variant -> index của item ground truth tương ứng
        # Đồng thời tạo bộ biến thể cho từng item GT để tính Recall theo số item GT duy nhất được tìm thấy
        gt_variant_to_idx: Dict[str, int] = {}
        gt_variants_list: List[Set[str]] = []
        for gi, gt_item in enumerate(true_items):
            vset = generate_variants(gt_item)
            gt_variants_list.append(vset)
            for v in vset:
                # Ưu tiên giữ mapping đầu tiên nếu trùng biến thể giữa các GT
                if v not in gt_variant_to_idx:
                    gt_variant_to_idx[v] = gi

        # ---- Hit@1 ----
        hit1_i = 0
        if len(pred_items) > 0:
            first_variants = generate_variants(pred_items[0])
            if any(v in gt_variant_to_idx for v in first_variants):
                hit1_i = 1

        # ---- Hit@5 ----
        hit5_i = 0
        top5 = pred_items[:5]
        for p in top5:
            if any(v in gt_variant_to_idx for v in generate_variants(p)):
                hit5_i = 1
                break

        # ---- Recall@20 ----
        matched_truth_idx: Set[int] = set()
        for p in pred_items[:20]:
            pv = generate_variants(p)
            for v in pv:
                if v in gt_variant_to_idx:
                    matched_truth_idx.add(gt_variant_to_idx[v])
        recall20_i = len(matched_truth_idx) / max(1, len(true_items))

        # ---- MRR ----
        rr_i = 0.0
        for rank, p in enumerate(pred_items, start=1):
            pv = generate_variants(p)
            if any(v in gt_variant_to_idx for v in pv):
                rr_i = 1.0 / rank
                break

        # Cộng dồn
        hit1 += hit1_i
        hit5 += hit5_i
        recall20 += recall20_i
        mrr += rr_i

        # Lưu chi tiết
        details_rows.append({
            "question": row["question"],
            "gt_answers_raw": true_items,
            "pred_answers_raw": pred_items,
            "hit@1_i": hit1_i,
            "hit@5_i": hit5_i,
            "recall@20_i": recall20_i,
            "rr_i": rr_i,
            "first_pred": pred_items[0] if pred_items else "",
            "matched_truth_count_top20": len(matched_truth_idx),
        })

    metrics = {
        "Hit@1": hit1 / Q,
        "Hit@5": hit5 / Q,
        "Recall@20": recall20 / Q,
        "MRR": mrr / Q,
        "Q": Q,
    }

    details_df = pd.DataFrame(details_rows)
    return metrics, details_df

metrics, details = evaluate_metrics(ground_truth, predictions)
print("=== Metrics Summary ===")
for k, v in metrics.items():
    print(f"{k}: {v:.6f}")

# Lưu chi tiết để debug
details.to_csv(DETAILS_OUT, index=False, encoding="utf-8")
print(f"Đã lưu chi tiết từng truy vấn tại: {DETAILS_OUT}")




