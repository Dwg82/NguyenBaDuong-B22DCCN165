# Tìm top 3 cầu thủ có điểm cao nhất và thấp nhất ở mỗi chỉ số



import pandas as pd

# Đọc dữ liệu từ file CSV
data = pd.read_csv('results.csv')

# Xác định các thuộc tính cần phân tích
attributes = [
    'Age', 'Matches', 'Starts', 'Minutes', 'non_penalty_goals', 'penalty_goals', 
    'assists', 'yellow_cards', 'red_cards', 'xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR', 
    'per90_Gls', 'per90_Ast', 'per90_G+A', 'per90_G-PK', 'per90_G+A-PK', 'per90_xG', 
    'per90_xAG', 'per90_xG+xAG', 'per90_npxG', 'per90_npxG+xAG', 'GA', 'GA90', 'SoTA', 
    'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'PKatt', 'PKA', 'PKsv', 'PKm', 'GK_Save%', 
    'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 
    'PKatt', 'xG_shooting', 'npxG_shooting', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Pass_Cmp', 
    'Pass_Att', 'Pass_Cmp%', 'TotDist', 'PrgDist', 'Short_Cmp', 'Short_Att', 'Short_Cmp%', 
    'Medium_Cmp', 'Medium_Att', 'Medium_Cmp%', 'Long_Cmp', 'Long_Att', 'Long_Cmp%', 
    'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP', 'Pass_Live', 'Pass_Dead', 
    'Pass_FK', 'Pass_TB', 'Pass_Sw', 'Pass_Crs', 'Pass_TI', 'Pass_CK', 'Corner_In', 'Corner_Out', 
    'Corner_Str', 'Pass_Cmp_outcome', 'Pass_Off', 'Pass_Blocks', 'SCA', 'SCA90', 'SCA_type_Passlive', 
    'SCA_type_Passdead', 'SCA_type_TO', 'SCA_type_Sh', 'SCA_type_Fld', 'SCA_type_Def', 'GCA', 
    'GCA90', 'GCA_type_Passlive', 'GCA_type_Passdead', 'GCA_type_TO', 'GCA_type_Sh', 'GCA_type_Fld', 
    'GCA_type_Def', 'Tkl', 'TklW', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Challenges_Tkl', 'Challenges_Att', 
    'Challenges_Tkl%', 'Challenges_Lost', 'Blocks', 'Blocks_Sh', 'Blocks_Pass', 'Blocks_Int', 
    'Blocks_Tkl+Int', 'Blocks_Clr', 'Blocks_Err', 'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 
    'Att_3rd', 'Att_Pen', 'Live_Touches', 'Take_Att', 'Take_Succ', 'Take_Succ%', 'Take_Tkld', 
    'Take_Tkld%', 'Carries', 'Carries_TotDist', 'Carries_ProDist', 'Carries_ProgC', 'Carries_1/3', 
    'Carries_CPA', 'Carries_Mis', 'Carries_Dis', 'Rec', 'Rec_PrgR', 'PT_Starts', 'PT_Mn/Start', 
    'PT_Compl', 'Subs', 'Subs_Mn/Sub', 'Subs_unSub', 'TS_PPM', 'TS_onG', 'TS_onGA', 'TSxG_onxG', 
    'TSxG_onGA', 'Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov', 'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'
]

# Chuyển đổi từng cột thành dạng số 
for attribute in attributes:
    data[attribute] = pd.to_numeric(data[attribute], errors='coerce')

# Tìm top 3 cầu thủ có điểm cao nhất và thấp nhất ở mỗi chỉ số

top_players = {}
bottom_players = {}

# Lặp qua từng chỉ số trong danh sách attributes
for attribute in attributes:

    # Loại bỏ các hàng có giá trị NaN trong chỉ số hiện tại
    valid_data = data.dropna(subset=[attribute])

    # Tìm 3 giá trị lớn nhất và nhỏ nhất
    top_3 = valid_data.nlargest(3, attribute)
    bottom_3 = valid_data.nsmallest(3, attribute)

    # Tìm giá trị tối đa và tối thiểu 
    max_value = top_3[attribute].max() if not top_3.empty else None
    min_value = bottom_3[attribute].min() if not bottom_3.empty else None

    # Lấy tất cả cầu thủ có điểm số cao hơn hoặc bằng với max_value
    top_players[attribute] = valid_data[valid_data[attribute] >= max_value][['Name', attribute]].sort_values(by=attribute, ascending=False)
    
    # Nếu không đủ 3 cầu thủ, tìm tiếp cho đến khi đủ
    while len(top_players[attribute]) < 3:
        next_value = valid_data[valid_data[attribute] < top_players[attribute][attribute].min()][attribute].max()  # Tìm giá trị tiếp theo
        if pd.isna(next_value):  
            break
        top_players[attribute] = valid_data[valid_data[attribute] >= next_value][['Name', attribute]].sort_values(by=attribute, ascending=False)

    # Lấy tất cả cầu thủ có điểm số thấp hơn hoặc bằng với min_value
    bottom_players[attribute] = valid_data[valid_data[attribute] <= min_value][['Name', attribute]].sort_values(by=attribute, ascending=True)

    # Nếu không đủ 3 cầu thủ, tìm tiếp cho đến khi đủ
    while len(bottom_players[attribute]) < 3:
        next_value = valid_data[valid_data[attribute] > bottom_players[attribute][attribute].max()][attribute].min()  # Tìm giá trị tiếp theo
        if pd.isna(next_value):  
            break
        bottom_players[attribute] = valid_data[valid_data[attribute] <= next_value][['Name', attribute]].sort_values(by=attribute, ascending=True)

# Ghi kết quả ra file BAI_2_a.in 
with open('BAI_2_a.in', 'w', encoding='utf-8') as file:
    for attribute in attributes:
        file.write(f"Top 3 cầu thủ có điểm cao nhất ở chỉ số {attribute}:\n")
        file.write(top_players[attribute].to_string(index=False))
        file.write("\n\n")

        
        file.write(f"Top 3 cầu thủ có điểm thấp nhất ở chỉ số {attribute}:\n")
        file.write(bottom_players[attribute].to_string(index=False))
        file.write("\n\n")

print("Kết quả đã được ghi vào file BAI_2_a.in")