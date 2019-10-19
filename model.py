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
    del df_credit["Age_cat_Young"]
    del df_credit["Age_cat_Senior"]
    del df_credit["Risk"]
    del df_credit['Risk_good']
    del df_credit['Purpose_car']
    del df_credit['Purpose_domestic appliances']
    del df_credit['Purpose_education']
    del df_credit['Purpose_furniture/equipment']
    del df_credit['Purpose_radio/TV']
    del df_credit['Purpose_repairs']
    del df_credit['Purpose_vacation/others']

    df = df_credit[["Age",
      'Job',
      'Credit amount',
      'Duration',
      'Sex_male',
      'Housing_own',
      'Housing_rent',
      'Savings_moderate',
      'Savings_quite rich',
      'Savings_rich',
      'Risk_bad',
      'Check_moderate',
      'Check_rich']]

    X = df.drop('Risk_bad', 1).values
    y = df["Risk_bad"].values

    # Spliting X and y into train and test version
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)

    model = GNB.fit(X_train, y_train)
    return model


def compute_credit_confidence(model, params):

    # params:
    # ['Age', Age of lendee
    #  'Job', 1 if they have job 0 otherwise
    #  'Credit amount', Amount of credit that they owe
    #  'Duration', Amount of time for which they have owed debt (dummy val is fine)
    #  'Sex_male', 1 if male, 0 otherwise
    #  'Housing_own', 1 if they own their own house
    #  'Housing_rent', 1 if they rent
    #  'Savings_moderate', 1 if they have moderate savings
    #  'Savings_quite rich', 1 if they have some savings
    #  'Savings_rich', 1 if they rich
    #  'Check_moderate', 1 if they have some money in checking
    #  'Check_rich'] 1 if they rich

    params_dict = {}
    params_dict["Age"] = [params[0]]
    params_dict["Job"] = [params[1]]
    params_dict["Credit amount"] = [params[2]]
    params_dict["Duration"] = [params[3]]
    params_dict["Sex_male"] = [params[4]]
    params_dict["Housing_own"] = [params[5]]
    params_dict["Housing_rent"] = [params[6]]
    params_dict["Savings_moderate"] = [params[7]]
    params_dict["Savings_quite rich"] = [params[8]]
    params_dict["Savings_rich"] = [params[9]]
    params_dict["Check_moderate"] = [params[10]]
    params_dict["Check_rich"] = [params[11]]

    df = pd.DataFrame(params_dict)

    return (model.predict_proba(df), model.predict(df))


if __name__ == "__main__":
    model = train_model()
    conf, res = compute_credit_confidence(model, [22,1,500,313,1,0,1,0,1,0,1,0])
    print(conf)
    print(res)
