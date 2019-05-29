import numpy as np
import pandas as pd
import glob
print('imported pandas as pd, numpy as np and glob')

def convert_txt():
    '''automatically read all the txt files present in currect working directory and convert to xlsx'''
    txts = glob.glob("*txt")
    for i in txts:
        x = pd.read_csv(i, sep="|")
        x.to_excel(i[:-3]+"xlsx")
        print("Success with ", i, "\nShape: ", x.shape, '\n')

def guess_name(name):
    '''automatically considers the desired file name from the provided hint'''
    li = glob.glob('*'+name+'*')
    if   len(li) == 0 : print('no such file')
    elif len(li) != 1 : print('Give more specific name-\n', li)
    else: file = li[0]; print(file); return file


def read_data(name, rows=5):
    '''automatically reads the desired file and returns as a pandas df from the provided name regex'''
    file = guess_name(name)
    if type(file) == str:
        endin = file[len(file)-4:][file[len(file)-4:].find('.')+1:]
        if endin=='pkl':
            a = pd.read_pickle(file)
            print("Shape:", a.shape, display(a.head(rows)))
            return a
        elif endin =='csv':
            a = pd.read_csv(file, encoding='latin')
            print("Shape:",a.shape, display(a.head(rows)))
            return a
        elif endin =='xlsx':
            a = pd.read_excel(file)
            print("Shape:",a.shape, display(a.head(rows)))
            return a
        elif endin =='txt':
            a = pd.read_csv(file, sep = '|')
            print("Shape:",a.shape, display(a.head(rows)))
            return a
        else:
            print(endin, 'type is yet not supported')
