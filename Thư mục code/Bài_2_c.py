# Vẽ historgram phân bố của mỗi chỉ số của các cầu thủ trong toàn giải và mỗi đội


import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
import os

# Tải dữ liệu lên
df = pd.read_csv('results.csv')

#chuyển dữ liệu cột 'Minutes' sang dạng số
df['Minutes'] = df['Minutes'].str.replace(',', '').astype(float)
# Định nghĩa các  chỉ số cụ thể
categories = {
    "Age": ["Age"],
    "Playing time": ["Matches", "Starts", "Minutes"],
    "Performance": ["non_penalty_goals", "penalty_goals", "assists", "yellow_cards", "red_cards"],
    "Expected": ["xG", "npxG", "xAG"],
    "Progression": ["PrgC", "PrgP", "PrgR"],
    "Per 90 minutes": ["per90_Gls", "per90_Ast", "per90_G+A", "per90_G-PK", "per90_G+A-PK", "per90_xG", "per90_xAG", "per90_xG+xAG", "per90_npxG", "per90_npxG+xAG"],
    "Goalkeeping Performance": ["GA", "GA90", "SoTA", "Saves", "Save%", "W", "D", "L", "CS", "CS%"],
    "Goalkeeping Penalties": ["PKatt", "PKA", "PKsv", "PKm", "Save%"],
    "Shooting Standard": ["Gls", "Sh", "SoT", "SoT%", "Sh/90", "SoT/90", "G/Sh", "G/SoT", "Dist", "FK", "PK", "PKatt"],
    "Shooting Expected": ["xG", "npxG", "npxG/Sh", "G-xG", "np:G-xG"],
    "Passing Total": ["Pass_Cmp", "Pass_Att", "Pass_Cmp%", "TotDist", "PrgDist"],
    "Passing Short": ["Short_Cmp", "Short_Att", "Short_Cmp%"],
    "Passing Medium": ["Medium_Cmp", "Medium_Att", "Medium_Cmp%"],
    "Passing Long": ["Long_Cmp", "Long_Att", "Long_Cmp%"],
    "Passing Expected": ["Ast", "xAG", "xA", "A-xAG", "KP", "1/3", "PPA", "CrsPA", "PrgP"],
    "Pass Types": ["Pass_Live", "Pass_Dead", "Pass_FK", "Pass_TB", "Pass_Sw", "Pass_Crs", "Pass_TI", "Pass_CK"],
    "Corners": ["Corner_In", "Corner_Out", "Corner_Str"],
    "Passing Outcomes": ["Pass_Cmp_outcome", "Pass_Off", "Pass_Blocks"],
    "Goal and Shot Creation": ["SCA", "SCA90", "SCA_type_Passlive", "SCA_type_Passdead", "SCA_type_TO", "SCA_type_Sh", "SCA_type_Fld", "SCA_type_Def", "GCA", "GCA90", "GCA_type_Passlive", "GCA_type_Passdead", "GCA_type_TO", "GCA_type_Sh", "GCA_type_Fld", "GCA_type_Def"],
    "Defensive Actions": ["Tkl", "TklW", "Def_3rd", "Mid_3rd", "Att_3rd", "Challenges_Tkl", "Challenges_Att", "Challenges_Tkl%", "Challenges_Lost", "Blocks", "Blocks_Sh", "Blocks_Pass", "Blocks_Int", "Blocks_Tkl+Int", "Blocks_Clr", "Blocks_Err"],
    "Possession": ["Touches", "Def_Pen", "Def_3rd", "Mid_3rd", "Att_3rd", "Att_Pen", "Live_Touches", "Take_Att", "Take_Succ", "Take_Succ%", "Take_Tkld", "Take_Tkld%", "Carries", "Carries_TotDist", "Carries_ProDist", "Carries_ProgC", "Carries_1/3", "Carries_CPA", "Carries_Mis", "Carries_Dis", "Rec", "Rec_PrgR"],
    "Playing Time": ["PT_Starts", "PT_Mn/Start", "PT_Compl", "Subs", "Subs_Mn/Sub", "Subs_unSub", "TS_PPM", "TS_onG", "TS_onGA", "TSxG_onxG", "TSxG_onGA"],
    "Miscellaneous Stats": ["Fls", "Fld", "Off", "Crs", "OG", "Recov", "Aerial_Won", "Aerial_Lost", "Aerial_Won%"]
}

# Tạo thư mục để lưu các biểu đồ histogram
output_all = 'histograms_by_all'
os.makedirs(output_all, exist_ok=True)

# Hàm để thay thế ký tự không hợp lệ trong tên file
def sanitize_filename(filename):
    return filename.replace('/', '_').replace('\\', '_')

# Tạo và lưu biểu đồ cho từng chỉ số
for category, stats in categories.items():
    category_dir = os.path.join(output_all, sanitize_filename(category))
    os.makedirs(category_dir, exist_ok=True)
    
    for stat in stats:
        if stat in df.columns:
            plt.figure(figsize=(12, 10))
            plt.hist(df[stat].dropna(), bins=20, alpha=0.6, color='blue')
            plt.title(f'{stat} - {category}', fontsize=14)
            plt.xlabel('Giá trị', fontsize=12)
            plt.ylabel('Số lượng cầu thủ', fontsize=12)
            plt.grid(axis='y', alpha=0.7)

            # Giới hạn số tick trên trục x
            plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, nbins=15))  # Chỉ hiển thị tối đa 15 tick x
            plt.xticks(fontsize=10)  
            plt.yticks(fontsize=10)
            # Lưu biểu đồ dưới dạng ảnh riêng
            plt.savefig(os.path.join(category_dir, f'{sanitize_filename(stat)}.png'))
            plt.close()

print("Đã lưu các biểu đồ cho mỗi chỉ số của toàn giải đấu vào thư mục 'histograms_by_all'.")

# Vẽ histogram phân bố của mỗi chỉ số cho từng đội và lưu vào thư mục riêng có tên là từng đội bóng
teams = df['Team'].unique()
team_output = 'histograms_by_team'
os.makedirs(team_output, exist_ok=True)

for team in teams:
    team_data = df[df['Team'] == team]
    team_dir = os.path.join(team_output, sanitize_filename(team))
    os.makedirs(team_dir, exist_ok=True)
    
    for category, stats in categories.items():
        category_dir = os.path.join(team_dir, sanitize_filename(category))
        os.makedirs(category_dir, exist_ok=True)
        
        for stat in stats:
            if stat in team_data.columns:
                plt.figure(figsize=(12, 10))
                plt.hist(team_data[stat].dropna(), bins=20, alpha=0.7, color='blue')
                plt.title(f'{stat} - {category} - {team}', fontsize=14)
                plt.xlabel('Giá trị', fontsize=12)
                plt.ylabel('Số lượng cầu thủ', fontsize=12)
                plt.grid(axis='y', alpha=0.7)
                # Giới hạn số tick trên trục x
                plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, nbins=15))  # Chỉ hiển thị tối đa 15 tick x
                plt.xticks( fontsize=10)  
                plt.yticks(fontsize=10)
                # Lưu biểu đồ dưới dạng ảnh riêng
                plt.savefig(os.path.join(category_dir, f'{sanitize_filename(stat)}.png'))
                plt.close()

print("Đã lưu biểu đồ của mỗi đội vào các thư mục riêng trong 'histograms_by_team'.")

