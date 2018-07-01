import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import numpy as np
import pickle

df = pd.read_csv('E:\phishing2.csv')
def train(df):
	
	feature_column_names = [ 'url_length','having_at_symbol','double_slash','https_token','ip_address', 'tiny_url', 
		'email_submit','ssl_state', 'port','redirect','domain_registeration_length','Prefix_Suffix','sub_domain','age_of_domain','url_anchor','web_traffic','google_index','favicon','requesr_url','links_in_tags','result']

	df = df[feature_column_names]

	X = df.drop('result',axis=1)
	y = df['result']

	X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.3,shuffle=True)

	print(X_train.shape)
	print(y_train.shape)
	print(X_test.shape)
	print(y_test.shape)


	rf_model = RandomForestClassifier(random_state=5,n_estimators=400)

	rf_model.fit(X,y)

	y_predict = rf_model.predict(X_test)
	#print(y_predict)
	accuracy = accuracy_score(y_test, y_predict)
	#train_accuracy = accuracy_score(y_train,rf_model.predict(X_train))
	#print(train_accuracy)
	#for i in range(0,5):
		#print("Actual: {} Predicted: {}".format(list(y_test)[i],y_predict[i]))
	print("model accuracy : ", accuracy)
	print(confusion_matrix(y_test,y_predict))

	with open('model.pickle', 'wb') as f:
		pickle.dump(rf_model, f)

def model_load(filename):

	with open(filename, 'rb') as f:
		model = pickle.load(f)
		return model

train(df)




