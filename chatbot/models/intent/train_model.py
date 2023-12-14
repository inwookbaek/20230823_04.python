# 쳇봇엔진-의도분류모델
import pandas as pd
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate

# 1. 데이터로딩
train_file = './chatbot/models/intent/total_train_data.csv'
data = pd.read_csv(train_file, delimiter=",")
queries = data['query'].tolist()
intents = data['intent'].tolist()

# 2. 단어시퀀스사전로딩
from chatbot.utils.Preprocess import Preprocess
p = Preprocess(word2index_dic="./chatbot/train_tools/dict/chatbot_dict.bin",
               userdic="./chatbot/utils/user_dic.tsv")

# 3. 단어시퀀스 생성
sequences = []
for sentence in queries:
    pos = p.pos(sentence)
    keywords = p.get_keywords(pos, without_tag=True)
    seq = p.get_wordidx_sequence(keywords)
    sequences.append(seq)
    
# 4. 단어인덱스시퀀스벡터생성
# Preprocess에서 생성한 시퀀스벡터의 크기를 동일하게 처리하기 위해 
# MAX_SEQ_LEN=15 즉 최대 벡터크기를 15로 설정하고 15이하인 벡터는 padding처리
from chatbot.config.GlobalParams import MAX_SEQ_LEN
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')
print(padded_seqs.shape, len(intents))
print()

# 5. 학습용, 검증용, 테스트용 데이터셋 생성 - 7:2:1
# 패딩처리된 시퀀스(padded_seqs)리스트와 의도(intents)리스트를 데이터셋으로 생성후
# 랜덤하게 학습용,검증용,테스트용 데이터셋을 7:2:1로 분할
ds = tf.data.Dataset.from_tensor_slices((padded_seqs, intents))
df = ds.shuffle(len(queries))

train_size = int(len(padded_seqs) * 0.7)
val_size = int(len(padded_seqs) * 0.2)
test_size = int(len(padded_seqs) * 0.1)

train_ds = ds.take(train_size).batch(20)
val_ds = ds.skip(train_size).take(val_size).batch(20)
test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

# 6. 하이퍼파라미터설정
dropout_prob = 0.5
EMB_SIZE = 128
EPOCH = 5
VOCAB_SIZE = len(p.word_index) + 1 

# 7. CNN모델정의
input_layer = Input(shape=(MAX_SEQ_LEN, ))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

conv1 = Conv1D(filters=128, kernel_size=3, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool1 = GlobalMaxPool1D()(conv1)
conv2 = Conv1D(filters=128, kernel_size=4, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool2 = GlobalMaxPool1D()(conv2)
conv3 = Conv1D(filters=128, kernel_size=5, padding='valid', activation=tf.nn.relu)(dropout_emb)
pool3 = GlobalMaxPool1D()(conv3)

# 1) 3,4,5-gram 출력층을 한개로 합치기
concat = concatenate([pool1, pool2, pool3])

# 2) 은닉층
hidden = Dense(128, activation=tf.nn.relu)(concat)
dropout_hidden = Dropout(rate=dropout_prob)(hidden)
logits = Dense(5, name='logits')(dropout_hidden)
predictions = Dense(5, activation=tf.nn.softmax)(logits)

# 8. CNN모델생성
# 정의된 모델을 케라스모델에 추가, Model()함수는 입력층과 출력층만 사용
model = Model(inputs=input_layer, outputs=predictions)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 9. 모델학습
model.fit(train_ds, validation_data=val_ds, epochs=EPOCH, verbose=1)

# 10. 모델평가
loss, accuracy = model.evaluate(test_ds, verbose=1)
print(f'Accuracy : {accuracy*100:.2f}')
print(f'Loss     : {loss:.2f}')

# 11. 모델저장
model.save('./chatbot/models/intent/intent_model.keras')
