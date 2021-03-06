# -*- coding: utf-8 -*-
"""B20AI052_lab10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iWLT5m2918XfGKE8GMq5w3FGGwoMI60E

# PRML Lab 10

Ayush Abrol B20AI052

---

## Question 1

### Reading Data and Preprocessing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv('spambase.data', header = None)
df

headers = ['word_freq_make', 'word_freq_address', 'word_freq_all', 'word_freq_3d', 'word_freq_our', 'word_freq_over', 'word_freq_remove', 'word_freq_internet', 'word_freq_order', 'word_freq_mail', 'word_freq_receive', 'word_freq_will', 'word_freq_people', 'word_freq_report', 'word_freq_addresses', 'word_freq_free', 'word_freq_business', 'word_freq_email', 'word_freq_you', 'word_freq_credit', 'word_freq_your', 'word_freq_font', 'word_freq_000', 'word_freq_money', 'word_freq_hp', 'word_freq_hpl', 'word_freq_george', 'word_freq_650', 'word_freq_lab', 'word_freq_labs', 'word_freq_telnet', 'word_freq_857', 'word_freq_data', 'word_freq_415', 'word_freq_85', 'word_freq_technology', 'word_freq_1999', 'word_freq_parts', 'word_freq_pm', 'word_freq_direct', 'word_freq_cs', 'word_freq_meeting', 'word_freq_original', 'word_freq_project', 'word_freq_re', 'word_freq_edu', 'word_freq_table', 'word_freq_conference', 'char_freq_;', 'char_freq_(', 'char_freq_[', 'char_freq_!', 'char_freq_$', 'char_freq_#', 'capital_run_length_average', 'capital_run_length_longest', 'capital_run_length_total', 'spam']

df.columns = headers
df

values, counts = np.unique(df['spam'], return_counts=True)
print(values, counts)
print("Here 1 represents Spam and 0 represents Non-Spam mails")

"""### Normalizing the data"""

X, y = df.iloc[:,:-1], df.iloc[:,-1]
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)
X = pd.DataFrame(X, columns=headers[:-1])
X

"""### Splitting the dataset into 70:30 ratio"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

"""### Principal component Analysis for visualizing the dataset with reduced dimensions"""

from sklearn.decomposition import PCA
pca = PCA(n_components=3)
X_train_pca = pca.fit_transform(X_train)
X_train_pca = pd.DataFrame(X_train_pca, columns=['Pca 1', 'Pca 2', 'Pca 3'])
X_train_pca = X_train_pca.join(y_train)
X_test_pca = pca.transform(X_test)
X_test_pca = pd.DataFrame(X_test_pca, columns=['Pca 1', 'Pca 2', 'Pca 3'])
X_test_pca = X_test_pca.join(y_test)

import seaborn as sns
sns.set(style="ticks")
sns.set(style="whitegrid", color_codes=True)
sns.pairplot(X_train_pca, hue='spam', palette='rainbow')

"""### Using kernel = poly with degree = 2 (Quadratic) for finding the best fit line for best accuracy"""

C_vals_quad = []
scores_quad = []
for C in range(1, 100):
    clf = SVC(kernel='poly', degree = 2, C = C)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    score = accuracy_score(y_test, preds)
    scores_quad.append(score)
    C_vals_quad.append(C)

plt.figure(figsize=(20,10))
plt.title('Accuracy vs C values for quadratic kernel C [1,99]')
plt.xlabel('C values')
plt.ylabel('Accuracy for quadratic kernel')
plt.plot(C_vals_quad, scores_quad, marker='*', c = 'red')
plt.show()

max_quad = scores_quad.index(max(scores_quad))
C_quad_max = C_vals_quad[max_quad]
print('The best C value for quadratic kernel is:', C_quad_max, "with accuracy:", max(scores_quad))

"""### Using kernel = rbf (Radial Basis function) for finding the best fit line for best accuracy"""

C_vals_rbf = []
scores_rbf = []
for C in range(1, 100):
    clf = SVC(kernel='rbf', C = C)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    score = accuracy_score(y_test, preds)
    scores_rbf.append(score)
    C_vals_rbf.append(C)

plt.figure(figsize=(20,10))
plt.title('Accuracy vs C values for rbf kernel C [1,99]')
plt.xlabel('C values')
plt.ylabel('Accuracy for Radial basis function kernel,')
plt.plot(C_vals_rbf, scores_rbf, marker='*', c = 'red')
plt.show()

max_rbf = scores_rbf.index(max(scores_rbf))
C_rbf_max = C_vals_rbf[max_rbf]
print('The best C value for rbf kernel is:', C_rbf_max, "with accuracy:", max(scores_rbf))

"""### Using kernel = linear for finding the best fit line for best accuracy"""

C_vals_lin = []
scores_lin = []
for C in range(1, 100):
    clf = SVC(kernel='linear', C = C)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    score = accuracy_score(y_test, preds)
    scores_lin.append(score)
    C_vals_lin.append(C)

plt.figure(figsize=(20,10))
plt.title('Accuracy vs C values for linear kernel C [1,99]')
plt.xlabel('C values')
plt.ylabel('Accuracy for linear kernel')
plt.plot(C_vals_lin, scores_lin, marker='*', c = 'red')
plt.show()

max_lin = scores_lin.index(max(scores_lin))
C_lin_max = C_vals_lin[max_lin]
print('The best C value for linear kernel is:', C_lin_max, "with accuracy:", max(scores_lin))

"""### Creating a comparison table for the accuracies obtained from above three methods"""

def comparisonTable(C_lin_max, C_quad_max, C_rbf_max, max_lin, max_quad, max_rbf):
    d_table = pd.DataFrame({'Kernel': ['Linear', 'Quadratic', 'rbf'],
                    'C': [C_lin_max, C_quad_max, C_rbf_max],
                    'Accuracy': [max_lin, max_quad, max_rbf]})

    return d_table              

table = comparisonTable(C_lin_max, C_quad_max, C_rbf_max, max(scores_lin), max(scores_quad), max(scores_rbf))
table