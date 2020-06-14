#modules for flask model
from flask import Flask,request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from wtforms import Form
from flask.views import MethodView
from monkeylearn import MonkeyLearn

#for fetching related tweets
import tweepy
import pandas as pd
import itertools
import nltk
import sklearn
#nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'#only for MAC 
#for tense
from tense import tweet_tense

#for cosine similarity
from accuracy_cosine2 import get_accuracy

#for loading model
from fastai import *
from fastai.text import *

#for web scraping
import requests
from bs4 import BeautifulSoup
import re
import time
import lxml

#final model
import pickle
import json

import numpy as np
import tensorflow as tf
from sklearn import preprocessing
import matplotlib.pyplot as plt
import sys

app = Flask(__name__)
cors = CORS(app, resources={r"/find/": {"origins": "http://trumer.herokuapp.com"}})
api = Api(app)

consumer_key = "rMus7QVnwVo083dlmWhrPY5md"
consumer_secret = "tT8mBpKgmKPtsYUpG21Iuj5ihx0F5YruDm2cG97gWJgmLS70LM"
access_token = "3010011516-2ukydRKN2IWPeDIFzBTx26U7JxCPLdd8p5KsTrv"
access_token_secret = "i5XPTmZqrkenWI9l3jB9gqPbYsCnpfVzOcNdNOuu1U5jM"


x={}

def tweets_df(results,orig_tweet):
	#store tweet result in a dataframe
	id_list = [tweet.id for tweet in results]
	data_set = pd.DataFrame(id_list, columns=["id"])
	data_set["target"] = [orig_tweet for tweet in results]
	data_set["text"] = [tweet.text for tweet in results]
	data_set["created_at"] = [tweet.created_at for tweet in results]
	data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
	data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
	data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
	data_set["user_location"] = [tweet.author.location for tweet in results]
	data_set["Hashtags"] = [tweet.entities.get('hashtags') for tweet in results]
	data_set["isVerified"] = [tweet.author.verified for tweet in results]

	return data_set

def clean_ascii(text):
    # function to remove non-ASCII chars from data    
    return ''.join(i for i in text if ord(i) < 128)

def monkey_learn(tweet_text):
	print("inside monkey_learn")
	ml = MonkeyLearn('3a29f7db21c735f4ef5339fa181f915ac2acd063')
	model_id = 'ex_YCya9nrn'
	tweet_list = []
	tweet_list.append(tweet_text)
	keywords = []
	data_set_new = pd.DataFrame()

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	response = ml.extractors.extract(model_id, data=tweet_list)
	for resp in response.body:
		for extr in resp['extractions']:
			keywords.append(extr['parsed_value'])
	if '@' in keywords:
		keywords.remove("@")
	print(keywords)
	for i in range(len(keywords)):
		results=[]	
		for y in api.search(q= keywords[i]+" -filter:retweets", lang="en", count=100):
			results.append(y)
		data_set_new = pd.concat([data_set_new,tweets_df(results,tweet_text)],ignore_index=True)

	data_set_new.to_csv('tweets_extracted_ht.csv')

def proper_noun(sentence):
	tokens = nltk.word_tokenize(sentence)
	tagged_sent = nltk.pos_tag(tokens)
	propernouns = [word for word,pos in tagged_sent if pos == 'NNP']	
	if(len(propernouns)==0):
		return False
	else:
		return True

def fetch_hashtags(tweet_text):
	#fetch tweets based on hashtags
	init_hashtags = []
	print("Inside fetch hashtags")

	tweet = tweet_text
	print(tweet)
	words = tweet.split(" ")
	#Extracting Hashtags
	for w in words:
		tags = w.split("#")
		if len(tags)==1:
			continue
		else:
			init_hashtags = init_hashtags + tags[1:]
	print(init_hashtags)
	#Extracting Proper Nouns
	print("Extracting Proper Nouns")
	tokens = nltk.word_tokenize(tweet)
	print(tokens)
	pos_tags = nltk.pos_tag(tokens)
	print(pos_tags)
	for x in pos_tags:
	  if x[1] == "NNP":
	    init_hashtags.append(x[0])

	init_hashtags.sort()
	init_hashtags = list(init_hashtags for init_hashtags,_ in itertools.groupby(init_hashtags))
	print("reached")
	if "@" in init_hashtags:
		init_hashtags.remove("@")
	print(init_hashtags)
	print("done")

	results = []
	hashtags = []
	tweets = []
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	#Getting Initial Set of Tweets
	for x in init_hashtags:		
		for tweet in api.search(q=x+" -filter:retweets", lang="en", count=100):
			results.append(tweet)
			for x in tweet.entities.get('hashtags'):
				hashtags.append(x['text'])	
	data_set = tweets_df(results,tweet_text)
	
	hashtag_freq = {}
	for x in hashtags:
		if x in hashtag_freq.keys():			
			hashtag_freq[x] += 1
		else:
			hashtag_freq[x] = 1

	data_set_new = pd.DataFrame()

	for x in hashtag_freq.keys():
		results_ = []		
		if(hashtag_freq[x] > 2):
			for y in api.search(q=x+" -filter:retweets", lang="en", count=50):
				results_.append(y)
			data_set_new = pd.concat([data_set_new,tweets_df(results_,tweet_text)],ignore_index=True)

	data_set_new.to_csv('tweets_extracted_ht.csv')

