import pandas as pd
import numpy  as np

# All of these will be implemented as methods in the class

# Common steps in preprocessing:
# 1. Drop cols (list of to_drop columns) 
# 2. Drop rows that have nan values in a particular column 
# 3. Rename entries in a column from a dict
# 4. Rename columns from a dict
# 5. Functionality to use the same dict for a list of columns
# 6. Save and return processed data frames
# All operations are done inplace

# Tests
# 1. Check to make sure that columns have Nans in the same places before and after renaming
# 2. Check that there are no more nans after the dropna

class Preprocessor:
    """
    A class to streamline the performance of common preprocessing steps and to
    integrate these with testing. 

    ...

    Attributes
    ----------
    df : pandas dataframe
        the dataframe 
    columns : list(str)
        list containing the columns of the df attribute
   
    Methods
    -------
    drop(columns):
        drops a list of columns inplace.
    
    dropna(subset):
        drops all rows that have nan values in a subset of the columns.
    
    map(columns, mappers):
        remaps the given list of columns using the mappers provided in 
        a dictionary of mappers.
    
    map_cols(mapper):
        renames  the columns of the data set using the provided mapper (a dict).
    
    save(path):
        saves the processed dataframe to the provided path.
        the index column is dropped.
    """

    def __init__(self, df):
        self.df      = df
        self.columns = df.columns
       
    def drop(self, columns):
        """drops a list of columns inplace.
        
        Parameters
        ----------
        columns : list
            List of columns to drop.
        
        Returns
        -------
        self.df : pandas dataframe
            The dataframe with columns dropped.
        """
        self.df.drop(columns=columns, inplace=True)
        self.columns = self.df.columns
        return self.df
    
    def dropna(self, subset):
        """drops all rows that have nan values in a subset of the columns.
       
        Parameters
        ----------
        subset : list
            List of columns to check for nan values when diciding if a row will
            be dropped.
        
        Returns
        -------
        self.df : pandas dataframe
            The dataframe with rows that have nan values in the prescribed
            subset dropped.
        """
        self.df.dropna(subset=subset, inplace=True)
        for col in subset:
            assert self.df[col].isna().sum()==0
        return self.df

    def map(self, columns, mappers):
        """remaps the given list of columns using the mapper or mappers 
        provided in a dictionary of mappers.
        
        Parameters
        ----------
        columns : list
            List of columns with entries that are to be remapped.
        
        mappers : dict or dict of dicts
            A dict containing a mapper that will be used for every column or
            a dict of dicts containing a unique mapper for each column.
        
        Returns
        -------
        self.df : pandas dataframe
            The dataframe with columns entries remapped according to the mappers.
        """
        if len(columns)==len(mappers):
            for col in columns:
                temp = self.df[col].isna()
                self.df[col] = self.df[col].map(mappers[col])
                assert np.all(temp==self.df[col].isna()), f'error with column: {col}'
            return self.df
        
        else:
            for col in columns:
                temp = self.df[col]
                self.df[col] = self.df[col].map(mappers)
                assert np.all(self.df[col].isna()==temp.isna())
            return self.df   

    def map_cols(self, mapper):
        """renames  the columns of the data set using the provided mapper (a dict).
        
        Parameters
        ----------
        mapper : dict
            A dict prescribing how each column is to be renamed.
        
        Returns
        -------
        self.df : pandas dataframe
            The dataframe with columns renamed according to the mapper.
        """
        self.df.columns = self.df.columns.map(mapper)
        self.columns = self.df.columns
        return self.df
 
    def save(self, path):
        """saves the processed dataframe to the provided path.
        the index column is dropped.
        
        Parameters
        ----------
        path : string or pathlike object
            The path where the processed dataframe is saved.
        """
        self.df.to_csv(path, index=False)
		
	
	



