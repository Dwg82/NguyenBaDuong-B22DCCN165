import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep

# Cấu hình Selenium để sử dụng Chrome
options_chrome = webdriver.ChromeOptions()
# tự động quản lý phiên bản driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options_chrome)

# Mở trang web 1
driver.get("https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats")
sleep(1)

# Lấy HTML sau khi trang web đã được tải lên 
html = driver.page_source
# phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')
# Tìm bảng dữ liệu cầu thủ
table = soup.find('table', {'id': 'stats_standard'})
# Khởi tạo danh sách để lưu dữ liệu cầu thủ
data = []

# Danh sách các thuộc tính của cầu thủ

players = [
    'Name', 'Nation','Team', 'Position', 'Age',                        
    'Matches', 'Starts', 'Minutes', 
    'non_penalty_goals', 'penalty_goals', 'assists', 'yellow_cards', 
    'red_cards',
    'xG', 'npxG', 'xAG',
    'PrgC', 'PrgP', 'PrgR', 
    'per90_Gls', 'per90_Ast', 'per90_G+A', 'per90_G-PK', 
    'per90_G+A-PK', 'per90_xG', 'per90_xAG', 'per90_xG+xAG', 
    'per90_npxG', 'per90_npxG+xAG',
    'GA', 'GA90', 'SoTA', 'Saves', 
    'Save%', 'W', 'D', 'L', 'CS', 'CS%',
    'PKatt', 'PKA', 'PKsv', 'PKm', 'GK_Save%',
    'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt', 
    'xG_shooting', 'npxG_shooting', 'npxG/Sh', 'G-xG', 'np:G-xG', 
    'Pass_Cmp', 'Pass_Att', 'Pass_Cmp%', 'TotDist', 'PrgDist', 
    'Short_Cmp', 'Short_Att', 'Short_Cmp%', 'Medium_Cmp', 
    'Medium_Att', 'Medium_Cmp%', 'Long_Cmp', 'Long_Att', 
    'Long_Cmp%', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 
    'CrsPA', 'PrgP', 'Pass_Live', 'Pass_Dead', 'Pass_FK', 
    'Pass_TB', 'Pass_Sw', 'Pass_Crs', 'Pass_TI', 'Pass_CK',
    'Corner_In','Corner_Out','Corner_Str', 
    'Pass_Cmp_outcome', 'Pass_Off', 'Pass_Blocks',
    'SCA','SCA90','SCA_type_Passlive','SCA_type_Passdead','SCA_type_TO','SCA_type_Sh','SCA_type_Fld','SCA_type_Def',
    'GCA','GCA90','GCA_type_Passlive','GCA_type_Passdead','GCA_type_TO','GCA_type_Sh','GCA_type_Fld','GCA_type_Def', 
    'Tkl','TklW', 'Def_3rd', 'Mid_3rd', 'Att_3rd',
    'Challenges_Tkl','Challenges_Att', 'Challenges_Tkl%', 'Challenges_Lost', 
    'Blocks','Blocks_Sh','Blocks_Pass','Blocks_Int','Blocks_Tkl+Int','Blocks_Clr','Blocks_Err',
    'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 
    'Att_Pen', 'Live_Touches', 'Take_Att', 'Take_Succ', 
    'Take_Succ%', 'Take_Tkld', 'Take_Tkld%', 'Carries', 
    'Carries_TotDist', 'Carries_ProDist', 'Carries_ProgC', 
    'Carries_1/3', 'Carries_CPA', 'Carries_Mis', 'Carries_Dis',
    'Rec','Rec_PrgR',
    'PT_Starts','PT_Mn/Start','PT_Compl',
    'Subs','Subs_Mn/Sub','Subs_unSub',
    'TS_PPM','TS_onG','TS_onGA',
    'TSxG_onxG','TSxG_onGA', 
    'Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov',
    'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'
]


# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')
# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    # Ban đầu ta cho các thuộc tính mặc định có giá trị "N/a"
    player = {col: "N/a" for col in players} 

    # Bắt đầu lấy dữ liệu
    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['Nation'] = cols[1].text.strip() if cols[1].text.strip() else "N/a"
    player['Position'] = cols[2].text.strip() if cols[2].text.strip() else "N/a"
    player['Team'] = cols[3].text.strip() if cols[3].text.strip() else "N/a"
    player['Age'] = cols[4].text.strip() if cols[4].text.strip() else "N/a"
    player['Matches'] = cols[6].text.strip() if cols[6].text.strip() else "N/a"
    player['Starts'] = cols[7].text.strip() if cols[7].text.strip() else "N/a"
    player['Minutes'] = cols[8].text.strip() if cols[8].text.strip() else "N/a"
    player['assists'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['non_penalty_goals'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['penalty_goals'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['yellow_cards'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['red_cards'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['xG'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['npxG'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['xAG'] = cols[20].text.strip() if cols[20].text.strip() else "N/a"
    player['PrgC'] = cols[22].text.strip() if cols[22].text.strip() else "N/a"
    player['PrgP'] = cols[23].text.strip() if cols[23].text.strip() else "N/a"
    player['PrgR'] = cols[24].text.strip() if cols[24].text.strip() else "N/a"
    player['per90_Gls'] = cols[25].text.strip() if cols[25].text.strip() else "N/a"
    player['per90_Ast'] = cols[26].text.strip() if cols[26].text.strip() else "N/a"
    player['per90_G+A'] = cols[27].text.strip() if cols[27].text.strip() else "N/a"
    player['per90_G-PK'] = cols[28].text.strip() if cols[28].text.strip() else "N/a"
    player['per90_G+A-PK'] = cols[29].text.strip() if cols[29].text.strip() else "N/a"
    player['per90_xG'] = cols[30].text.strip() if cols[30].text.strip() else "N/a"
    player['per90_xAG'] = cols[31].text.strip() if cols[31].text.strip() else "N/a"
    player['per90_xG+xAG'] = cols[32].text.strip() if cols[32].text.strip() else "N/a"
    player['per90_npxG'] = cols[33].text.strip() if cols[33].text.strip() else "N/a"
    player['per90_npxG+xAG'] = cols[34].text.strip() if cols[34].text.strip() else "N/a"


    # bỏ dấu phẩy trong cột minutes
    minutes_value = player['Minutes'].replace(',', '')
    
    # Chỉ thêm cầu thủ có số phút thi đấu nhiều hơn 90
    if minutes_value != "N/a" and int(minutes_value) > 90:
        data.append(player)




# Mở trang web thứ hai:Goalkeeper
driver.get("https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats")


sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu thủ môn
table = soup.find('table', {'id': 'stats_keeper'})



new_GK_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['GA'] = cols[10].text.strip() if cols[10].text.strip() else "N/a"
    player['GA90'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['SoTA'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['Saves'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['Save%'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['W'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['D'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['L'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['CS'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['CS%'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['PKatt'] = cols[20].text.strip() if cols[20].text.strip() else "N/a"
    player['PKA'] = cols[21].text.strip() if cols[21].text.strip() else "N/a"
    player['PKsv'] = cols[22].text.strip() if cols[22].text.strip() else "N/a"
    player['PKm'] = cols[23].text.strip() if cols[23].text.strip() else "N/a"
    player['GK_Save%'] = cols[24].text.strip() if cols[24].text.strip() else "N/a"

    new_GK_data.append(player)

# Danh sách các thuộc tính cần cập nhật 
GK_attributes_to_update = ['GA', 'GA90', 'SoTA', 'Saves', 
    'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'PKatt', 'PKA', 'PKsv', 
    'PKm', 'GK_Save%']

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_data dựa vào tên
    matching_player = next((p for p in new_GK_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính
    if matching_player:
        for attr in GK_attributes_to_update:
            player[attr] = matching_player[attr]






# Mở trang web thứ ba:Shooting
driver.get("https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats")


sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu
table = soup.find('table', {'id': 'stats_shooting'})

new_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['Team'] = cols[3].text.strip() if cols[3].text.strip() else "N/a"
    player['Gls'] = cols[7].text.strip() if cols[7].text.strip() else "N/a"
    player['Sh'] = cols[8].text.strip() if cols[8].text.strip() else "N/a"
    player['SoT'] = cols[9].text.strip() if cols[9].text.strip() else "N/a"
    player['SoT%'] = cols[10].text.strip() if cols[10].text.strip() else "N/a"
    player['Sh/90'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['SoT/90'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['G/Sh'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['G/SoT'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['Dist'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['FK'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['PK'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['PKatt'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['xG_shooting'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['npxG_shooting'] = cols[20].text.strip() if cols[20].text.strip() else "N/a"
    player['npxG/Sh'] = cols[21].text.strip() if cols[21].text.strip() else "N/a"
    player['G-xG'] = cols[22].text.strip() if cols[22].text.strip() else "N/a"
    player['np:G-xG'] = cols[23].text.strip() if cols[23].text.strip() else "N/a"

    new_data.append(player)

# Danh sách các thuộc tính cần cập nhật trong shooting
attributes_to_update = ['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 
                        'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt', 
                        'xG_shooting', 'npxG_shooting', 'npxG/Sh', 
                        'G-xG', 'np:G-xG']

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_data dựa vào tên
    matching_player = next((p for p in new_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính
    if matching_player:
        for attr in attributes_to_update:
            player[attr] = matching_player[attr]



# Mở trang web thứ 4:Passing
driver.get("https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats")


sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu 
table = soup.find('table', {'id': 'stats_passing'})

new_passing_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['Team'] = cols[1].text.strip() if cols[1].text.strip() else "N/a"
    player['Pass_Cmp'] = cols[5].text.strip() if cols[5].text.strip() else "N/a"
    player['Pass_Att'] = cols[6].text.strip() if cols[6].text.strip() else "N/a"
    player['Pass_Cmp%'] = cols[7].text.strip() if cols[7].text.strip() else "N/a"
    player['TotDist'] = cols[8].text.strip() if cols[8].text.strip() else "N/a"
    player['PrgDist'] = cols[9].text.strip() if cols[9].text.strip() else "N/a"
    player['Short_Cmp'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['Short_Att'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['Short_Cmp%'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['Medium_Cmp'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['Medium_Att'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['Medium_Cmp%'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['Long_Cmp'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['Long_Att'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['Long_Cmp%'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['Ast'] = cols[21].text.strip() if cols[21].text.strip() else "N/a"
    player['xAG'] = cols[22].text.strip() if cols[22].text.strip() else "N/a"
    player['xA'] = cols[23].text.strip() if cols[23].text.strip() else "N/a"
    player['A-xAG'] = cols[24].text.strip() if cols[24].text.strip() else "N/a"
    player['KP'] = cols[25].text.strip() if cols[25].text.strip() else "N/a"
    player['1/3'] = cols[26].text.strip() if cols[26].text.strip() else "N/a"
    player['PPA'] = cols[27].text.strip() if cols[27].text.strip() else "N/a"
    player['CrsPA'] = cols[28].text.strip() if cols[28].text.strip() else "N/a"
    player['PrgP'] = cols[29].text.strip() if cols[29].text.strip() else "N/a"

    new_passing_data.append(player)

# Danh sách các thuộc tính cần cập nhật trong passing
passing_attributes_to_update = ['Pass_Cmp', 'Pass_Att', 'Pass_Cmp%', 'TotDist', 'PrgDist', 
                                'Short_Cmp', 'Short_Att', 'Short_Cmp%', 'Medium_Cmp', 
                                'Medium_Att', 'Medium_Cmp%', 'Long_Cmp', 'Long_Att', 
                                'Long_Cmp%', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', 
                                '1/3', 'PPA', 'CrsPA', 'PrgP']

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_data dựa vào tên
    matching_player = next((p for p in new_passing_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính
    if matching_player:
        for attr in passing_attributes_to_update:
            player[attr] = matching_player[attr]



# Mở trang web thứ 5:Passing Types
driver.get("https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats")

sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu 
table = soup.find('table', {'id': 'stats_passing_types'})

new_passing_types_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['Team'] = cols[3].text.strip() if cols[3].text.strip() else "N/a"
    player['Pass_Live'] = cols[8].text.strip() if cols[8].text.strip() else "N/a"
    player['Pass_Dead'] = cols[9].text.strip() if cols[9].text.strip() else "N/a"
    player['Pass_FK'] = cols[10].text.strip() if cols[10].text.strip() else "N/a"
    player['Pass_TB'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['Pass_Sw'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['Pass_Crs'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['Pass_TI'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['Pass_CK'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['Corner_In'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['Corner_Out'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['Corner_Str'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['Pass_Cmp_outcome'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['Pass_Off'] = cols[20].text.strip() if cols[20].text.strip() else "N/a"
    player['Pass_Blocks'] = cols[21].text.strip() if cols[21].text.strip() else "N/a"


    new_passing_types_data.append(player)

# Danh sách các thuộc tính cần cập nhật trong passing type
passing_types_attributes_to_update = ['Pass_Live', 'Pass_Dead', 'Pass_FK', 'Pass_TB', 'Pass_Sw', 
                                      'Pass_Crs', 'Pass_TI', 'Pass_CK', 'Corner_In','Corner_Out','Corner_Str','Pass_Cmp_outcome', 
                                      'Pass_Off', 'Pass_Blocks']

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_data dựa vào tên
    matching_player = next((p for p in new_passing_types_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính
    if matching_player:
        for attr in passing_types_attributes_to_update:
            player[attr] = matching_player[attr]
            




# Mở trang web thứ 6: GCA
driver.get("https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats")


sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu 
table = soup.find('table', {'id': 'stats_gca'})

new_gca_sca_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['SCA'] = cols[7].text.strip() if cols[7].text.strip() else "N/a"
    player['SCA90'] = cols[8].text.strip() if cols[8].text.strip() else "N/a"
    player['SCA_type_Passlive'] = cols[9].text.strip() if cols[9].text.strip() else "N/a"
    player['SCA_type_Passdead'] = cols[10].text.strip() if cols[10].text.strip() else "N/a"
    player['SCA_type_TO'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['SCA_type_Sh'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['SCA_type_Fld'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['SCA_type_Def'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['GCA'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['GCA90'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['GCA_type_Passlive'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['GCA_type_Passdead'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['GCA_type_TO'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['GCA_type_Sh'] = cols[20].text.strip() if cols[20].text.strip() else "N/a"
    player['GCA_type_Fld'] = cols[21].text.strip() if cols[21].text.strip() else "N/a"
    player['GCA_type_Def'] = cols[22].text.strip() if cols[22].text.strip() else "N/a"


    new_gca_sca_data.append(player)

# Danh sách các thuộc tính cần cập nhật 
gca_sca_attributes_to_update = ['SCA', 'SCA90', 'SCA_type_Passlive', 'SCA_type_Passdead', 'SCA_type_TO', 
                                'SCA_type_Sh', 'SCA_type_Fld', 'SCA_type_Def', 'GCA', 'GCA90', 
                                'GCA_type_Passlive', 'GCA_type_Passdead', 'GCA_type_TO', 
                                'GCA_type_Sh', 'GCA_type_Fld', 'GCA_type_Def']

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_gca_sca_data dựa vào tên
    matching_player = next((p for p in new_gca_sca_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính GCA và SCA
    if matching_player:
        for attr in gca_sca_attributes_to_update:
            player[attr] = matching_player[attr]



# Mở trang web thứ 7: Defence
driver.get("https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats")

sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu 
table = soup.find('table', {'id': 'stats_defense'})

new_defense_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['Tkl'] = cols[7].text.strip() if cols[7].text.strip() else "N/a"
    player['TklW'] = cols[8].text.strip() if cols[8].text.strip() else "N/a"
    player['Def_3rd'] = cols[9].text.strip() if cols[9].text.strip() else "N/a"
    player['Mid_3rd'] = cols[10].text.strip() if cols[10].text.strip() else "N/a"
    player['Att_3rd'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['Challenges_Tkl'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['Challenges_Att'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['Challenges_Tkl%'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['Challenges_Lost'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['Blocks'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['Blocks_Sh'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['Blocks_Pass'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['Blocks_Int'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['Blocks_Tkl+Int'] = cols[20].text.strip() if cols[20].text.strip() else "N/a"
    player['Blocks_Clr'] = cols[21].text.strip() if cols[21].text.strip() else "N/a"
    player['Blocks_Err'] = cols[22].text.strip() if cols[22].text.strip() else "N/a"

    new_defense_data.append(player)

# Danh sách các thuộc tính cần cập nhật 
defense_attributes_to_update = [
    'Tkl', 'TklW', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Challenges_Tkl', 'Challenges_Att', 
    'Challenges_Tkl%', 'Challenges_Lost', 'Blocks', 'Blocks_Sh', 'Blocks_Pass', 'Blocks_Int', 
    'Blocks_Tkl+Int', 'Blocks_Clr', 'Blocks_Err'
]

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_defense_data dựa vào tên
    matching_player = next((p for p in new_defense_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính phòng ngự
    if matching_player:
        for attr in defense_attributes_to_update:
            player[attr] = matching_player[attr]



# Mở trang web thứ 8:Possesion
driver.get("https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats")


sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu 
table = soup.find('table', {'id': 'stats_possession'})

new_possession_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['Touches'] = cols[7].text.strip() if cols[7].text.strip() else "N/a"
    player['Def_Pen'] = cols[8].text.strip() if cols[8].text.strip() else "N/a"
    player['Def_3rd'] = cols[9].text.strip() if cols[9].text.strip() else "N/a"
    player['Mid_3rd'] = cols[10].text.strip() if cols[10].text.strip() else "N/a"
    player['Att_3rd'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['Att_Pen'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['Live_Touches'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['Take_Att'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['Take_Succ'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['Take_Succ%'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['Take_Tkld'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['Take_Tkld%'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['Carries'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['Carries_TotDist'] = cols[20].text.strip() if cols[20].text.strip() else "N/a"
    player['Carries_ProDist'] = cols[21].text.strip() if cols[21].text.strip() else "N/a"
    player['Carries_ProgC'] = cols[22].text.strip() if cols[22].text.strip() else "N/a"
    player['Carries_1/3'] = cols[23].text.strip() if cols[23].text.strip() else "N/a"
    player['Carries_CPA'] = cols[24].text.strip() if cols[24].text.strip() else "N/a"
    player['Carries_Mis'] = cols[25].text.strip() if cols[25].text.strip() else "N/a"
    player['Carries_Dis'] = cols[26].text.strip() if cols[26].text.strip() else "N/a"
    player['Rec'] = cols[27].text.strip() if cols[27].text.strip() else "N/a"
    player['Rec_PrgR'] = cols[28].text.strip() if cols[28].text.strip() else "N/a"
  

    new_possession_data.append(player)

# Danh sách các thuộc tính cần cập nhật 
possession_attributes_to_update = [
    'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Att_Pen', 'Live_Touches', 
    'Take_Att', 'Take_Succ', 'Take_Succ%', 'Take_Tkld', 'Take_Tkld%', 'Carries', 
    'Carries_TotDist', 'Carries_ProDist', 'Carries_ProgC', 'Carries_1/3', 'Carries_CPA', 
    'Carries_Mis', 'Carries_Dis', 'Rec', 'Rec_PrgR'
]

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_possession_data dựa vào tên
    matching_player = next((p for p in new_possession_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính kiểm soát bóng
    if matching_player:
        for attr in possession_attributes_to_update:
            player[attr] = matching_player[attr]


# Mở trang web thứ 9:Playing time
driver.get("https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats")


sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu thủ môn
table = soup.find('table', {'id': 'stats_playing_time'})

new_playing_time_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['PT_Starts'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['PT_Mn/Start'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['PT_Compl'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['Subs'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['Subs_Mn/Sub'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['Subs_unSub'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['TS_PPM'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['TS_onG'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['TS_onGA'] = cols[19].text.strip() if cols[19].text.strip() else "N/a"
    player['TSxG_onxG'] = cols[23].text.strip() if cols[23].text.strip() else "N/a"
    player['TSxG_onGA'] = cols[24].text.strip() if cols[24].text.strip() else "N/a"


    new_playing_time_data.append(player)

# Danh sách các thuộc tính cần cập nhật 
playing_time_attributes_to_update = [
    'PT_Starts', 'PT_Mn/Start', 'PT_Compl', 
    'Subs', 'Subs_Mn/Sub', 'Subs_unSub', 
    'TS_PPM', 'TS_onG', 'TS_onGA', 
    'TSxG_onxG', 'TSxG_onGA'
]

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_playing_time_data dựa vào tên
    matching_player = next((p for p in new_playing_time_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính thời gian thi đấu
    if matching_player:
        for attr in playing_time_attributes_to_update:
            player[attr] = matching_player[attr]



# Mở trang web thứ 10:MISC
driver.get("https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats")


sleep(1)

# Lấy HTML sau khi trang web đã được render đầy đủ
html = driver.page_source

# Sử dụng BeautifulSoup để phân tích cú pháp HTML
soup = BeautifulSoup(html, 'html.parser')

# Tìm bảng dữ liệu 
table = soup.find('table', {'id': 'stats_misc'})

new_misc_data = []

# Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
rows = table.tbody.find_all('tr')

# Duyệt qua từng hàng và lấy dữ liệu
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    player = {}

    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/a"
    player['Fls'] = cols[11].text.strip() if cols[11].text.strip() else "N/a"
    player['Fld'] = cols[12].text.strip() if cols[12].text.strip() else "N/a"
    player['Off'] = cols[13].text.strip() if cols[13].text.strip() else "N/a"
    player['Crs'] = cols[14].text.strip() if cols[14].text.strip() else "N/a"
    player['OG'] = cols[15].text.strip() if cols[15].text.strip() else "N/a"
    player['Recov'] = cols[16].text.strip() if cols[16].text.strip() else "N/a"
    player['Aerial_Won'] = cols[17].text.strip() if cols[17].text.strip() else "N/a"
    player['Aerial_Lost'] = cols[18].text.strip() if cols[18].text.strip() else "N/a"
    player['Aerial_Won%'] = cols[19].text.strip() if cols[19].text.strip() else "N/a" 

    new_misc_data.append(player)

# Danh sách các thuộc tính cần cập nhật
misc_attributes_to_update = [
    'Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov',
    'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'
]

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_playing_time_data dựa vào tên
    matching_player = next((p for p in new_misc_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính thời gian thi đấu
    if matching_player:
        for attr in misc_attributes_to_update:
            player[attr] = matching_player[attr]


# Lưu dữ liệu vào DataFrame và xuất ra file CSV
df = pd.DataFrame(data)


df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1])


# Tạo cột 'First_Name' bằng cách tách tên đầy đủ
df['First_Name'] = df['Name'].apply(lambda x: x.split()[-1])


# Chuyển đổi cột 'Age' sang kiểu số nguyên (int) để có thể sắp xếp chính xác
df['Age'] = df['Age'].astype(int)

# Sắp xếp theo 'First_Name' và sau đó theo 'Age' từ lớn đến nhỏ
df = df.sort_values(by=['First_Name','Age'], ascending=[True, False])

# Xoá cột First_Name ra khỏi bảng
df.drop(columns=['First_Name'], inplace=True)



df.to_csv('results.csv', index=False)

# Đóng trình duyệt
driver.quit()
