import pandas as pd
import numpy as np
import matplotlib as pl
import tensorflow as tf 
#import nltk as nl 
import re 
import json 
import os as dirc



# from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

#nl.download()


class AImodel:
	def __init__(self,trainsize,traindocUrl,train=True):
		self.trainsize = trainsize
		self.traindocUrl = traindocUrl
		self.train = train
		self.model = None #The NeuralNetwork Model or Model choosen
		self.df  = None #dataset
		self.traindf = None #trainningdata dataset 
		self.testdf = None#testing dataset
		self.trainFeature = None  #traindata dataset features
		self.trainLabel = None  #training dataset labels
		self.testFeature= None #testing dataset features
		self.testLabel = None #testing dataset labels

		
	#extracting data 
	def load_data(self):
		try:
			self.df = pd.read_csv(self.traindocUrl,engine='python')
		except Exception as e:
			print(e)

	#prepocessing output and input
	@staticmethod
	def preprocessor(text):
		if isinstance(text,str):
			#convert text to lowercase 
			text = text.lower()
			# #remove RT usermentions links and emojis
			emoji_pattern = re.compile("["
			   u"\U0001F600-\U0001F64F"  # emoticons
			   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
			   u"\U0001F680-\U0001F6FF"  # transport & map symbols
			   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
			   u"\U00002500-\U00002BEF"  # chinese char
			   u"\U00002702-\U000027B0"
			   u"\U00002702-\U000027B0"
			   u"\U000024C2-\U0001F251"
			   u"\U0001f926-\U0001f937"
			   u"\U00010000-\U0010ffff"
			   u"\u2640-\u2642"
			   u"\u2600-\u2B55"
			   u"\u200d"
			   u"\u23cf"
			   u"\u23e9"
			   u"\u231a" 
			   u"\ufe0f"  #dingbats
			   u"\u3030"
			   "]+", flags=re.UNICODE)
			text = emoji_pattern.sub(r'',text) # removing emojis and special characters
			text = re.sub("(RT|rt)\S*"," ",text) #remove RT 
			text = text.replace("\qt","\"") #replacing all \qt with "
			text = re.sub("(@\S+)"," ",text) #remove @handles 
			text = re.sub("((https|http|www)\S*)|([a-z]+.[a-z]+\.com/[a-zA-z0-9=?/.&]*)|([a-z]+.[a-z]+\.com)|(\S+\.com)"," ",text) #remove @URL 
			#remove numbers 
			#remove punctuation and special characters
			#remove stop words 
			#stemming
			return text 
		else:
			return 0
		pass

	#function to tokenize , sequence and pad words
	@staticmethod
	def tokenize(text, train=True,tokenpath=None):
		if tokenpath is None:
			tokenpath = 'tokenizer.json'
			pass


		if type(text) is str:
			text = [text]
			pass

		text = [str(x) for x in text] #to make sure every item is a string

		if train: 
			if dirc.path.exists(tokenpath):
				dirc.remove(tokenpath)

		if train:
			if not dirc.path.exists(tokenpath):
				tokenizer = Tokenizer(num_words=9000,oov_token='<00V>')
				tokenizer.fit_on_texts(text)
				word_index = tokenizer.word_index
				tokenizer_json = tokenizer.to_json() #saving tokenizer to json 
				with open(tokenpath,'w+',encoding='utf-8') as file: #creates a file to save token when Training text is tokenized
					#copy files here
					file.write(json.dumps(tokenizer_json,ensure_ascii=False)) 
					#print(word_index)
					pass
				 
				training_sequences = tokenizer.texts_to_sequences(text)
				training_padded = pad_sequences(training_sequences,maxlen=250,padding='post',truncating='post')
				#print('....tokenized trainingdata')				
				return np.array(training_padded)
			else:
				with open(tokenpath,'r+',encoding='utf-8') as file: #retrieve tokens from file if it does exist
					data = json.load(file)
					tokenizer = tokenizer_from_json(data) #Loading Tokenizer from file
					pass
				text_sequences = tokenizer.texts_to_sequences(text)
				text_padded = pad_sequences(text_sequences,maxlen=250,padding='post',truncating='post')
				#print('....tokenized testingdata')
				return np.array(text_padded)
				pass
		else:
			if tokenpath is None:
				print('Tokenizer.json not avaliable')
			else:
				with open(tokenpath,'r+',encoding='utf-8') as file: #retrieve tokens from file if it does exist
						data = json.load(file)
						tokenizer = tokenizer_from_json(data) #Loading Tokenizer from file
						pass
				text_sequences = tokenizer.texts_to_sequences(text)
				text_padded = pad_sequences(text_sequences,maxlen=250,padding='post',truncating='post')
				#print('....tokenized testingdata')
				return np.array(text_padded)
		pass

	def NeuralNetwork(self):
		self.model = tf.keras.Sequential([
			tf.keras.layers.Embedding(9000,32),
			#tf.keras.layers.LSTM(32),
			tf.keras.layers.GlobalAveragePooling1D(),
			tf.keras.layers.Dense(24,activation='relu'),
			tf.keras.layers.Dense(1,activation='sigmoid'),
		]) #creating the structure of the model

		self.model.compile(loss="binary_crossentropy",optimizer="adam",metrics=["accuracy"])
		self.model.summary() #printing structure of the model
		self.model.fit(self.trainFeature,self.trainLabel,epochs=10,validation_data=(self.testFeature,self.testLabel),verbose=2)#training model

		pass

	#saving model 
	def saveModel(self):
		if dirc.path.exists('Depression_model.h5'):
			dirc.remove('Depression_model.h5')
		self.model.save('Depression_model.h5')
		pass

	@staticmethod
	def loadModel(modelPath):
		model = tf.keras.models.load_model(modelPath)
		return model

	@staticmethod
	def predict(text,tokens,model):
		if type(text) is str:
			text = [text]
		result = model.predict(tokens)
		result = result.tolist()
		result = [x[0] for x in result]
		result = zip(text,result)
		result = [{'text': x[0] , 'value': x[1] } for x in result]
		return result


	def run(self):
		if self.train:
			self.load_data()
			self.df = self.df.sample(frac=1) #shuffle the data 
			self.df['Text'] = self.df['Text'].apply(self.preprocessor) #preprocessing everything in the dataset 
			#splitting data
			self.traindf = self.df[0:self.trainsize] #trainningdata dataset 
			self.testdf = self.df[self.trainsize:] #testing dataset
			self.trainFeature = self.traindf['Text'] #traindata dataset features
			self.trainLabel = self.traindf['Value'] #training dataset labels
			self.testFeature = self.testdf['Text'] #testing dataset features
			self.testLabel = self.testdf['Value'] #testing dataset labels
			# print(trainFeature.head())
			# print(testdf.shape)
			self.trainFeature = self.trainFeature.tolist()
			self.testFeature = self.testFeature.tolist()
			self.trainFeature = self.tokenize(self.trainFeature) #tokenize the training features
			self.testFeature = self.tokenize(self.testFeature,train=False) #tokenize the testing features
			self.testLabel = self.testLabel.to_numpy()#making the testLabels a numpy array
			self.trainLabel = self.trainLabel.to_numpy() #making the trainLabels a numpy array
			#print(self.testFeature)


			#Training the Model
			self.NeuralNetwork()
			#Testing
			print('***********TESTING TIME************')
			myTest = ['Depression is taking a hard toll on me','This is the a very good day for footie']
			print(myTest)
			myTest =  self.tokenize(myTest,train=False)
			res = self.model.predict(myTest)
			print(type(res))
			print(res)


			print('Working......')

			#save a model 

			self.saveModel()

			print('Model saved !!!!')
			 
			# subr = self.trainFeature.shape[0]/5
			# subr = self.df.shape[0]/5
			# index=0
			# while index < subr :
			# 	end = index+5
			# 	print(self.df[index:end].head())
			# 	index=index+5
		else:
			pass



def main():
	myAImodel = AImodel(trainsize = 15000,traindocUrl='Data/RealDataedited.csv')
	myAImodel.run()

if __name__ == '__main__':
	main()