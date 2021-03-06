# -*- coding: utf-8 -*-
"""B20AI052_lab9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LRduQgzrcmwWeVo0vavfe9JQQbneHub1

# PRML Lab 9
    Ayush Abrol B20AI052
---

## Question 1

### Reading and preprocessing of data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('wine.data', header=None)
df

attribute_names = ['Classes', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols', 'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue', 'OD280/OD315 of diluted wines', 'Proline']
df.columns = attribute_names
df

df.info()

df.describe()

unscaled_columns = ['Malic acid', 'Alcalinity of ash', 'Magnesium', 'Total phenols', 'Flavanoids', 'Proanthocyanins', 'Color intensity', 'OD280/OD315 of diluted wines', 'Proline']

scalar = StandardScaler()
for i in unscaled_columns:
    df[i] = scalar.fit_transform(df[i].values.reshape(-1, 1))

df

values, counts = np.unique(df['Classes'], return_counts=True)
print(values, counts)

sns.pairplot(df, hue='Classes', vars=['Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols', 'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue', 'OD280/OD315 of diluted wines', 'Proline'])

X = df.iloc[:, 1:].values
y = df.iloc[:, 0].values

# Manually encoding the classes

for i in range(len(y)):
    if y[i] == 3:
        y[i] = 0
    elif y[i] == 2:
        y[i] = 1
    elif y[i] == 1:
        y[i] = 2

"""### Use any dimension reduction technique of your choice, visualize the data and by looking at the plot tell which value of k will be best suited for k-means clustering"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

"""### Using PCA"""

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

X_pca[0:5]

sns.scatterplot(X_pca[:, 0], X_pca[:, 1], hue=y, palette='rainbow')

"""### Using LDA"""

lda_model = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda_model.fit_transform(X, y)

X_lda[0:5]

sns.scatterplot(X_lda[:, 0], X_lda[:, 1], hue=y, palette='rainbow')

"""The value of K is found to be 3

### Build a k-means clustering algorithm( can use sklearn library) and implement using the value of k = 3
"""

kmeans = KMeans(n_clusters=3, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
y_kmeans = kmeans.fit_predict(X_lda)

print("True Class Labels :- ")
print(y)

print("Predicted Class labels :- ")
print(kmeans.labels_)

"""### Visualize part b by showing the clusters along with the centroids."""

plt.figure(figsize=(10,5))
plt.scatter(X_lda[y_kmeans == 0, 0], X_lda[y_kmeans == 0, 1], s = 100, c = 'red',)
plt.scatter(X_lda[y_kmeans == 1, 0], X_lda[y_kmeans == 1, 1], s = 100, c = 'orange')
plt.scatter(X_lda[y_kmeans == 2, 0], X_lda[y_kmeans == 2, 1], s = 100, c = 'green')

#Plotting the centroids of the cluster
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], s = 100, c = 'black', label = 'Centroids')

plt.legend()

"""### Use different values of k and find the Silhouette Score and then tell which value of k will be optimal and why?"""

from sklearn.metrics import silhouette_score

list = [int(i) for i in range(2, 11)]
silhouette = []

for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    y_kmeans = kmeans.fit_predict(X_lda)
    new_score = silhouette_score(X_lda, y_kmeans, metric='euclidean')
    silhouette.append(new_score)
print(silhouette)

plt.plot(list, silhouette)
plt.show()

"""### There are few methods to find the optimal k value for k-means algorithm like the Elbow Method . Use the above method to find the optimal value of k."""

from scipy.spatial.distance import cdist
 
distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 10)
 
