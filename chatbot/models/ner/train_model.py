# 쳇봇엔진 - NER모델작성
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import preprocessing
from sklearn.model_selection import train_test_split
from chatbot.utils.Preprocess import Preprocess

# 1. 학습파일로딩
def read_file(file_name):
    sents = []
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx + 1][0] == '$':
                this_sent = []
            elif l[0] == '$' and lines[idx - 1][0] == ';':
                continue
            elif l[0] == '\n':
                sents.append(this_sent)
            else:
                this_sent.append(tuple(l.split()))
    return sents

p = Preprocess(word2index_dic="./chatbot/train_tools/dict/chatbot_dict.bin",
               userdic="./chatbot/utils/user_dic.tsv")

# 2. 학습용말뭉치데이터 로딩
corpus = read_file('./chatbot/models/ner/ner_train.txt')

# 3. 말뭉치데이터에서 단어(2번쨰), BIO태그(4번째)만 로딩해서 학습용데이터셋을 생성
sentences, tags = [], []
for t in corpus:
    tagged_sentence = []
    sentence, bio_tag = [], []
    for w in t:
        tagged_sentence.append((w[1], w[3]))
        sentence.append(w[1])
        bio_tag.append(w[3])
    
    sentences.append(sentence)
    tags.append(bio_tag)
    
print("샘플 크기 : \n", len(sentences))
print("0번 째 샘플 단어 시퀀스 : \n", sentences[0])
print("0번 째 샘플 bio 태그 : \n", tags[0])
print("샘플 단어 시퀀스 최대 길이 :", max(len(l) for l in sentences))
print("샘플 단어 시퀀스 평균 길이 :", (sum(map(len, sentences))/len(sentences)))    

# 4. 토크나이저 정의 
# 단어시퀀스는 Preprocess객체에서 생성하기 때문에 예제에서는 BIO태그용 토크나이저 객체만 생성
tag_tokenizer = preprocessing.text.Tokenizer(lower=False) # 태그 정보는 lower=False 소문자로 변환하지 않는다.
tag_tokenizer.fit_on_texts(tags)

# 단어사전 및 태그 사전 크기
vocab_size = len(p.word_index) + 1
tag_size = len(tag_tokenizer.word_index) + 1
print("BIO 태그 사전 크기 :", tag_size)
print("단어 사전 크기 :", vocab_size)

# 5. 학습용단어시퀀스생성
# BIO태그는 토크나이저에서 생성된 사전데이터를 시퀀스번호형태로 인코딩한다.
x_train = [p.get_wordidx_sequence(sent) for sent in sentences]
y_train = tag_tokenizer.texts_to_sequences(tags)

index_to_ner = tag_tokenizer.index_word # 시퀀스 인덱스를 NER로 변환 하기 위해 사용
index_to_ner[0] = 'PAD'

# 6. 시퀀스 패딩 처리
# 개체명인식모델의 입출력크기를 동일하게 맞추기위해 시퀀스 패딩작업을 진행
# 벡터크기를 단어 시퀀스의 평균길이보다 여유있게 40으로 정의
max_len = 40
x_train = preprocessing.sequence.pad_sequences(x_train, padding='post', maxlen=max_len)
y_train = preprocessing.sequence.pad_sequences(y_train, padding='post', maxlen=max_len)

# 7. 학습 데이터와 테스트 데이터를 8:2의 비율로 분리
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train,
                                                    test_size=.2,
                                                    random_state=1234)

# 8. 출력 데이터를 one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=tag_size)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=tag_size)

print("학습 샘플 시퀀스 형상 : ", x_train.shape)
print("학습 샘플 레이블 형상 : ", y_train.shape)
print("테스트 샘플 시퀀스 형상 : ", x_test.shape)
print("테스트 샘플 레이블 형상 : ", y_test.shape)

# 9. 모델정의(Bi-LSTM)
# tag_size만큼 출력 뉴런에서 제일 확률 높은 출력값 1개를 선택하기 위해 활성화함수로 softmax를 사용
# 손실함수는 categorical_crossentropy를 사용
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam

model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=30, input_length=max_len, mask_zero=True))
model.add(Bidirectional(LSTM(200, return_sequences=True, dropout=0.50, recurrent_dropout=0.25)))
model.add(TimeDistributed(Dense(tag_size, activation='softmax')))
model.compile(loss='categorical_crossentropy', optimizer=Adam(0.01), metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=128, epochs=10)

print("평가 결과 : ", model.evaluate(x_test, y_test)[1])
model.save('./chatbot/models/ner/ner_model.keras')

# 10. 시퀀스를 NER태그로 변환
# 예측값을 index_to_ner함수를 사용해서 태깅정보로 변경하는 함수
def sequences_to_tag(sequences):
    result = []
    for sequence in sequences: # 전체 시퀀스에서 시퀀스를 하나씩 꺼내기
        temp = []
        for pred in sequence:  # 시퀀스로 부터 예측값을 하나씩 꺼낵;
            pred_index = np.argmax(pred) # [0,0,1,...]라면 1의 위치인 2를 리턴
            temp.append(index_to_ner[pred_index].replace('PAD', 'O')) # 품사태그 PAD를 O로 변경
        result.append(temp)
    return result

# 11. 테스트데이터셋의 NER예측
# 1) f1_sre를 계산하기 위한 모듈 import
#    f1_score계산을 위해 predict()함수를 사용
from seqeval.metrics import f1_score, classification_report

# 2) 테스트데이터셋으로 예측
#    x_test(테스트용데이터셋)는 시퀀스번호로 인코딩된 데이터(단어시퀀스, numpy배열)
#    테스트한 결과로 예측된 NER태그정보가 담긴 넘파이배열을 리턴
y_predicted = model.predict(x_test)
pred_tags = sequences_to_tag(y_predicted) # 예측된 개체인식명(NER)
test_tags = sequences_to_tag(y_test)      # 실제 개체인식명

# 3) f1 평가결과
#    classification_report함수로 NER태그별로 계산된 정밀도, 재현율, f1-score를 출력
print(classification_report(test_tags, pred_tags))
print(f'f1 score : {f1_score(test_tags, pred_tags):.2%}')
