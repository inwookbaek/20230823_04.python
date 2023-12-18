# 답변검색모듈

class FindAnswer:
    
    def __init__(self, db):
        self.db = db
        
    # 검색 sql생성
    def make_query(self, intent_name, ner_tags):
        sql = "select * from chatbot_train_data "
        if intent_name != None and ner_tags == None:
            sql = sql + f" where intent = '{intent_name}'"
            
        elif intent_name != None and ner_tags != None:
            where = f" where intent = '{intent_name}'"
            if(len(ner_tags) > 0):
                where += " and ("
                for ne in ner_tags:
                    where += f" ner like '%{ne}%' or "
                where = where[:-3] + ")"
                
            sql = sql + where
        
        # 동일한 답변이 2개이상인 경우, 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        
        return sql
        
    # 답변검색
    # 의도명(intent_name)과 태그리스트(ner_tags)를 이용해서 질문의 답변을 검색하는 메서드
    def search(self, intent_name, ner_tags):
        
        # 의도명, 개체인식명으로 답변을 검색
        sql = self.make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)
        
        # 검색되는 답변이 없을 경우 의도명만 검색
        if answer is None:
            sql = self.make_query(intent_name, None)
            answer = self.db.select_one(sql)
            
        return(answer['answer'], answer['answer_image'])
   
    # NER태그를 실제로 입력된 단어로 변환하는 함수
    # 질물 : 탕수육 대자로 한개 주문할게요 -> 개체인식명 탕수육 B_FOOD으로 처리
    # 답변 : {B_FOOD} 주문 처리 완료되었습니다. 주문해주셔서 감사합니다.
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:
            
            # 변환해야 하는 태그가 있는 경우 추가
            if tag == 'B_FOOD' or tag == 'B_DT' or tag == 'B_TI':
                answer = answer.replace(tag, word)
                
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
