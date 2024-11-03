# Tìm đội bóng có chỉ số điểm số cao nhất ở mỗi chỉ số.


import pandas as pd

# Đọc dữ liệu từ file results.csv
df = pd.read_csv('results.csv')  

#chuyển dữ liệu cột 'Minutes' sang dạng số
df['Minutes'] = df['Minutes'].str.replace(',', '').astype(float)
# ta nhóm dữ liệu theo cột 'Team'
teams = df.groupby('Team')
# khởi tạo dataframe rỗng để lưu kết quả
best_teams = pd.DataFrame(columns=['Attribute', 'Best Team', 'Value'])

# lọc ra các cột chứa dữ liệu dạng số
number_columns = df.select_dtypes(include=[float, int]).columns

# Tìm đội có điểm số cao nhất cho từng chỉ số
for column in number_columns:
    # tính giá trị trung bình của mỗi đội cho cột đang xét
    best_team = teams[column].mean().idxmax()
    # trả về giá trị trung bình cao nhất của chỉ số
    best_value = teams[column].mean().max()
    
    # tạo một hàng dữ liệu mới 
    row = pd.DataFrame({'Attribute': [column], 'Best Team': [best_team], 'Value': [best_value]})
    # thêm hàng này vào best_team
    best_teams = pd.concat([best_teams, row], ignore_index=True)

#  in kết quả ra màn hình
print(best_teams)

# lưu kết quả vào file 'results_bai_2d.csv'
best_teams.to_csv('results_bai_2d.csv', index=False)

