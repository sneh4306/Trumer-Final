import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

def get_accuracy(filename,tweet_text,save_filename):  
  stoplist = set(stopwords.words('english'))
  data = pd.read_csv(filename)
  tweets = data["text"]
  verified_status = data["isVerified"]
  verified_status = list(verified_status)
  tweets = list(tweets)
  for i in range(len(tweets)):
    tweets[i] = tweets[i].split("…")[0]
    tweets[i] = tweets[i].split("http")[0]

  related_target = []
  related_text=[]
  related_sim=[]
  verified_list = []
  related_dict={}
  unrelated = []
  for i in range(len(tweets)):
    x = tweet_text#"Thrilled to see so much excitement for AirPods Pro all around the world. You are going to love them."
    y = tweets[i]
    verif = verified_status[i]

    x_list = [word for word in x.lower().split() if word not in stoplist]
    y_list = [word for word in y.lower().split() if word not in stoplist]

    x = " ".join(x_list)
    y = " ".join(y_list)
    sim = get_cosine_sim(x, y)[0][1]
    if sim > 0.0:
      related_target.append(tweet_text)
      related_text.append(y)
      related_sim.append(sim)
      verified_list.append(verif)
    else :
      unrelated.append([tweet_text,y,sim])
    #print(i, get_cosine_sim(x, y)[0][1])
  #print(related)
  related_dict['target']=related_target
  related_dict['text'] = related_text
  related_dict['similarity_score'] = related_sim
  related_dict['isVerified'] = verified_list
  id_list = data["id"]
  related_df = pd.DataFrame(related_dict)
  print("created dataframe")
  related_df.to_csv("related_2.csv")
  
def get_cosine_sim( * strs):
  vectors = [t
    for t in get_vectors( * strs)
  ]
  return cosine_similarity(vectors)

def get_vectors( * strs):
  text = [t
    for t in strs
  ]
  vectorizer = CountVectorizer(text)
  vectorizer.fit(text)
  return vectorizer.transform(text).toarray()


#nltk.download('stopwords')