def get_results(data):
	# Load Model
	loaded_model = tf.keras.models.Sequential()
	output_dim = 8
	# Input Layer
	loaded_model.add(tf.keras.layers.Dense(output_dim, input_dim=8, activation='relu'))
	# Hidden Layers
	loaded_model.add(tf.keras.layers.Dense(output_dim, activation='relu'))
	loaded_model.add(tf.keras.layers.Dense(output_dim, activation='relu'))
	loaded_model.add(tf.keras.layers.Dense(output_dim, activation='relu'))
	loaded_model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
	# load weights into new model
	# loaded_model.load_weights("model_nn_final.h5")
	loaded_model.load_weights("model_SMOTE.h5")

	# evaluate loaded model on test data
	loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

	#loaded_model = pickle.load(open('model_SMOTE.h5', 'rb'))
	tweet = data

	max_followers_count = 22720218
	min_followers_count = 4
	min_retweet_count = 1
	max_retweet_count = 51951
	min_verified_in_support = 0
	max_verified_in_support = 14
	min_verified_in_deny = 0
	max_verified_in_deny = 7
	min_support = 0
	max_support = 81
	min_deny = 0
	max_deny = 92
	# min_neutral = 0
	# max_neutral = 227

	followers_count = int(tweet["followers"])
	if tweet["isVerified"] == False:
		verified = 0
	else:
		verified = 1
	print("retweet count")
	print(type(tweet["retweet_count"]))
	retweet_count = int(tweet["retweet_count"].replace(",",""))
	verified_in_support = int(tweet["verifiedInFor"])
	verified_in_deny = int(tweet["verifiedInAgainst"])
	print("support")
	print(type(tweet["FOR"]))
	support = int(tweet["FOR"])
	deny = int(tweet["AGAINST"])
	# neutral = int(tweet["NONE"])
	if tweet["tense"] == "PAST TENSE":
		tense = 0
	elif tweet["tense"] == "PRESENT TENSE":
		tense = 0.5
	else:
		tense = 1

	followers_count = (followers_count - min_followers_count) / (max_followers_count - min_followers_count)
	retweet_count = (retweet_count - min_retweet_count) / (max_retweet_count - min_retweet_count)
	verified_in_support = (verified_in_support - min_verified_in_support) / (max_verified_in_support - min_verified_in_support)
	verified_in_deny = (verified_in_deny - min_verified_in_deny) / (max_verified_in_deny - min_verified_in_deny)
	support = (support - min_support) / (max_support - min_support)
	deny = (deny - min_deny) / (max_deny - min_deny)
	# neutral = (neutral - min_neutral) / (max_neutral - min_neutral)

	test = np.array([np.array([followers_count, verified, retweet_count, verified_in_support, verified_in_deny, support, deny, tense])])
	c = loaded_model.predict(test)
	p = loaded_model.predict_classes(test)
	#print("Tweet:",tweet)
	#print("Probability:",p[0][1])
	#print("Class:",c)
	print("Tweet:",tweet)
	print("Probability:",c)
	print("Class:",p)
	tf.keras.backend.clear_session()
	return str(c[0][0])

