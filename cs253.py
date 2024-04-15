import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
# Read the training data
train_df = pd.read_csv('/kaggle/input/shivam/train.csv')

# Preprocessing
label = LabelEncoder()
train_df['Party'] = label.fit_transform(train_df['Party'])
train_df['state'] = label.fit_transform(train_df['state'])
train_df['Total Assets'] = train_df['Total Assets'].str.replace(' Crore+', 'e+7').str.replace(' Lac+', 'e+5').str.replace(' Thou+', 'e+3').str.replace(' Hund+', 'e+2')
train_df['Liabilities'] = train_df['Liabilities'].str.replace(' Crore+', 'e+7').str.replace(' Lac+', 'e+5').str.replace(' Thou+', 'e+3').str.replace(' Hund+', 'e+2')
train_df['Total Assets'] = pd.to_numeric(train_df['Total Assets'])
train_df['Liabilities'] = pd.to_numeric(train_df['Liabilities'])

education_mapping = {
    'Doctorate': 10,'Post Graduate': 9,'Graduate Professional': 8,'Graduate': 7,'12th Pass': 6,'10th Pass': 5,'8th Pass': 4,'5th Pass': 3,'Literate': 2,'Others': 1
}
train_df['Education'] = train_df['Education'].replace(education_mapping)

# Feature Engineering: Ratio of Liabilities to Assets
train_df['Feature_engineering_promt'] = np.log((train_df['Liabilities'] + 1)/ (train_df['Total Assets'] + 1)) # Adding a small constant before division to avoid zero division

# Read the test data
test_df = pd.read_csv('/kaggle/input/shivam/test.csv')

# Preprocess test data
test_df['Party'] = label.transform(test_df['Party'])
test_df['state'] = label.transform(test_df['state'])
test_df['Total Assets'] = test_df['Total Assets'].str.replace(' Crore+', 'e+7').str.replace(' Lac+', 'e+5').str.replace(' Thou+', 'e+3').str.replace(' Hund+', 'e+2')
test_df['Liabilities'] = test_df['Liabilities'].str.replace(' Crore+', 'e+7').str.replace(' Lac+', 'e+5').str.replace(' Thou+', 'e+3').str.replace(' Hund+', 'e+2')
test_df['Total Assets'] = pd.to_numeric(test_df['Total Assets'])
test_df['Liabilities'] = pd.to_numeric(test_df['Liabilities'])

# Feature Engineering: Ratio of Liabilities to Assets for test data
test_df['Feature_engineering_promt'] = np.log((test_df['Liabilities'] +1)/ (test_df['Total Assets'] + 1)) 


# Define features and target variable
features = ['Party', 'Criminal Case', 'state', 'Feature_engineering_promt']
X = train_df[features]
y = train_df['Education']

# Scale features
scaler = MinMaxScaler()
x_parameters = scaler.fit_transform(X)

#Grid_Search for best params
KNN = KNeighborsClassifier()
parameters = {'n_neighbors': (1,31), 'weights': ['uniform'], 'metric': ['euclidean']}
trained_data = GridSearchCV(KNN, parameters, cv=5)

# Fit the model
trained_data.fit(x_parameters, y)




# Scale test features
KNN.fit(x_parameters, y)

# Scaled and made predictions
X_test_scaled = scaler.transform(test_df[features])
predictions = KNN.predict(X_test_scaled)

education_remapping = {v: k for k, v in education_mapping.items()}
predicted_df = pd.DataFrame({'ID': test_df['ID'], 'Education': [education_remapping[int(prediction)] for prediction in predictions]})

# Store predictions to CSV
predicted_df.to_csv('submission.csv', index=False)
