# Tìm trung vị của mỗi chỉ số. Tìm trung bình và độ lệch chuẩn của mỗi chỉ số cho các cầu thủ trong toàn
# giải và của mỗi đội. Ghi kết quả ra file results2.csv



import pandas as pd


# Đọc dữ liệu từ file 'results.csv'
data = pd.read_csv("results.csv")

#chuyển dữ liệu cột 'Minutes' sang dạng số
data['Minutes'] = data['Minutes'].str.replace(',', '').astype(float)
# Chọn các cột chỉ chứa dữ liệu số (các cột chỉ số cần phải tính)
number_attributes = data.select_dtypes(include=[float, int]).columns

# Khởi tạo từ điển kết quả với cột "Team"
results = {"Team": ["all"]}

# Tính trung vị, trung bình và độ lệch chuẩn cho từng chỉ số cho cả giải đấu
for x in number_attributes:

    results[f"Median of {x}"] = [f"{data[x].median(skipna=True):.2f}"]  
    results[f"Mean of {x}"] = [f"{data[x].mean(skipna=True):.2f}"]      
    results[f"Std of {x}"] = [f"{data[x].std(skipna=True):.2f}"]        

# Nhóm dữ liệu theo từng đội bóng và tính trung vị, trung bình, độ lệch chuẩn cho từng đội
for team, group in data.groupby("Team"):
    results["Team"].append(team)
    for x in number_attributes:
        results[f"Median of {x}"].append(f"{group[x].median(skipna=True):.2f}")
        results[f"Mean of {x}"].append(f"{group[x].mean(skipna=True):.2f}")
        results[f"Std of {x}"].append(f"{group[x].std(skipna=True):.2f}")

# Chuyển kết quả thành DataFrame
results_df = pd.DataFrame(results)

# Lưu kết quả vào file 'results2.csv' 
results_df.to_csv("results2.csv", index=False)



