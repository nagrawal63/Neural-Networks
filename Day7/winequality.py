import numpy as np
import pandas as pd
from pandas_ml import ConfusionMatrix
import matplotlib.pyplot as plt

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
        print ('Predicted: '+str(predicted))
    #accuracy=predicted/actual
    #accuracy[accuracy >1]=0
    #print ('Accuracy: '+str(np.mean(accuracy)*3))

NN = Neural_Network()
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
#NN.predict(y)