class Trumer(Resource):
	def post(self):
		""" return final probability for tweet"""
		url= request.form['tweet']
		print("recieved: "+url)

		#page = requests.get(url)
		#print(page.text)		
		#soup = bs4.BeautifulSoup(page.content, 'html.parser')
		#print(soup.prettify())
		#print(list(soup.children))
		#print(type(soup))
		#title = soup.title.text
		#print(title)
		#text = re.sub(r'^https?:\/\/.*[\r\n]*', '', title, flags=re.MULTILINE)
		#tweet=text.split('"')
		#print(tweet)
		#orig_tweet=tweet[1]		
		#print(orig_tweet)
		# try:
		# 	retweets = soup.find('li', {'class': 'js-stat-count js-stat-retweets stat-count'}).find('a').get('data-activity-popup-title')
		# 	print(retweets.split()[0])
		# 	retweets = retweets.split()[0]
		# except:
		# 	retweets = 0
		# 	print(retweets)
		
		t=url.split("/")
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)

		tweet = api.get_status(t[5])
		orig_tweet=tweet.text
		retweets=str(tweet.retweet_count)
		followers_count=str(tweet.user.followers_count)
		verified=tweet.user.verified
		following_count=str(tweet.user.friends_count)

		#t_final = t[0]+"//"+t[2]+"/"+t[3]

		
		if("#" in orig_tweet  or proper_noun(orig_tweet)):
			print("Using Hashtag Method")
			fetch_hashtags(orig_tweet)
		else:
			print("Using monkeylearn")
			monkey_learn(orig_tweet)

		get_accuracy("tweets_extracted_ht.csv",orig_tweet,"related_2.csv")		
		model_path = "models/vocab.pkl"
		data_clas_path = "train_test_predicted_data/train.csv"
		learn_path = "models/final_learn_model"
		test_data_path = "related_2.csv"
		cwd = os.getcwd()

		vocab_load = pickle.load(open(os.path.join(cwd, model_path), 'rb'))
		data_clas = TextClasDataBunch.from_csv('', os.path.join(cwd, data_clas_path), vocab=vocab_load, min_freq=7, bs=64)
		learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
		learn = learn.load(os.path.join(cwd, learn_path))
		
		test_data = pd.read_csv(os.path.join(cwd, test_data_path), delimiter=",")
		test_data["text"] = test_data['text'].apply(clean_ascii)		
		input_data = test_data[['target', 'text','isVerified']]
		input_data['Stance'] = input_data['text'].apply(lambda row: str(learn.predict(row)[0]))
		
		objects = input_data[['Stance']].Stance.unique()
		print(type(objects))
		y_pos = np.arange(len(objects))
		print(type(y_pos))
		perf = []
		for i in range(len(objects)):
			perf.append(int(input_data['Stance'].value_counts()[i]))
		performance = perf
		print(type(perf[0]))
		print("processing done")

		file_to_save="predicted.tsv"
		input_data.to_csv(file_to_save, sep='\t', index=True,header=['Target', 'Tweet', 'isVerified','Stance'], index_label='ID')

		verifiedInFor = 0
		verifiedInAgainst = 0

		for index,row in input_data.iterrows():
			if(row["Stance"] == "FOR" and row["isVerified"]):
				verifiedInFor += 1
			if(row["Stance"] == "AGAINST" and row["isVerified"]):
				verifiedInAgainst += 1

		print(verifiedInFor)
		print(verifiedInAgainst)
		
		global x
		x["input_tweet"]=orig_tweet

		
		#print(t[3])

		# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
		# auth.set_access_token(access_token, access_token_secret)
		# api = tweepy.API(auth)
		# verified = api.get_user(t[3]).verified
		x["isVerified"] = verified

		# temp = requests.get(t_final)
		# bs = BeautifulSoup(temp.text,'lxml')
		
			# follow_box = bs.find('li',{'class':'ProfileNav-item ProfileNav-item--followers'})
			# follow_box1 = bs.find('li',{'class':'ProfileNav-item ProfileNav-item--following'})
			# followers = follow_box.find('a').find('span',{'class':'ProfileNav-value'})
			# following = follow_box1.find('a').find('span',{'class':'ProfileNav-value'})
		x["followers"]=followers_count
		x["following"]=following_count
		print(x["following"]+"\n"+x["followers"])
		#except:
		#	print('Account name not found...')
		
		x["tense"] = tweet_tense(orig_tweet)
		objects = objects.tolist()
		for i in range(len(objects)):
			x[objects[i]] = perf[i]

		x["retweet_count"] = retweets
		x["verifiedInFor"] = verifiedInFor
		x["verifiedInAgainst"] = verifiedInAgainst

		#final model
		x["probability"] = get_results(x)
		
		# with open('result.json', 'w') as f:
		#     json.dump(x, f)

		x["stance_labels"] = objects#.tolist()
		x["stance_count"] = perf
		print("Probability:",x["probability"])
		y=json.dumps(x)
		z=json.loads(y)
		return z

api.add_resource(Trumer, '/find/')

@app.route('/')
def home_page():
	return render_template('index.html');

@app.route('/results')
def result_page():
	username = request.args.get('username')
	tweet_id = request.args.get('id')
	if username == None:
		return render_template('result_page.html', paramters=False)
	else:
		return render_template('result_page.html', parameters=True, username=username, tweetId=tweet_id)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)





