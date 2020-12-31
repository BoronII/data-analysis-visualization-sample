import pandas as pd

from SKClassifier           import SKClassifier
from fastai.tabular.all     import TabularPandas, Categorify, FillMissing
from sklearn.ensemble       import RandomForestClassifier


if __name__=='__main__':
    
    TRAIN = pd.read_csv('../data/processed_data/turkey_political_opinions_processed.csv',
                        low_memory=False)

    # Categorical features
    CAT = ['Sex', 'Age', 'City', 'Education level', 'Q1', 'Q2', 'Q3',
       'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
   
    # Target feature
    DEP_VAR = 'Political View'

    assert len(CAT)==(len(TRAIN.columns)-1)
    
    # Data processing procedures
    # Categorify replaces categorical columns with numerical categorical columns. 
    # FillMissing replaces missing values with the median of the column and 
    # creates a new Boolean column that records whether data was missing.
    PROCS = [Categorify, FillMissing]
    
    model = RandomForestClassifier(n_jobs=-1, max_samples=2/3,
                            oob_score=True, max_features='sqrt',
                            n_estimators=1000, criterion='entropy',
                            max_leaf_nodes=750, min_samples_split=30, min_samples_leaf=5)
   
    clf = SKClassifier(model, TRAIN, CAT, DEP_VAR, PROCS)
    
    clf.process_df(test_size=0.1, save_as='turkey_political_opinions_to.pkl')

    xs, y             = clf.xs,       clf.y
    valid_xs, valid_y = clf.valid_xs, clf.valid_y
    
    clf.fit(xs, y)
   
    train_preds = clf.predict_proba(xs)
    valid_preds = clf.predict_proba(valid_xs)
    
    train_auroc = clf.auroc(y, train_preds)
    print(f'Train_AUROC: {train_auroc}')
    
    valid_auroc = clf.auroc(valid_y, valid_preds)
    print(f'Valid_AUROC: {valid_auroc}')

    clf.save('models/RF_model.pkl')
    
    
   
