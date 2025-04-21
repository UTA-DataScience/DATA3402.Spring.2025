import math
import scipy
import glob 
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

# Hard coded! Not great
PATH = "../Lectures/Lecture.8/"
target_files = glob.glob(PATH+"Train/*/target_train.parquet")

#print(target_files)

classification_datasets = list()
regression_datasets = list()
binary_classification_datasets = list()
multiclass_classification_datasets = list()

dataset_summary = dict()

for target_file in target_files:
    # Load Dataset
    df = pd.read_parquet(target_file)

    # Extract the name from the file path
    dataset_name = target_file.split("/")[4]

    # Get number of training datapoints
    n_train = df.shape[0]
    
    # Check the target type is float
    a_value = df[df.columns[0]].to_numpy()[0]
    float_check = isinstance(a_value,np.float64)
    
    # Check number of unique targets
    n_unique = len(np.unique(df))
    
    # Open training set, check various things
    df_train = pd.read_parquet(PATH+"Train/"+dataset_name+"/data_train.parquet")
    if df_train.shape[0] != n_train:
        print ("Warning, dataset", dataset_name, "has mismatch of train/target rows.")
        
    n_features = df_train.shape[1]
    any_null = np.any(df_train.isnull())
    
    cat_list = json.load(open(PATH+"Train/"+dataset_name+"/categorical_indicator.json","r"))
    num_cat, num_not_cat = sum(cat_list), len(cat_list)-sum(cat_list)
              
    # Lets see if we can deterimine the type of task based on the target:
    binary_classification = n_unique == 2
    multiclass_classification = n_unique < n_train/10 and not binary_classification
    regression = not binary_classification and not multiclass_classification

    if binary_classification:
        binary_classification_datasets.append(dataset_name)
        classification_datasets.append(dataset_name)
        
    if multiclass_classification:
        multiclass_classification_datasets.append(dataset_name)
        classification_datasets.append(dataset_name)
    
    if regression:
        regression_datasets.append(dataset_name)
        
    dataset_summary[dataset_name] = [dataset_name, binary_classification, 
                                     multiclass_classification, regression, n_train,
                                    any_null,n_features, num_cat, num_not_cat] 
        
# from IPython.display import HTML, display
# import tabulate

# display(HTML(tabulate.tabulate(dataset_summary.values(), tablefmt='html', 
#                                headers=["Name", "Binary", "Multi", "Regression", 
#                                         "N Train", "Any Null", "N Features", "N Cat", "N non-Cat"])))


def load_dataset(dataset_name):
    df_train = pd.read_parquet(PATH+"Train/"+dataset_name+"/data_train.parquet")
    df_target = pd.read_parquet(PATH+"Train/"+dataset_name+"/target_train.parquet")
    cat_list = json.load(open(PATH+"Train/"+dataset_name+"/categorical_indicator.json","r"))
    attrib_list = json.load(open(PATH+"Train/"+dataset_name+"/attribute_names.json","r"))
    
    return {"Training":df_train, "Target":df_target, "Categorical":cat_list, "Attributes": attrib_list}


def compare_features_binary(d,logscale=False):
    # Divide the data into separate dfs for the two categories
    
    df_0=d["Training"][(d["Target"]==0).to_numpy()]
    df_1=d["Training"][(d["Target"]==1).to_numpy()]
    
    print("Number of catogory 0:",df_0.shape[0])
    print("Number of catogory 1:",df_1.shape[0])
    
    # Make a grid of plots
    N_Features = d["Training"].shape[1]
    N_X= math.ceil(math.sqrt(N_Features))
    N_Y= math.floor(math.sqrt(N_Features))
    if N_X*N_Y<N_Features:
        N_Y+=1

    print("Found",N_Features,"features. Creating grid of",N_X,"by",N_Y)
    
    # Histogram Features
    plt.figure(figsize=(50,50))

    for i,column in enumerate(df_0.columns):
        KS_test=scipy.stats.kstest(df_0[column],df_1[column]).statistic
        print(column,"KS Distribution Similarity Test:", KS_test)
        
        plt.subplot(N_X,N_Y,i+1)
        plt.title(str(KS_test))
        if logscale:
            plt.yscale("log")
        plt.hist(df_0[column],bins=100, histtype="step", color="red",label="0",density=1, stacked=True)
        plt.hist(df_1[column],bins=100, histtype="step", color="blue",label="1",density=1, stacked=True)
        plt.legend()
        plt.xlabel(column)
        
    plt.show()