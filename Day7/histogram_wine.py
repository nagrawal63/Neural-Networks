import numpy as np
import pandas as pd
from pandas_ml import ConfusionMatrix
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pickle as pickle
from matplotlib.gridspec import GridSpec

df=pd.read_csv('/home/nishchay/Documents/Arcon/Day6/winequality-red.csv')
df=pd.get_dummies(df,columns=['quality'])
df.drop(['citric acid','residual sugar','pH','free sulfur dioxide','quality_3','quality_8'], axis = 1, inplace = True)
training_data=df.head(1100).iloc[:,0:7].values
testing_data=df.tail(400).iloc[:,0:7].values
X=df.iloc[:,0:7].values
y=df.iloc[:,7:11].values
X = X/np.amax(X, axis=0)
training_data = training_data/np.amax(training_data, axis=0)
testing_data = testing_data/np.amax(testing_data, axis=0)
#xPredicted = xPredicted/np.amax(xPredicted, axis=0)
#y = y/100


def make_pie_chart(predicted,actual):
    labels = 'Quality_4', 'Quality_5', 'Quality_6'
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)
    maxP=np.argmax(predicted,axis=1)
    maxA=np.argmax(actual,axis=1)
    predict= np.zeros((3,), dtype=int)
    actual_pie=np.zeros((3,), dtype=int)
    for i in maxP:
        if i==1 :
            predict[0]+=1
            actual_pie[0]+=1
        elif i==2:
            predict[1]+=1
            actual_pie[1]+=1
        elif i ==3: 
            predict[2]+=1
            actual_pie[2]+=1
    for i in maxA:
        if i==1 :
            actual_pie[0]+=1
        elif i==2:
            actual_pie[1]+=1
        elif i ==3:
            actual_pie[2]+=1
    f,(ax1,ax2)=plt.subplots(1,2,sharey=True,figsize=(15,15))
    f.suptitle('Predicted vs actual')
#    plt.subplot(the_grid[0, 0], aspect=1)
#    axarr[0].setTitle('Predicted')
    ax1.pie(predict,labels=labels,colors=colors,autopct="%1.1f%%", shadow=False)
#    plt.subplot(the_grid[0,1],aspect=1)
#    axarr[1].setTitle('Predicted')
    ax2.pie(actual_pie,labels=labels,colors=colors,autopct="%1.1f%%", shadow=False)
    plt.show()

class Neural_Network(object):
  def __init__(self):

    self.inputSize = 7
    self.outputSize = 4
    self.hiddenSize = 10

    self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
    self.W2 = np.random.randn(self.hiddenSize, self.outputSize) 

  def predict(self,actual):
    print ('Predicting ...')
    predicted=[]
    for i in range(0,testing_data.shape[0]):
        l1 = 1/(1 + np.exp(-(np.dot(testing_data[i], NN.W1))))
        l2 = 1/(1 + np.exp(-(np.dot(l1, NN.W2))))
        predicted.append(np.round(l2,3))
    #plt.hist(predicted, normed=True, bins=1)
    #plt.ylabel('Probability')
    #plt.show()
    #accuracy=predicted/actual
    #accuracy[accuracy >1]=0
    #print ('Accuracy: '+str(np.mean(accuracy)*3))
    make_pie_chart(predicted,actual)

NN = Neural_Network()
def run(NN):
	learning_rate = 0.2 # slowly update the network
	error=[]
	for epoch in range(5000):
		for i in range(0,training_data.shape[0]):
		    row=X[i][np.newaxis]
		    l1 = 1/(1 + np.exp(-(np.dot(row, NN.W1))))# sigmoid function
		    l2 = 1/(1 + np.exp(-(np.dot(l1, NN.W2))))
		    er = (abs(y[i] - l2)).mean()
		    l2_delta = (y[i][np.newaxis] - l2)*(l2 * (1-l2))
		    l1_delta = l2_delta.dot(NN.W2.T) * (l1 * (1-l1))
		    NN.W2 += l1.T.dot(l2_delta) * learning_rate
		    NN.W1 += row.T.dot(l1_delta) * learning_rate
		print ('Error:', er)
		error.append(er)
	plt.hist(error, normed=True, bins=30)
	plt.ylabel('Probability');
	list_pickle_path1 = 'list_pickle_weight1.pkl'
	list_pickle_path2 = 'list_pickle_weight2.pkl'
	list_pickle1 = open(list_pickle_path1, 'wb')
	list_pickle2 = open(list_pickle_path2, 'wb')
	pickle.dump(NN.W1, list_pickle1)
	pickle.dump(NN.W2, list_pickle2)
	list_pickle1.close()
	list_pickle2.close()
#NN.predict(y)
#run (NN)


with open('list_pickle_weight1.pkl','rb') as f: 
	NN.W1 = pickle.load(f)

with open('list_pickle_weight2.pkl','rb') as f: 
	NN.W2 = pickle.load(f)
NN.predict(y)