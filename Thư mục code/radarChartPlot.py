import pandas as pd
import argparse
import matplotlib.pyplot as plt
from math import *


def radar_chart(player1, player2, attributes):
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv("results.csv")
    
    # Lấy thông tin cầu thủ
    p1_data = data[data['Name'] == player1][attributes].iloc[0].values.flatten().tolist()
    p2_data = data[data['Name'] == player2][attributes].iloc[0].values.flatten().tolist()
    
    # Chuẩn bị dữ liệu radar
    labels = attributes
    num_vars = len(labels)
    
    # Vẽ biểu đồ radar
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    p1_data += p1_data[:1]
    ax.plot(angles, p1_data, linewidth=1, linestyle='solid', label=player1)
    ax.fill(angles, p1_data, 'blue', alpha=0.1)
    
    p2_data += p2_data[:1]
    ax.plot(angles, p2_data, linewidth=1, linestyle='solid', label=player2)
    ax.fill(angles, p2_data, 'green', alpha=0.1)
    
    plt.xticks(angles[:-1], labels)
    
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', type=str, required=True)
    parser.add_argument('--p2', type=str, required=True)
    parser.add_argument('--Attribute', type=str, required=True)
    
    args = parser.parse_args()
    
    player1 = args.p1
    player2 = args.p2
    attributes = args.Attribute.split(',')
    
    radar_chart(player1, player2, attributes)


# python radarChartPlot.py --p1 "Max Aarons" --p2 "Tosin Adarabioyo" --Attribute "Matches,Starts,Minutes"
