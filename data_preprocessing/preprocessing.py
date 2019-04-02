# Restrict dataset to selected features

Brooklyn_Permit_Issuance_Corp = NYC_Permit_Issuance.loc[(NYC_Permit_Issuance['BOROUGH'].isin(['BROOKLYN'])) & (NYC_Permit_Issuance['Owner\'s Business Type'].isin(['CORPORATION'])) & (NYC_Permit_Issuance['Filing Status'].isin(['INITIAL'])) & (NYC_Permit_Issuance['Permit Status'].isin(['ISSUED']))]

Brooklyn_Permit_Issuance_Corp_prediction_dataset = Brooklyn_Permit_Issuance_Corp[['Special District 1', 'Special District 2', 'Non-Profit', 
                               'Permittee\'s License Type', 'Permit Type', 'Residential',
                                'Bldg Type', 'Work Type', 'Processing Time']]

Brooklyn_Permit_Issuance_Corp_prediction_dataset.index = range(len(Brooklyn_Permit_Issuance_Corp_prediction_dataset.index))

# Label encoding for categorical variables

from sklearn import preprocessing

def encode_transform_labels(df):
    
    # Label encoders for categorical variables 
    df2 = df
    sd1_enc = preprocessing.LabelEncoder()
    sd1_enc.fit(list(df2['Special District 1'].astype(str).unique()))

    sd2_enc = preprocessing.LabelEncoder()
    sd2_enc.fit(list(df2['Special District 2'].unique().astype(str)))

    non_profit_enc = preprocessing.LabelBinarizer()
    non_profit_enc.fit(list(df['Non-Profit'].unique().astype(str)))

    ltype_enc = preprocessing.LabelEncoder()
    ltype_enc.fit(list(df2['Permittee\'s License Type'].unique().astype(str)))

    ptype_enc = preprocessing.LabelEncoder()
    ptype_enc.fit(list(df2['Permit Type'].unique().astype(str)))

    residential_enc = preprocessing.LabelBinarizer()
    residential_enc.fit(list(df2['Residential'].unique().astype(str)))

    bldg_type_enc = preprocessing.LabelEncoder()
    bldg_type_enc.fit(list(df2['Bldg Type'].unique().astype(str)))

    wtype_enc = preprocessing.LabelEncoder()
    wtype_enc.fit(list(df2['Work Type'].unique().astype(str)))

    df2['Special District 1'] = sd1_enc.transform(df2['Special District 1'].astype(str))
    df2['Special District 2'] = sd2_enc.transform(df2['Special District 2'].astype(str))
    df2['Non-Profit'] = non_profit_enc.transform(df2['Non-Profit'].astype(str))
    df2['Permittee\'s License Type'] = ltype_enc.transform(df2['Permittee\'s License Type'].astype(str))
    df2['Permit Type'] = ptype_enc.transform(df2['Permit Type'].astype(str))
    df2['Residential'] = residential_enc.transform(df2['Residential'].astype(str))
    df2['Bldg Type'] = bldg_type_enc.transform(df2['Bldg Type'].astype(str))
    df2['Work Type'] = wtype_enc.transform(df2['Work Type'].astype(str))
    
    return df2

# Applying both encoders (one-hot encoding on top of label encoding)

label_encoded_df = encode_transform_labels(Brooklyn_Permit_Issuance_Corp_prediction_dataset)

features_data = label_encoded_df[label_encoded_df.columns[:-1]]
labels_data = label_encoded_df['Processing Time']

encoded_prediction_dataset = preprocessing.OneHotEncoder().fit_transform(features_data)

# Train/test split

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(encoded_prediction_dataset, labels_data, test_size = 0.3)

# Cat2Vec

from gensim.models.word2vec import Word2Vec
from random import shuffle
import copy

X = Brooklyn_Permit_Issuance_Corp_prediction_dataset.iloc[:,:-1]
y = Brooklyn_Permit_Issuance_Corp_prediction_dataset['Processing Time']

X_train_c2v, X_test_c2v, y_train_c2v, y_test_c2v = train_test_split(Brooklyn_Permit_Issuance_Corp_prediction_dataset, labels_data, test_size = 0.3) 

size=6
window=8

x_c2v = copy.deepcopy(features_data)
names = list(x_c2v.columns.values)

for i in names:
    x_c2v[i]=x_c2v[i].astype('category')
    x_c2v[i].cat.categories = ["Feature %s %s" % (i,g) for g in x_c2v[i].cat.categories]
x_c2v = x_c2v.values.tolist()

for i in x_c2v:
    shuffle(i)
    
c2v = Word2Vec(x_c2v,size=size,window=window)

X_train_c2v = copy.copy(X_train_c2v)
X_test_c2v = copy.copy(X_test_c2v)

for i in names:
    X_train_c2v[i]=X_train_c2v[i].astype('category')
    X_train_c2v[i].cat.categories = ["Feature %s %s" % (i,g) for g in X_train_c2v[i].cat.categories]
    
for i in names:
    X_test_c2v[i]=X_test_c2v[i].astype('category')
    X_test_c2v[i].cat.categories = ["Feature %s %s" % (i,g) for g in X_test_c2v[i].cat.categories]
    
X_train_c2v = X_train_c2v.values
X_test_c2v = X_test_c2v.values
x_c2v_train = np.random.random((len(X_train_c2v),size*X_train_c2v.shape[1]))

for j in range(X_train_c2v.shape[1]):
    for i in range(X_train_c2v.shape[0]):
        if X_train_c2v[i,j] in c2v:
            x_c2v_train[i,j*size:(j+1)*size] = c2v[X_train_c2v[i,j]]
x_c2v_test = np.random.random((len(X_test_c2v),size*X_test_c2v.shape[1]))

for j in range(X_test_c2v.shape[1]):
    for i in range(X_test_c2v.shape[0]):
        if X_test_c2v[i,j] in c2v:
            x_c2v_test[i,j*size:(j+1)*size] = c2v[X_test_c2v[i,j]]
