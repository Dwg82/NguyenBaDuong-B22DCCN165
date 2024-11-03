import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
data = pd.read_csv("results.csv")

# Chuẩn bị dữ liệu (từ 'Matches' đến cột cuối cùng)
fea = data.loc[:, 'Matches':]
for col in fea.columns:
    if fea[col].dtype == 'object':
        fea[col] = fea[col].str.replace(',', '').replace('N/a', np.nan).astype(float)
    else:
        fea[col] = fea[col].astype(float)
fea = fea.fillna(0)

# Phân cụm với k = 5
kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10, random_state=0)
data['Cluster'] = kmeans.fit_predict(fea)

# Giảm số chiều dữ liệu bằng PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(fea)
data_pca = pd.DataFrame(data=principal_components, columns=['P1', 'P2'])
data_pca['Cluster'] = data['Cluster']

# Vẽ biểu đồ phân cụm
plt.figure(figsize=(10,6))
plt.scatter(data_pca['P1'], data_pca['P2'], c=data_pca['Cluster'], cmap='plasma')
plt.title('PCA - Phân cụm cầu thủ')
plt.xlabel('P1')
plt.ylabel('P2')
plt.show()
