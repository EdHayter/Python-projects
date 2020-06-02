"""
Pubmed feature encoder to format features from scraper into sparse matrix for modelling

Ed Hayter 27/05/20
"""

import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from scipy import sparse
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# filepath = 'test.csv'
data = pd.read_csv('test.csv')
data2 = pd.read_csv('test2.csv')

#cat the 2 files
data = pd.concat([data, data2],ignore_index=True)
#drop other index, tidy nulls
data = data.drop('Unnamed: 0',axis=1) 
data.Abstract.fillna(' ',inplace=True)

#Count authors, set new column
data['no_authors'] = data.Authors.str.count(',') + 1
data.no_authors.fillna(0,inplace=True)

#remove initials from first and last authors (take only last name)
data['First_author'] = data.First_author.str.split(' ',1,expand=True)[0]
data['Last_author'] = data.Last_author.str.split(' ',1,expand=True)[0]

#drop rows with invalid years 
valid_years = ['2015','2016','2017','2018','2019','2020']
data=data[(data.Year.isin(valid_years))]

#One hot encode authors
first_ohe = pd.get_dummies(data['First_author'],prefix = 'F_a',sparse=True)
last_ohe = pd.get_dummies(data['Last_author'],prefix = 'L_a',sparse=True)

#one hot encode article type, NaNs are articles
data.Article_type.fillna('Article',inplace=True)
article_type_ohe = pd.get_dummies(data['Article_type'],prefix = 'A_T',sparse=True)
#encode journals 
journal_ohe = pd.get_dummies(data['Journal'],prefix='journal',sparse=True)
#bolt onto data [too large]
# data = pd.concat([data, article_type_ohe, journal_ohe, first_ohe, last_ohe],axis=1)

#convert to sparse and bolt together 
first_ohe = sparse.csr_matrix(first_ohe)
last_ohe = sparse.csr_matrix(last_ohe)
article_type_ohe = sparse.csr_matrix(article_type_ohe)
journal_ohe = sparse.csr_matrix(journal_ohe)
year = sparse.csr_matrix(data.Year.astype(int)).transpose()
no_authors = sparse.csr_matrix(data.no_authors.astype(int)).transpose()

data_sparse = sparse.hstack([first_ohe,last_ohe,article_type_ohe,journal_ohe,year,no_authors])

#see distribution of citations 
sns.distplot(data.no_citations) 


#split train/valid sets, make sure random_state is equal otherwise we'll shuffle indicies
x_train, x_valid, y_train, y_valid = train_test_split(data.drop('no_citations',axis=1),data['no_citations'],test_size=0.1,random_state=2)
x_train_sp, x_valid_sp, y_train, y_valid = train_test_split(data_sparse,data['no_citations'],test_size=0.1,random_state=2)


#initialise vectoriser for bag of words
#combines count vectorisation with tfidf normalisation 
vectoriser = TfidfVectorizer()
#fit vectoriser to train data, transform both sets to avoid leakage 
x_train_titles_bow = vectoriser.fit_transform(x_train.Title)
x_valid_titles_bow = vectoriser.transform(x_valid.Title)

#same for abstract
x_train_abstract_bow = vectoriser.fit_transform(x_train.Abstract)
x_valid_abstract_bow = vectoriser.transform(x_valid.Abstract)

#finally build sparse matrix for model training
X_train = sparse.hstack([x_train_sp,x_train_titles_bow,x_train_abstract_bow])
X_valid = sparse.hstack([x_valid_sp,x_valid_titles_bow,x_valid_abstract_bow])

#%%
#train random forest
model = RandomForestRegressor()
model.fit(X_train,y_train)

#compare error over train and validation sets to test for overfitting
mse_train = mean_squared_error(model.predict(X_train),y_train)
mse_valid = mean_squared_error(model.predict(X_valid),y_valid)
print('train MSE: ' + str(mse_train) +'\nvalid MSE: ' + str(mse_valid))



    
    