for k in K:
    # Building and fitting the model
    kmeanModel = KMeans(n_clusters=k, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    kmeanModel.fit(X_lda)
 
    distortions.append(sum(np.min(cdist(X_lda, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / X_lda.shape[0])
    inertias.append(kmeanModel.inertia_)
 
    mapping1[k] = sum(np.min(cdist(X_lda, kmeanModel.cluster_centers_,
                                   'euclidean'), axis=1)) / X_lda.shape[0]
    mapping2[k] = kmeanModel.inertia_

plt.plot(K, distortions, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Distortion')
plt.title('The Elbow Method using Distortion')
plt.show()

plt.plot(K, inertias, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Inertia')
plt.title('The Elbow Method using Inertia')
plt.show()

"""## Question 2

### Reading Data and preprocessing
"""

mnist_train_data = pd.read_csv('fashion-mnist_train.csv')
mnist_train_data

mnist_test_data = pd.read_csv('fashion-mnist_test.csv')
mnist_test_data

mnist_train_data.describe()

mnist_test_data.describe()

print(mnist_train_data.shape)
print(mnist_test_data.shape)

mnist_train_data_X = mnist_train_data.iloc[:, 1:].values
mnist_train_data_y = mnist_train_data.iloc[:, 0].values
mnist_test_data_X = mnist_test_data.iloc[:, 1:].values
mnist_test_data_y = mnist_test_data.iloc[:, 0].values

print(mnist_train_data_X.shape)
print(mnist_train_data_y.shape)
print(mnist_test_data_X.shape)
print(mnist_test_data_y.shape)

"""### Implement a k-means clustering algorithm from scratch.

* Class which will be able to store the cluster centers.
* Take a value of k from users to give k clusters.
* Able to take initial cluster center points from the user as its initialization.
* Stop iterating when it converges (cluster centers are not changing anymore) or, a maximum iteration (given as max_iter by user) is reached.
"""

class Kmeans_from_scratch:
    def __init__(self, k, max_iter = 300, n_init = 10, random_state=0):
        self.k = k
        self.max_iter = max_iter
        self.n_init = n_init
        self.random_state = random_state
        self.centroids = None
        self.labels = None
        
    def fit(self, X):
        self.centroids = self.init_centroids(X)
        self.labels = np.zeros(X.shape[0])
        for i in range(self.n_init):
            self.labels = self.assign_labels(X)
            self.centroids = self.update_centroids(X)

        num = 1
        while num < self.max_iter:
            centroids_old = self.centroids
            self.labels = self.assign_labels(X)
            self.centroids = self.update_centroids(X)
            if np.array_equal(centroids_old, self.centroids):
                break
            num += 1

        return self
    
    def init_centroids(self, X):
        centroids = np.zeros((self.k, X.shape[1]))
        for i in range(self.k):
            centroids[i] = X[np.random.randint(X.shape[0])]
        return centroids
    
    def assign_labels(self, X):
        labels = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            distances = np.linalg.norm(X[i] - self.centroids, axis=1)
            labels[i] = np.argmin(distances)
        return labels
    
    def update_centroids(self, X):
        new_centroids = np.zeros((self.k, X.shape[1]))
        for i in range(self.k):
            new_centroids[i] = np.mean(X[self.labels == i], axis=0)
        return new_centroids

k = int(input("Enter the number of clusters: "))
n_init = int(input("Enter the initial cluster center points: "))

"""### Train the k-means model on f-MNIST data with k = 10 and 10 random 784 dimensional points (in input range) as initializations."""

model_kmeans = Kmeans_from_scratch(k = k, max_iter = 300, n_init = n_init)
model_kmeans = model_kmeans.fit(mnist_train_data_X)

centroids = model_kmeans.centroids
centroids.shape

labels = model_kmeans.labels
labels.shape

print(labels)
print(len(labels))
print("The labels of the clusters are " + str(np.unique(labels)))

label_dict = {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat', 5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'}

print(mnist_train_data_y.shape)
unique_labels = np.unique(labels)
unique_labels = unique_labels.tolist()
for i in range(len(unique_labels)):
    unique_labels[i] = int(unique_labels[i])
print(unique_labels)

"""### Reporting the number of points in each cluster."""

num_cluster = len(np.unique(labels))

cluster_indexes = [[] for i in range(num_cluster)]

for i,label in enumerate(labels):
    for n in range(num_cluster):
        if label == n:
            cluster_indexes[n].append(i)
        else:
            continue

print('After Clustering\n')
for i in range(num_cluster):
    print('No. of items in Cluster ' + str(i) + ': ' + str(len(cluster_indexes[i])))

"""### Visualize the cluster centers of each cluster as 2-d images of all clusters."""

# Visualize the cluster centers of each cluster as 2-d images of all clusters.
def visualizing_clusters(X, centroids, labels):
    num_cluster = len(np.unique(labels))
    cluster_indexes = [[] for i in range(num_cluster)]
    for i,label in enumerate(labels):
        for n in range(num_cluster):
            if label == n:
                cluster_indexes[n].append(i)
            else:
                continue
   
    for j in range(len(cluster_indexes)):
        plt.figure(figsize=(3,3))
        val = X.iloc[cluster_indexes[j][0],:]
        val = val.values
        val = val.reshape(28, 28)
        plt.imshow(val, cmap='magma')
        plt.title('Cluster ' + str(j))
        plt.show()
X_f = pd.DataFrame(mnist_train_data_X)
visualizing_clusters(X_f, centroids, labels)

"""### Visualize 10 images corresponding to each cluster."""

def visualizing_clusters_10(X, centroids, labels):
    num_cluster = len(np.unique(labels))
    cluster_indexes = [[] for i in range(num_cluster)]
    for i,label in enumerate(labels):
        for n in range(num_cluster):
            if label == n:
                cluster_indexes[n].append(i)
            else:
                continue
   
    for j in range(len(cluster_indexes)):
        plt.figure(figsize=(10,10))
        for i in range(10):
            plt.subplot(2,5,i+1)
            val = X.iloc[cluster_indexes[j][i],:]
            val = val.values
            val = val.reshape(28, 28)
            plt.imshow(val, cmap='inferno')
            plt.title('Cluster ' + str(j))
        plt.show()    

visualizing_clusters_10(X_f, centroids, labels)

"""### Train another k-means model with 10 images from each class as initializations,  report the number of points in each cluster and visualize the cluster centers."""

kmeanModel_2 = Kmeans_from_scratch(k = 10, max_iter = 300, n_init = 10)
kmeanModel_2 = kmeanModel_2.fit(mnist_train_data_X)
centroids_2 = kmeanModel_2.centroids
labels_2 = kmeanModel_2.labels

num_cluster_2 = len(np.unique(labels_2))

cluster_indexes_2 = [[] for i in range(num_cluster_2)]

for i, label in enumerate(labels_2):
    for n in range(num_cluster_2):
        if label == n:
            cluster_indexes_2[n].append(i)
        else:
            continue

print('After 2nd Model Training from Clustering\n')
for i in range(num_cluster_2):
    print('No. of items in Cluster ' + str(i) + ': ' + str(len(cluster_indexes_2[i])))

visualizing_clusters(X_f, centroids_2, labels_2)

"""### Visualize 10 images corresponding to each cluster."""

visualizing_clusters_10(X_f, centroids_2, labels_2)

"""### Visualizing number of images in each cluster."""

def cluster_visualization_using_bar_graphs(X, centroids, labels):
    num_cluster = len(np.unique(labels))
    cluster_indexes = [[] for i in range(num_cluster)]
    for i,label in enumerate(labels):
        for n in range(num_cluster):
            if label == n:
                cluster_indexes[n].append(i)
            else:
                continue

    plt.bar(np.arange(num_cluster), [len(cluster_indexes[i]) for i in range(num_cluster)])
    plt.xticks(np.arange(num_cluster), [str(i) for i in range(num_cluster)])
    plt.xlabel('Cluster')
    plt.ylabel('Number of Images')
    plt.title('Number of Images in Each Cluster')
    plt.show()

cluster_visualization_using_bar_graphs(X_f, centroids, labels)
cluster_visualization_using_bar_graphs(X_f, centroids_2, labels_2)

"""### Evaluate Clusters of part c and part f with Sum of Squared Error (SSE) method."""

def Sum_Squared_Means(data, centroid, label):
    data = data.to_numpy()

    sum_error = 0
    for i in range(len(centroid)):
        for j in range(len(data[label==i])):
            sum_error += (np.sum(data[label==i] - centroid[i]))**2

    return np.sum(sum_error)

"""# Question 3

### Reading Data and preprocessing
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import cv2
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import Normalizer
from sklearn.metrics import accuracy_score as acc 
from sklearn.decomposition import PCA

df = []
path = 'yesno'
for image in os.listdir(path):
    img = cv2.imread(os.path.join(path, image))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if 'y' in image.lower():
        df.append(np.append(cv2.resize(gray_img,(128,128)).flatten(),0))
    if 'n' in image.lower():
        df.append(np.append(cv2.resize(gray_img,(128,128)).flatten(),1))

df = pd.DataFrame(np.array(df))

df

X_df = df.iloc[:,:-1]
y_df = df.iloc[:,-1]

"""### Use any dimension reduction technique and visualize the dataset & find out the number of communities available."""

normalizer = Normalizer()
X_df = normalizer.fit_transform(X_df)

pca = PCA(n_components=2)
X_df = pca.fit_transform(X_df)

X_df.shape

"""### Visualize the communities from part A."""

plt.scatter(X_df[:,0], X_df[:,1], c=y_df)

yes = X_df[y_df==0]
no = X_df[y_df==1]

"""### Apply Agglomerative hierarchical clustering (using sklearn)."""

clusterer = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
clusterer.fit(X_df)
preds = clusterer.labels_
print(acc(y_df, preds))

"""### Apply K-means (sklearn) and make a comparison between these two approaches"""

from sklearn.cluster import KMeans
kmeans_cluster = KMeans(n_clusters=2, max_iter=300, n_init=10)
kmeans_cluster.fit(X_df)
preds = kmeans_cluster.labels_
print(acc(y_df, preds))