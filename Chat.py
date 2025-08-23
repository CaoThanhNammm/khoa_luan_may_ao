from LLM.Cohere import CohereChatBot
from LLM.GPT import GPT
from LLM.Gemini import Gemini
import LLM.prompt as prompt
from LLM.Llama import Llama
from dotenv import load_dotenv
from Validator import Validator
from knowledge_graph.create_entities_relationship_kb import pre_processing
load_dotenv()
import os
import torch
from langchain_core.prompts import PromptTemplate


class Chat:
    def __init__(self, t, qdrant, neo4j, pre_processing, document_id):
        self.t = t
        self.question = ''
        self.pre_processing = pre_processing
        self.reference = []
        self.extract = ""
        self.feedback = ""
        self.answer = ""
        self.more_info = ""
        self.new_question = ""
        self.reference_final = []
        self.entities = []
        self.relations = []
        self.len_ans = 0
        self.document_id = document_id

        # 1. khởi tạo gemini và chat
        model_name_15_flash = os.getenv('MODEL_15_FLASH')
        model_name_20_flash = os.getenv('MODEL_20_FLASH')
        model_name_25_flash = os.getenv('MODEL_25_FLASH')

        api_key_agent = os.getenv('API_KEY_AGENT')
        api_key_generator = os.getenv('API_KEY_GENERATOR')
        api_key_valid = os.getenv('API_KEY_VALID')
        api_key_commentor = os.getenv('API_KEY_COMMENTOR')

        self.gemini_agent = Gemini(model_name_25_flash, api_key_agent)
        self.gemini_generator = Gemini(model_name_20_flash, api_key_generator)
        self.gemini_valid = Gemini(model_name_15_flash, api_key_valid)
        self.gemini_commentor = Gemini(model_name_15_flash, api_key_commentor)

        self.qdrant = qdrant
        self.neo = neo4j

        api_key_01 = os.getenv("API_KEY_NVIDIA_01")
        api_key_02 = os.getenv("API_KEY_NVIDIA_02")
        api_key_03 = os.getenv("API_KEY_NVIDIA_03")
        api_key_04 = os.getenv("API_KEY_NVIDIA_04")

        model_llama_405b = os.getenv("MODEL_LLAMA_405B")

        self.llama3_1_commentor = Llama(api_key_01, model_llama_405b)
        self.llama3_1_generator = Llama(api_key_02, model_llama_405b)
        self.llama3_1_graph = Llama(api_key_03, model_llama_405b)
        self.llama3_1_summary = Llama(api_key_04, model_llama_405b)

        self.cohere_agent = CohereChatBot()
        self.cohere_generator = CohereChatBot()
        self.cohere_valid = CohereChatBot()
        self.cohere_commentor = CohereChatBot()

        self.gpt_agent = GPT("gpt-5-mini")
        self.gpt_generator = GPT("gpt-5-nano")
        self.gpt_valid = GPT("gpt-5-nano")
        self.gpt_commentor = GPT("gpt-5-mini")
        self.gpt_summary = GPT("gpt-5-nano")
        self.gpt_graph = GPT("gpt-5-nano")

        self.validator_512 = Validator(qdrant.get_model_512())
        self.validator_768 = Validator(qdrant.get_model_768())
        self.validator_1024 = Validator(qdrant.get_model_1024())

        print('Initialize Chat success')

    def answer_by_context(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.answer_by_context()
        )
        formatted_prompt = prompt_template.format(question=self.question)

        return self.gemini_agent.generator(formatted_prompt)

    def answer_s2s(self):
        self.extract = ""
        self.feedback = ""
        self.new_question = ""
        self.reference = ""
        self.reference_final.clear()

        print(f'question: {self.question}')
        for t in range(self.t):
            print(f"Step {t}, initial feedback: {self.feedback}")
            self.new_question = ""
            self.reference = ""
            self.reference_final.clear()

            self.extract = self.agent()
            print(f'extract: {self.extract}')

            for question in self.extract.values():
                self.new_question += f"{question}, "

            print(f"new question: {self.new_question}")
            reference_retrieval = self.retrieval_graph()
            self.reference = str(reference_retrieval)
            self.reference_final = reference_retrieval
            print(f"Available references: {self.reference}")

            self.more_info = self.retrieval_text()
            self.reference_final.extend(self.more_info)
            print(f"more_info: {self.more_info}")

            self.answer = self.generator()
            print(f"answer: {self.answer}")

            if len(self.reference_final) != 0 or len(self.more_info) != 0:
                validator = self.valid()
                print(f"valid: {validator}")

                if "yes" in validator:
                    return self.summary_answer()

            self.feedback = self.commentor()
        return self.summary_answer()

    def answer_s2s_stsv(self):
        self.document_id = 'so_tay_sinh_vien_2024'
        self.extract = ""
        self.feedback = ""
        self.reference = ""
        self.new_question = ""
        self.reference_final.clear()

        print(f'question: {self.question}')
        for t in range(self.t):
            print(f"Step {t}, initial feedback: {self.feedback}")
            self.new_question = ""
            self.reference = ""
            self.reference_final.clear()

            self.extract = self.agent()
            print(f'extract: {self.extract}')

            for question in self.extract.values():
                self.new_question += f"{question}, "
            print(f"new question: {self.new_question}")

            reference_retrieval = self.retrieval_graph_stsv()
            self.reference = str(reference_retrieval)
            self.reference_final = reference_retrieval
            print(f"Available references: {self.reference}")

            self.more_info = self.retrieval_text()
            self.reference_final.extend(self.more_info)
            print(f"more_info: {self.more_info}")

            self.answer = self.generator()
            print(f"answer: {self.answer}")

            if len(self.reference_final) != 0 or len(self.more_info) != 0:
                validator = self.valid()
                print(f"valid: {validator}")

                if "yes" in validator:
                    return self.summary_answer()

            self.feedback = self.commentor()
        return self.summary_answer()

    def answer_prime(self):
        self.extract = ""
        self.feedback = ""

        print(f'question: {self.question}')
        for t in range(self.t):
            print(f"Step {t}, initial feedback: {self.feedback}")
            self.reference.clear()

            relationship, action = self.agent_prime()  # knowledge graph or text documents

            print(f'Relationship: {relationship}')
            print(f'Action: {action}')

            documents = self.retrieval_bank_prime(action, relationship)

            self.reference.append(documents)

            self.answer = f"{self.generator_prime()}"
            print(f"Answer: {self.answer}")

            validator = self.valid_prime()
            print(f"valid: {validator}")

            if "yes" in validator:
                self.entities.clear()
                self.relations.clear()
                return self.summary_answer_prime()

            self.feedback = self.commentor_prime()
            self.entities.clear()
            self.relations.clear()

        return self.summary_answer_prime()

    def agent_prime(self):
        agent = self.first_decision_prime() if not self.feedback else self.reflection_prime()
        print(f"Agent: {agent}")
        agent = pre_processing.string_to_json(agent)

        return agent["relationship"], agent["action"]

    def first_decision_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.first_decision_prime()
        )

        formatted_prompt = prompt_template.format(question=self.question)
        # return self.gemini_agent.generator(formatted_prompt).lower()
        # self.llama3_1_graph.set_prompt(formatted_prompt)
        # return self.llama3_1_graph.generator().lower()
        return self.cohere_agent.chat(formatted_prompt).lower()

    def reflection_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "feedback"],
            template=prompt.self_reflection_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, feedback=self.feedback)
        return self.cohere_agent.chat(formatted_prompt).lower()

    def summary_answer(self):
        prompt_template = PromptTemplate(
            input_variables=['question', 'answer'],
            template=prompt.summary_answer()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=str(self.answer))
        return self.gpt_summary.ask(formatted_prompt)

    def summary_answer_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", 'answer'],
            template=prompt.summary_answer_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=self.answer)
        return self.gpt_summary.ask(formatted_prompt)

    def agent(self):
        agent = self.first_decision() if not self.feedback else self.reflection()
        return pre_processing.string_to_json(agent)

    def retrieval_bank_stsv(self, action):
        return self.retrieval_graph_stsv() if 'graph' in action else self.retrieval_text()

    def retrieval_bank(self, action):
        return self.retrieval_graph() if 'graph' in action else self.retrieval_text()

    def retrieval_bank_prime(self, action, relationship):
        return self.retrieval_graph_prime(relationship) if 'knowledge graph' in action else self.retrieval_text_prime(
            relationship)

    def retrieval_graph_prime(self, relationship):
        res = ""
        for relation in relationship:
            head_type = relation["head_type"]
            head_name = str(relation["head"]).replace("'", "").replace('"', "")

            query = f"""
            MATCH p=(a)-[r]-(b)
            WHERE a.name CONTAINS '{head_name}'
            RETURN p
            LIMIT 20
            """.strip()

            print('query:', query)
            e, r, triplets = self.neo.run_cypher(query)

            self.entities.extend(e)
            self.relations.extend(r)
            res += str(triplets)

        return res

    def retrieval_graph(self):
        # llm dự đoán câu hỏi thuộc phần nào để thu hẹp nội dung cần truy xuất
        prompt_template = PromptTemplate(
            input_variables=["question", "document_id", "parts_of_document"],
            template=prompt.predict_question_belong_to()
        )
        formatted_prompt = prompt_template.format(question=self.question, document_id=self.document_id,
                                                  parts_of_document=self.neo.get_part_of_document(self.document_id))
        res = self.gpt_graph.ask(formatted_prompt)
        res = self.pre_processing.string_to_json(res)

        query = f"""
        MATCH (document:Document {{name: '{self.document_id}'}})-[*]->(predict:Part {{name: '{res['name']}'}})
        MATCH p=(predict)-[r*1..{res['level']}]->(e)
        RETURN p
        """
        print('query:', query)
        nodes, edges = self.neo.fetch_subgraph(query)

        # Tạo mapping node_id_to_idx trước
        node_id_list = list(nodes.keys())
        node_id_to_idx = {nid: i for i, nid in enumerate(node_id_list)}

        # Xác định thiết bị (GPU nếu có, ngược lại CPU)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Tạo edge_index và chuyển lên device
        edge_index = torch.tensor([
            [node_id_to_idx[edge["source"]] for edge in edges],
            [node_id_to_idx[edge["target"]] for edge in edges]
        ], dtype=torch.long).to(device)

        texts = [" ".join([f"{key} {value}" for key, value in dict(nodes[nid].items())['properties'].items()]) for nid
                 in node_id_list]
        return texts

    def retrieval_graph_stsv(self):
        # llm dự đoán câu hỏi thuộc phần nào để thu hẹp nội dung cần truy xuất
        prompt_template = PromptTemplate(
            input_variables=["question", "document_id"],
            template=prompt.predict_question_belong_to_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.new_question, document_id=self.document_id)
        res = self.gpt_graph.ask(formatted_prompt)
        res = self.pre_processing.string_to_json(res)

        query = f"""
        MATCH (document:Document {{name: '{self.document_id}'}})-[*]->(predict:{res["part"]} {{name: '{res['name']}'}})
        MATCH p=(predict)-[r*1..{res['level']}]->(e)
        RETURN p
        """
        print('query:', query)
        nodes, edges = self.neo.fetch_subgraph(query)

        # Tạo mapping node_id_to_idx trước
        node_id_list = list(nodes.keys())
        node_id_to_idx = {nid: i for i, nid in enumerate(node_id_list)}

        # Xác định thiết bị (GPU nếu có, ngược lại CPU)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Tạo edge_index và chuyển lên device
        edge_index = torch.tensor([
            [node_id_to_idx[edge["source"]] for edge in edges],
            [node_id_to_idx[edge["target"]] for edge in edges]
        ], dtype=torch.long).to(device)

        documents = [" ".join([f"{key} {value}" for key, value in dict(nodes[nid].items())['properties'].items()]) for
                     nid
                     in node_id_list]

        embed_question = self.neo.encode(self.new_question)
        embed_documents = self.neo.encode(documents)

        return self.neo.re_ranking(embed_question, embed_documents, documents, int(len(embed_documents) * 0.5))

    def retrieval_text(self):
        self.qdrant.set_collection_name(self.document_id)
        documents = self.qdrant.query_from_db(self.question)

        re_ranking_query_text = self.qdrant.re_ranking(self.question, documents)
        reference = []
        for i in range(len(re_ranking_query_text)):
            logit = re_ranking_query_text[i].metadata['relevance_score']
            text = re_ranking_query_text[i].page_content
            if logit > 0:
                reference.append(f'{text}\n')

        return reference

    def retrieval_text_prime(self, relationship):
        self.qdrant.set_collection_name(self.document_id)
        entities_topic = ""
        for relation in relationship:
            entities_topic += relation["head"]

        documents = self.qdrant.query_from_db_prime(entities_topic)

        re_ranking_query_text = self.qdrant.re_ranking(entities_topic, documents)
        reference = ""
        for i in range(len(re_ranking_query_text)):
            logit = re_ranking_query_text[i].metadata['relevance_score']
            text = re_ranking_query_text[i].page_content
            if logit > 0:
                reference += f'{text}\n'
        return reference

    def first_decision(self):
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt.first_decision()
        )
        formatted_prompt = prompt_template.format(question=self.question)
        return self.gpt_agent.ask(formatted_prompt).lower()

    def reflection(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "feedback", "answer"],
            template=prompt.self_reflection()
        )
        formatted_prompt = prompt_template.format(question=self.question, feedback=self.feedback,
                                                  answer=str(self.answer))
        return self.gpt_agent.ask(formatted_prompt).lower()

    def generator(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "references"],
            template=prompt.generator()
        )

        formatted_prompt = prompt_template.format(question=self.question,
                                                  references=f"{str(self.reference)}, {str(self.more_info)}")
        return self.gpt_generator.ask(formatted_prompt)

    def generator_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "document"],
            template=prompt.generator_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, document=str(self.reference))
        return self.gpt_generator.ask(formatted_prompt)

    def valid(self):
        val_512 = self.validator_512.evaluate(self.question, self.answer, self.reference_final)
        val_768 = self.validator_768.evaluate(self.question, self.answer, self.reference_final)
        val_1024 = self.validator_1024.evaluate(self.question, self.answer, self.reference_final)
        qa_mean = (val_512['QA_similarity'] + val_768['QA_similarity'] + val_1024['QA_similarity']) / 3
        qd_mean = (val_512['Q_in_D_max'] + val_768['Q_in_D_max'] + val_1024['Q_in_D_max']) / 3
        ad_mean = (val_512['A_in_D_max'] + val_768['A_in_D_max'] + val_1024['A_in_D_max']) / 3
        print(f"val_512: {val_512}")
        print(f"val_768: {val_768}")
        print(f"val_1024: {val_1024}")
        print(f"qa_mean: {qa_mean}\nqd_mean: {qd_mean}\nad_mean: {ad_mean}")

        prompt_template = PromptTemplate(
            input_variables=["question", "answer", "qa_mean", "reference" "qd_mean", "ad_mean"],
            template=prompt.valid_stsv()
        )
        formatted_prompt = prompt_template.format(question=self.question, answer=self.answer, reference=self.reference, qa_mean=qa_mean, qd_mean=qd_mean, ad_mean=ad_mean)

        return self.gpt_valid.ask(formatted_prompt).lower()

    def valid_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "document", "answer"],
            template=prompt.validator_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, document=self.reference,
                                                  answer=self.answer)
        return self.gpt_valid.ask(formatted_prompt).lower()

    def commentor(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "entities", "references"],
            template=prompt.commentor()
        )
        formatted_prompt = prompt_template.format(question=self.question, entities=self.extract,
                                                  references=self.reference)
        # return self.gemini_commentor.generator(formatted_prompt)
        return self.gpt_commentor.ask(formatted_prompt)

    def commentor_prime(self):
        prompt_template = PromptTemplate(
            input_variables=["question", "entities", "relations"],
            template=prompt.commentor_prime()
        )
        formatted_prompt = prompt_template.format(question=self.question, entities=self.entities,
                                                  relations=self.relations)

        # return self.gemini_commentor.generator(formatted_prompt)
        # self.llama3_1_commentor.set_prompt(formatted_prompt)
        # return self.llama3_1_commentor.generator()
        # return self.cohere_commentor.chat(formatted_prompt)

        return self.gpt_commentor.ask(formatted_prompt)

    def set_question(self, question):
        self.question = question

    def set_document_id(self, document_id):
        self.document_id = document_id
