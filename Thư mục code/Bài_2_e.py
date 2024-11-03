# Theo bạn đội nào có phong độ tốt nhất giải ngoại Hạng Anh mùa 2023-2024



import pandas as pd

# Đọc dữ liệu từ file results.csv
df = pd.read_csv('results.csv')
teams = df.groupby('Team')

# Các chỉ số tấn công và phòng ngự
attack_metrics = ['non_penalty_goals', 'penalty_goals', 'assists', 'xG', 'npxG', 'xAG', 'per90_Gls', 'per90_Ast', 'per90_G+A']
defensive_metrics = ['Tkl', 'TklW', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Challenges_Tkl', 'Blocks', 'Blocks_Sh', 'Blocks_Pass']

# Tính trung bình các chỉ số tấn công và phòng ngự cho từng đội
team_attack_performance = teams[attack_metrics].mean().mean(axis=1)
team_defensive_performance = teams[defensive_metrics].mean().mean(axis=1) / 100

# Tạo bảng tổng hợp điểm phong độ
team_performance = pd.DataFrame({
    'Attack Performance': team_attack_performance,
    'Defensive Performance': team_defensive_performance
})

# Tính điểm phong độ chung bằng trung bình cộng của điểm tấn công và phòng ngự
team_performance['Overall Performance'] = team_performance.mean(axis=1)

# Sắp xếp theo thứ tự giảm dần của điểm phong độ chung
team_performance = team_performance.sort_values(by='Overall Performance', ascending=False)

# Lưu kết quả vào file results_bai_2e.csv
team_performance.to_csv('results_bai_2e.csv')

# In ra toàn bộ điểm phong độ tấn công, phòng ngự và điểm phong độ chung của từng đội bóng

print(team_performance)

# Tìm đội có phong độ cao nhất dựa trên điểm phong độ chung
best_team = team_performance['Overall Performance'].idxmax()
best_team_score = team_performance['Overall Performance'].max()

print(f"\nĐội bóng có phong độ tốt nhất của giải bóng đá Ngoại Hạng Anh mùa 2023-2024 là: {best_team} với điểm phong độ là: {best_team_score:.2f}")
