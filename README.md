# Hierarchical-Clustering
This project implements a hierarchical agglomerative clustering algorithm from scratch using the classic Iris dataset. It also generates a dendrogram with labels colored according to the true species.

# Concepts Used
Hierarchical agglomerative clustering
Euclidean distance
Single linkage (nearest neighbor)
Dendrograms
Data manipulation with pandas

# Project Structure
.
├── iris.csv
├── main.py
└── README.md

# Requirements
Install the required dependencies:
pip install pandas matplotlib scipy

# Usage

Run the main script: python main.py
This will open a window displaying the dendrogram.

# Dataset

The iris.csv file must include the following columns:

sepal.length
sepal.width
petal.length
petal.width
variety

Example species: Setosa, Versicolor Virginica

# Visualization
Each leaf in the dendrogram represents a sample
Colors indicate the true species:
🔴 Setosa
🟢 Versicolor
🔵 Virginica

# How It Works
1. Data Loading
The CSV file is read using pandas.
2. Distance Computation
Euclidean distance is calculated between all pairs of points.
3. Minimum Search
The closest pair of points/clusters is identified.
4. Cluster Merging
Clusters are merged using single linkage.
5. Dendrogram Construction
The structure is converted into a format compatible with scipy.
6. Visualization
The dendrogram is plotted and labels are color-coded.

# Limitations
High computational complexity (~O(n³))
Not optimized for large datasets
Intended for educational purposes

# Possible Improvements
Implement:
Complete linkage
Average linkage
Optimize distance calculations
Support additional datasets
Export dendrogram as an image

# Author
Juan Carlos Garcia Jimenez
