"""Module with class definitions for performing EDA."""

from istart import *
from pandas.plotting import scatter_matrix
import seaborn as sns
from pprint import *

def disp(data, nrows=5):
    '''Display shape and top rows of the data'''
    print("Shape of the data -", data.shape)
    display(data.head(nrows))

def missing_cols_removal(data, proportion=.4):
    '''Remove columns with a lot of missing values'''
    proportion = 0.4
    cols = [i for i in data.columns[data.isna().sum()/data.shape[0]<proportion]]
    print('Count of columns with less than %d percent missing values is -' %(proportion*100), len(cols), 
         '\nTotal columns were - ', data.shape[1])
    if input("wanna see the remaining column names? (press 'Y' for yes)- ") == "Y":
        pprint(cols, compact=True)
    print()
    disp(data[cols])
    return data[cols]
    
    
def num_conversion(df_series):
    '''Convert non-numeric pandas series to numeric'''
    try:
        num_series = pd.to_numeric(df_series, errors='raise')
        print('Successfully converted to numeric!')
        return num_series
    except ValueError:
        print('Non numeric value distribution is as below:')
        display(df_series[~(df_series.str.isnumeric())].value_counts())
        check = input('Shall I coerce all of these? (Press \'Y\' for Yes) - ')
        if check == 'Y':
            num_series = pd.to_numeric(df_series, errors='raise')
            print('Successfully converted to numeric!')
            return num_series


def num_conversion(df_series,brute_force=True,verbose=True):
    '''Convert non-numeric pandas series to numeric'''
    try:
        num_series = pd.to_numeric(df_series, errors='raise')
        if verbose:
            print('Successfully converted to numeric!')
        return num_series
    except ValueError:
        if verbose:
            print('Non numeric value distribution is as below-')
        non_num = df_series[~(df_series.str.isnumeric().fillna(True))]
        if verbose:
            display(non_num.value_counts())
        if brute_force and non_num.nunique() < 15 :
            num_series = df_series.str.extract('(^\d*)')[0]
            if verbose:
                print('Successfully converted to numeric using regex extraction of numbers. Example - ')
                df = pd.concat([df_series,num_series],1)
                df.columns=['Old Values','New Values']
                display(df[~(df.iloc[:,0].str.isnumeric().fillna(True))].drop_duplicates()[:10])
            return pd.to_numeric(num_series,errors='raise')
        else:
            print('Did not convert to numeric')
    except:
        print('Did not convert to numeric')
        
        

def drop_low_var_columns(dataframe, nunique=1):
    '''Drop columns with number of unique values less than specified'''
    colnames = [col for col in dataframe.columns if dataframe[col].nunique()<=nunique]
    print("Columns dropped because of containing <= %d unique values - \n" %nunique,colnames)
    return dataframe.drop(colnames,1)

def categ_eda_df(dataframe, target_column='y', limit_unique = 10):
    '''Categorical EDA: Return dataframe containing unique categories, their value counts 
    and mean of the target variable sorted according to the target variable'''
    eda_df = pd.DataFrame()
    categ_cols = [col for col in dataframe.columns if dataframe[col].nunique()<=limit_unique]
    print('Selected columns:\n',categ_cols)
    for col in categ_cols:
        try:
            temp_df = pd.DataFrame(dataframe[col].value_counts())
            temp_df.index.name = col
            temp_df = temp_df.join(dataframe.groupby(col)[[target_column]].mean())
            temp_df.columns = ['#Occurances','%s_mean' %target_column]
            temp_df = temp_df.sort_values('%s_mean' %target_column).reset_index()
            temp_df = temp_df[[col,'#Occurances','%s_mean' %target_column]].T.reset_index()
            temp_df.index = [col,col,col]
            eda_df = eda_df.append(temp_df)
        except:
            print("**Couldn't do for ", col)
    return eda_df
    



def bar_plot(df, x, y, figsize=(20, 25), **kwargs):
    ax = df.plot.barh(
        x=x, y=y, figsize=figsize, **kwargs)
    ax.set_title(title + f" - Shape of Data {df.shape}")
    plt.show()

class NullsAnalyzer():
    """
    Analyzer of Null counts.
    >>> nulls_analyzer = NullsAnalyzer(df)
    >>> nulls_analyzer.plot(title="Example plot")
    """
    def __init__(self, df, null_value=None):
        self.df = df
        if null_value is None:
            self.nulls_df = pd.DataFrame(self.df.isnull().sum())
        else:
            self.nulls_df = pd.DataFrame(self.df.eq(null_value).sum())
        self.nulls_df["cols"] = self.nulls_df.index
        self.nulls_df["nulls"] = self.nulls_df[0]
        self.nulls_df.sort_values(by=['cols'], inplace=True)
    
    def plot(self, title="", **kwargs):
        bar_plot(self.nulls_df, x="cols", y="nulls")

    def summary(self):
        return self.nulls_df[["nulls"]]

class CategoricalAnalyzer():
    """
    Analyzer for Categorical Variables.
    
    >>> scatter_analyzer = CategoricalAnalyzer(df)
    >>> scatter_analyzer.plot("column1", "column2", title="Example plot")
    """
    def __init__(self, df):
        self.df = df

    def plot(
        self, x, y, title="", xlim=(-100, 100), vline=0, vlines=[],
        figsize=(20, 20), palette="Set3", inner="quartile", **kwargs):
        plt.figure(figsize=figsize)
        ax = sns.violinplot(
            x=x, y=y,
            data=self.df,
            palette=palette,
            inner=inner,
            **kwargs
        )
        ax.set_xlim(*xlim)
        plt.axvline(vline)
        for vline in vlines:
            plt.axvline(vline, color='r', linestyle='--')
        ax.set_title(title + f" - Shape of Data {self.df.shape}")
        plt.show()
        
class ScatterAnalyzer():
    """
    Analyzer for Numeric Variable non-monotonic correlations.
    
    >>> scatter_analyzer = ScatterAnalyzer(df)
    >>> scatter_analyzer.plot(title="Example plot")
    """
    def __init__(self, df):
        self.df = df

    def plot(self, alpha=0.2, figsize=(20, 20), **kwargs):
        scatter_matrix(
            self.df, alpha=alpha,# ax=ax,
            figsize=figsize, diagonal='kde'
        )
        plt.show()

class NumericAnalyzer():
    """
    Analyzer for Numeric Variable correlations.
    
    >>> numeric_analyzer = NumericAnalyzer(df)
    >>> numeric_analyzer.plot(title="Example plot")
    """
    def __init__(self, df):
        self.df = df
    
    def plot(self, method="pearson", title="", figsize=(20,20), cmap="YlGnBu", annot=True, **kwargs):
        corr_data = self.df.corr(method=method)
        plt.figure(figsize=figsize)
        ax = sns.heatmap(corr_data, center=0, cmap=cmap, annot=annot, **kwargs)
        ax.set_title(title + f" - Shape of Data {self.df.shape}")
        plt.show()
        
        
        
