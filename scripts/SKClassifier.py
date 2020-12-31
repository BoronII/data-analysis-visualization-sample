import math
import numpy  as np
import pandas as pd
import pickle
 
from fastai.tabular.all      import TabularPandas, Categorify, FillMissing  
from sklearn.metrics         import roc_auc_score
from sklearn.model_selection import train_test_split
from pathlib                 import Path


class SKClassifier: 
    """
    A class to streamline training and prediction with sklearn classification 
    models.

    ...

    Attributes
    ----------
    model : sklearn classification model
    df : pandas dataframe
        the dataframe containing all features that will be used for class 
        prediction as well as the dependant variable.
    cat : list
        list containing the columns of the df that are to be treated as 
        categorical.
    cont : list
        list containing the columns of the df that are to be treated as 
        continuous.
    dep_var : str
        the name of the column containing the dependant variable.
    procs : list
        list of procedures that will be passed to the fastai TabularPandas
        object.
   
    Methods
    -------
    process_df(test_size, random_state, save):
        if a test_size is specified the dataframe is split into training and 
        validation sets using the sklearn train_test_split function. When 
        test_size is not specified the method doesn't yet have an implementation
        and will raise and error. 
    fit(xs, y):
        fits the model using the models fit method.
    predict_proba(xs):
        gets predictions from the model using the models predict_proba method.
        If the dep_var column has 2 unique values two class classification is
        assumed, otherwise multiclass classification is assumed.
    auroc(targ, pred):
        computes the AUROC score using sklearn's, roc_auc_score function.
        For multiclass classification multi_class='ovo' is passed to the
        roc_auc_score function.If the dep_var column has 2 unique values two 
        class classification is
        assumed, otherwise multiclass classification is assumed.
    save(path):
        saves the trained model to the specified path.
    """

    def __init__(self, model, df, cat, dep_var, procs, cont=None): 
        self.cat     = cat
        self.cont    = cont
        self.dep_var = dep_var
        self.procs   = procs
        self.df      = df
        self.model   = model
        
    def process_df(self, test_size=None, random_state=42, save_as=None):
        if test_size!=None:
            X = self.df[self.cat + self.cont] if self.cont!=None else self.df[self.cat]
            y = self.df[self.dep_var] 
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, 
                                                                random_state=random_state)
            X_train.reset_index(inplace=True)
            X_test.reset_index(inplace=True)
            train_idx = X_train['index']
            valid_idx = X_test['index']
            splits = (list(train_idx), list(valid_idx))
       
        # tabular object
        to = TabularPandas(self.df, self.procs, self.cat, self.cont, 
                           y_names=self.dep_var, splits=splits, do_setup=True, 
                           reduce_memory=True)
        
        # get training and validation data
        self.xs, self.y             = to.train.xs, to.train.y
        self.valid_xs, self.valid_y = to.valid.xs, to.valid.y
            
        return to
           
        
    def fit(self, xs, y):
        # train classifier
        self.model.fit(xs, y)
    
    def predict_proba(self, xs):
        # get predictions
        # if two classes
        if len(self.df[self.dep_var].unique())==2:
            self.prob = self.model.predict_proba(xs)[:,1]
            return self.prob
        # if not two classes assume multiclass
        else:
            self.prob = self.model.predict_proba(xs)
            return self.prob
        
    def auroc(self, targ, pred):
        # calculate auroc
        # if two classes
        if len(self.df[self.dep_var].unique())==2:
            auroc = roc_auc_score(targ, pred)
            return auroc 
        # if not two classes assume multiclass
        else:
            auroc = roc_auc_score(targ, pred, multi_class='ovo')
            return auroc                    
        
    def save(self, path): 
        path = Path(path)
        with open(path, 'wb') as file:
            pickle.dump(self.model, file)
