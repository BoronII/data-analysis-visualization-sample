import pandas as pd
import numpy  as np

from pathlib import Path


# All of these will be implemented as methods in the class

# Common steps in preprocessing:
# 1. Drop cols (list of to_drop columns)
# 2. Drop rows that have nan values in a particular column
# 3. Rename entries in a column from a dict
# 4. Rename columns from a dict
# 5. Functionality to use the same dict for a list of columns
# 6. Save and return processed data frames

# Tests
# 1. check to make sure that columns have Nans in the same places before and after renaming
# 2. check that there are no more nans after the dropna

class Preprocessor:

    def __init__(self, df):
        self.df      = df
        self.columns = df.columns
       
    def drop(self, columns):
        self.df.drop(columns=columns, inplace=True)
        return self.df
    
    def dropna(self, subset):
        self.df.dropna(subset=subset, inplace=True)
        for col in subset:
            assert self.df[col].isna().sum()==0
        return self.df

    def map(self, columns, dict):
   
        if len(columns)==len(dict):
            for col in columns:
                temp = self.df[col]
                self.df[col] = self.df[col].map(dict[col])
                assert np.all(self.df[col].isna()==temp.isna())
            return self.df
        
        else:
            for col in columns:
                temp = self.df[col]
                self.df[col] = self.df[col].map(dict)
                assert np.all(self.df[col].isna()==temp.isna())
            return self.df  
        assert np.all(df['Income_Group'].isna()==df['Income_Group'].isna())
 

    def map_cols(self, dict):
        self.df.columns = self.df.columns.map(dict)
        self.columns = self.df.columns
        return self.df
 
    def save(self, fname):
    # Save the data frame contained in self.df to csv
        self.df.to_csv(fname, index=False)
		
	
	



