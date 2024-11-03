import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# Đọc dữ liệu 
data = pd.read_csv("results.csv")

# Chuẩn bị dữ liệu (giả sử các cột từ 'Matches' đến cột cuối cùng)
fea = data.loc[:, 'Matches':]
for col in fea.columns:
    if fea[col].dtype == 'object':
        fea[col] = fea[col].str.replace(',', '').replace('N/a', np.nan).astype(float)
    else:
        fea[col] = fea[col].astype(float)
fea = fea.fillna(0)

# Tìm k tối ưu bằng phương pháp Elbow
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(fea)
    wcss.append(kmeans.inertia_)
    

# Vẽ biểu đồ Elbow
plt.plot(range(1, 11), wcss,marker='o')
plt.title('Elbow Method')
plt.xlabel('Số lượng cụm')
plt.ylabel('WCSS')
plt.xticks(range(1, 11))  # Đảm bảo hiện tất cả các giá trị k trên trục x
plt.show()
