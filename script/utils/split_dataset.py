
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split


'''
    Splits the .csv file obtained in the prepare_dataset step in train.csv file and
    in a test.csv file to use in the run_model step.
'''
def split_data_test_train(dataset_csv):
    data = pd.read_csv(dataset_csv)
    train, test = train_test_split(data, test_size=0.1, random_state=0)
    #train, test = train_test_split(data, test_size=0.166666667, random_state=42)
    train.to_csv('train.csv', index=False)
    test.to_csv('test.csv', index=False)

'''
    Generates indexes for n_splits splits of the .csv file.
'''
def split_data_fold(dataset_csv, DATA_ROOT, num_splits):
    train_ids = pd.read_csv(dataset_csv).id
    kfold = KFold(n_splits = num_splits, shuffle = False, random_state = None)
    folds = [[train_ids[idx] for idx in idxs[1]] for idxs in kfold.split(train_ids)]  
    np.save(os.path.join(DATA_ROOT, 'folds.npy'), folds)
    data = np.load(os.path.join(DATA_ROOT, 'folds.npy'), allow_pickle=True)

