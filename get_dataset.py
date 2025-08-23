import pandas as pd

def create_quest_answer(quest_dt, ans_dt, name_file):
    ans_dt['answer_ids'] = ans_dt['answer_ids'].astype(str)
    answer_dict = dict(zip(ans_dt['answer_ids'], ans_dt['answer']))
    def convert_ids_to_answers(answer_ids_str):
        # Chuyển đổi mảng answer_ids_str dạng chuỗi thành danh sách answer_ids
        answer_ids = eval(answer_ids_str)

        answers = []
        for answer_id in answer_ids:
            try:
                answer = answer_dict[str(answer_id)]
                answers.append(answer)
            except:
                continue
        return answers

    quest_dt['answers'] = quest_dt['answer_ids'].apply(convert_ids_to_answers)
    output_df = quest_dt[['query', 'answers']]
    output_df.to_csv(name_file, index=False)
    print(f"File {name_file} đã được tạo thành công.")


# stark-mag và stark-prime
splits = {'synthesized_all_split_mag': 'qa/mag/stark_qa/stark_qa.csv', 'humen_generated_eval_mag': 'qa/mag/stark_qa/stark_qa_human_generated_eval.csv', 'synthesized_all_split_prime': 'qa/prime/stark_qa/stark_qa.csv', 'humen_generated_eval_prime': 'qa/prime/stark_qa/stark_qa_human_generated_eval.csv'}

# answer_auto_mag = pd.read_csv('dataset/mag/mag_auto.csv')
# df_synthesized_all_split_mag = pd.read_csv("hf://datasets/snap-stanford/stark/" + splits["synthesized_all_split_mag"])
# create_quest_answer(df_synthesized_all_split_mag, answer_auto_mag, "mag_auto_qa.csv")
#
# answer_human_mag = pd.read_csv('dataset/mag/mag_human.csv')
# df_human_generated_eval_mag = pd.read_csv("hf://datasets/snap-stanford/stark/" + splits["humen_generated_eval_mag"])
# create_quest_answer(df_human_generated_eval_mag, answer_human_mag, "mag_human_qa.csv")
#
answer_auto_prime = pd.read_csv('dataset/prime/prime_auto_doc.csv')
df_synthesized_all_split_prime = pd.read_csv("hf://datasets/snap-stanford/stark/" + splits["synthesized_all_split_prime"])
create_quest_answer(df_synthesized_all_split_prime, answer_auto_prime, "prime_auto_qa.csv")
#
# answer_human_prime = pd.read_csv('dataset/prime/prime_human_doc.csv')
# df_human_generated_eval_prime = pd.read_csv("hf://datasets/snap-stanford/stark/" + splits["humen_generated_eval_prime"])
# create_quest_answer(df_human_generated_eval_prime, answer_human_prime, "prime_human_qa.csv")

# CRAG
# df = pd.read_json('crag_task_1_and_2_dev_v4.jsonl', lines=True)
#
# print(df.columns)
# print(df.head(5))






















