import pandas as pd
from social_sites_data.twitter import get_twitter_text
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding

def predict_sentiment(text,tokenizer,model,sentiment_label):
    tw = tokenizer.texts_to_sequences([text])
    tw = pad_sequences(tw,maxlen=200)
    prediction = int(model.predict(tw).round().item())
    if(sentiment_label[1][prediction]=="positive"):
        return 1
    else:
        return 0


def my_sentiment_analyser(df,tokenizer,model,sentiment_label):
    count=df.shape[0]
    localrate=0
    for singleTweet in df['Tweet']:
        res = predict_sentiment(singleTweet,tokenizer,model,sentiment_label)
        localrate+=res

    ans=localrate/count
    return ans*100/20



def trainAndAnalyse(mylist,s):
    
    df = pd.read_csv("Sample/Tweets.csv")
    tweet_df = df[['text','airline_sentiment']]
    tweet_df = tweet_df[tweet_df['airline_sentiment'] != 'neutral']

    sentiment_label = tweet_df.airline_sentiment.factorize()
    tweet = tweet_df.text.values
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(tweet)
    vocab_size = len(tokenizer.word_index) + 1
    encoded_docs = tokenizer.texts_to_sequences(tweet)
    padded_sequence = pad_sequences(encoded_docs, maxlen=200)

    embedding_vector_length = 32
    model = Sequential() 
    model.add(Embedding(vocab_size, embedding_vector_length, input_length=200) )
    model.add(SpatialDropout1D(0.25))
    model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid')) 
    model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])  

    history = model.fit(padded_sequence,sentiment_label[0],validation_split=0.2, epochs=5, batch_size=32)
    print("\n\n\n\n#######################  DONE  #######################\n\n\n\n")

    for i in mylist:
#        print(i)
        df=get_twitter_text("'"+s+"' '"+i+"'")
        print(df.shape[0])
        if df.shape[0]<10:
            continue
        print("twitter rating: ",i,str(my_sentiment_analyser(df,tokenizer,model,sentiment_label))+"/5")
        #for facebook
        #for Quora

    df=get_twitter_text(s)
    if df.shape[0]>10:
        print("twitter rating: ",s,str(my_sentiment_analyser(df,tokenizer,model,sentiment_label))+"/5")





