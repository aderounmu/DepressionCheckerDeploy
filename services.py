####SERVICES#####

import json
from AI.AImodel import AImodel 
import pandas as pd
import twint
import time

class noUser(Exception):
	pass

class services:
	def __init__(self,username=None,text=None):
		self.username = username
		self.text = text 
		self.tweets = None
		self.result = None 
		pass

	def getTweets(self,recent=False):
		c = twint.Config()
		c.Username = self.username
		c.Limit = 2000
		c.Pandas = True
		# c.Store_object = True saves to ram 
		c.Hide_output = True
		twint.run.Search(c)

		#data = twint.output.tweets_list len(data['id'])
		data_df = twint.storage.panda.Tweets_df
		data = data_df.to_dict()
		data = [data_df.loc[x].to_dict() for x in range(data_df.shape[0])]

		if len(data) == 0:
			raise noUser()
		if recent:
			self.tweets = data[0]
		else: 
			self.tweets =data
			# self.tweets.extend(twint.output.tweets_list)
		pass

	def predict(self):
		model = AImodel.loadModel('AI/Depression_model.h5')
		if self.username is None:
			if self.text is None:
				return {'error':' No text inputed '} #raise error
			else:
				texts = self.text 
				texts = AImodel.preprocessor(texts)
		else:
			texts = [str(tweet['tweet'].encode(encoding='UTF-8')) for tweet in self.tweets ]
			texts = list(map(AImodel.preprocessor,texts))
			pass
		token = AImodel.tokenize(texts, train=False,tokenpath='AI/tokenizer.json')
		self.result = AImodel.predict(texts,token,model)
		

	def response(self):
		if self.text != None:
			data = self.result
			return json.dumps({"data":data})
		elif self.tweets != None:
			if len(self.result) == len(self.tweets) :
				data = []
				# i= 0
				for (tweet,result) in zip(self.tweets,self.result):
					# tweet = self.tweets[i]
					# result = self.result[i]
					item = {
						'id': tweet['id'],
						'text': str(tweet['tweet'].encode('UTF-8')),
						'sentiment': result['value'],
						'date': tweet['date'].split(' ')[0],
						'time': tweet['date'].split(' ')[1],
						'username': tweet['username']
					}
					data.append(item)
				return data
			else:
				return {'Error': 'Result and tweet are not the same'}
				pass
		else:
			pass
		pass


def main():
	# model = AImodel.loadModel('AI/Depression_model.h5')

	# mytext = ['Hello world','I will destroy the world']
	# mytext = list(map(AImodel.preprocessor,mytext))#AImodel.preprocessor(mytext)
	# print(mytext)
	# token = AImodel.tokenize(mytext, train=False,tokenpath='AI/tokenizer.json')
	# result = AImodel.predict(mytext,token,model)
	#startTime = time.time()
	# try:
		# c = twint.Config()
		# c.Username = "Rounmubamgbose"
		# c.Limit = 2000
		# c.Store_object = True

		# c.Hide_output = True

		# twint.run.Search(c)
		# tweets = twint.output.tweets_list
		# texts = [str(x.tweet.encode('UTF-8')) for x in tweets]

		# print(texts)
	# except Exception as e:
	# 	print(e)
	# print('************************************************')
	# print('***********************RESULT*******************')
	# print('**************************************************')
	time.sleep(1)
	model = AImodel.loadModel('AI/Depression_model.h5')
	mytext = "b'this life is so sad and i hate myself"
	mytext = AImodel.preprocessor(mytext)
	# mytext = list(map(AImodel.preprocessor,texts))#AImodel.preprocessor(mytext)
	# #print(mytext)
	mytext = str(mytext)
	token = AImodel.tokenize(mytext, train=False,tokenpath='AI/tokenizer.json')
	result = AImodel.predict(mytext,token,model)
	print(result)
	#endTime = time.time()
	
	#print(newtext)

	#print('This time is {} secs'.format(endTime-startTime))



if __name__ == '__main__':
	main()