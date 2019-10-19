import pandas as pd #To work with dataset
import numpy as np #Math library
from sklearn.model_selection import train_test_split, KFold, cross_val_score # to split the data
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, fbeta_score #To evaluate our model

from sklearn.naive_bayes import GaussianNB


def train_model():
    # returns trained Gaussian model that has been trained on the test data
    df_credit = pd.read_csv("./german_credit_data.csv",index_col=0)
    #Purpose to Dummies Variable
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Purpose, drop_first=True, prefix='Purpose'), left_index=True, right_index=True)
    #Sex feature in dummies
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Sex, drop_first=True, prefix='Sex'), left_index=True, right_index=True)
    # Housing get dummies
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Housing, drop_first=True, prefix='Housing'), left_index=True, right_index=True)
    # Housing get Saving Accounts
    df_credit = df_credit.merge(pd.get_dummies(df_credit["Saving accounts"], drop_first=True, prefix='Savings'), left_index=True, right_index=True)
    # Housing get Risk
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Risk, prefix='Risk'), left_index=True, right_index=True)
    # Housing get Checking Account
    df_credit = df_credit.merge(pd.get_dummies(df_credit["Checking account"], drop_first=True, prefix='Check'), left_index=True, right_index=True)
    # Housing get Age categorical
    cats = ['Student', 'Young', 'Adult', 'Senior']
    interval = (18, 25, 35, 60, 120)
    df_credit["Age_cat"] = pd.cut(df_credit.Age, interval, labels=cats)
    df_credit = df_credit.merge(pd.get_dummies(df_credit["Age_cat"], drop_first=True, prefix='Age_cat'), left_index=True, right_index=True)

    GNB = GaussianNB()
    del df_credit["Saving accounts"]
    del df_credit["Checking account"]
    del df_credit["Purpose"]
    del df_credit["Sex"]
    del df_credit["Housing"]
    del df_credit["Age_cat"]
    del df_credit["Risk"]
    del df_credit['Risk_good']

    X = df_credit.drop('Risk_bad', 1).values
    y = df_credit["Risk_bad"].values

    # Spliting X and y into train and test version
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)

    model = GNB.fit(X_train, y_train)
    return model


def compute_credit_confidence(model, params):

    # params:
    # ['Age',
    #  'Job',
    #  'Credit amount',
    #  'Duration',
    #  'Sex_male',
    #  'Housing_own',
    #  'Housing_rent',
    #  'Savings_moderate',
    #  'Savings_quite rich',
    #  'Savings_rich',
    #  'Risk_bad',
    #  'Check_moderate',
    #  'Check_rich']
    #

    return (model.predict_proba(params), model.fit(params))
