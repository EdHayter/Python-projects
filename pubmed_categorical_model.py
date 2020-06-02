"""
Categorical model for citation estimation
take data from 'pubmed_feature_encoder.py'

Ed Hayter 29/05/20
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split,GridSearchCV
from scipy import sparse
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier,AdaBoostClassifier
import xgboost as xgb
import time
import numpy as np 

#create y with categorical [low/med/high #cites]
#numbers chosen to roughly split dataset into 3

y_train[(y_train>0) & (y_train<5)]=1
y_train[(y_train>4)]=2
y_valid[(y_valid>0) & (y_valid<5)]=1
y_valid[(y_valid>4)]=2

#%% model training and evaluation block
#note: gradient boosting on default settings achieves 61.8% valid accuracy

start_time = time.time()

#initialise model and fit
# model = GradientBoostingClassifier(random_state=2)
model = xgb.XGBClassifier(random_state=2)
model.fit(X_train.tocsr(),y_train,
          eval_metric="merror",
          eval_set = [(X_train.tocsr(),y_train),(X_valid.tocsr(),y_valid)])

#compare error over train and validation sets to test for overfitting
acc_train = accuracy_score(model.predict(X_train),y_train)*100
acc_valid = accuracy_score(model.predict(X_valid),y_valid)*100
print("--- %s seconds ---" % (time.time() - start_time))
print('train accuracy: ' + str(acc_train) +'\nvalid accuracy: ' + str(acc_valid))

#plot error over time
d = {'train':model.evals_result()['validation_0']['merror'],
     'valid':model.evals_result()['validation_1']['merror']}
data = pd.DataFrame(d)
sns.lineplot(data=data) 

#what features are being used? 
used_feature_indexes = np.nonzero(model.feature_importances_)[0]

#huge overfitting problem. let's try and tune hyperparameters
# tuned_parameters = [{'n_estimators': [10, 40, 70],
#                       'max_features': [10000, 15000, 20000],
#                       'max_depth' : [10, 15, 20]
#                       }]
# clf = GridSearchCV(ExtraTreesClassifier(random_state=2), tuned_parameters, scoring='accuracy')
# clf.fit(X_train,y_train)

# clf.best_params_()

