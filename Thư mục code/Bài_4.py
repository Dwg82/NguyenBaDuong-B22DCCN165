import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep

# Cấu hình Selenium để sử dụng Chrome
options = webdriver.ChromeOptions()

# Tạo driver với ChromeDriverManager 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Khởi tạo danh sách để lưu dữ liệu cầu thủ
data = []

# Duyệt qua 18 trang (page 1 đến page 18)
for page in range(1, 19):
    if page == 1:
        url = "https://www.footballtransfers.com/us/transfers/confirmed/2023-2024/uk-premier-league"  # Trang 1 không có số trang
    else:
        url = f"https://www.footballtransfers.com/us/transfers/confirmed/2023-2024/uk-premier-league/{page}"  # Các trang từ 2 trở đi

    driver.get(url)
    sleep(2)  # Đợi 2 giây để trang web tải xong

    # Lấy HTML 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Tìm bảng dữ liệu cầu thủ
    table = soup.find('table', {'class': 'table table-striped table-hover leaguetable mvp-table transfer-table mb-0'})
    
    if table:
        # Tìm tất cả các hàng trong tbody (bỏ qua hàng tiêu đề trong thead)
        rows = table.tbody.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if not cols:
                continue

            # Khởi tạo dictionary cho từng cầu thủ với giá trị mặc định là 'N/a'
            player = {'Name': 'N/a', 'Old_team': 'N/a', 'New_team': 'N/a', 'Price': 'N/a'}

            # Tìm giá trị 'Name' từ thẻ span có class 'd-none'
            name_span = cols[0].find('span', class_='d-none')
            if name_span:
                player['Name'] = name_span.text.strip()

            # Tìm đội bóng cũ của cầu thủ và đội mới mà cầu thủ chuyển nhượng đến
            old_team_div = cols[1].find('div', class_='transfer-club transfer-club--from')
            if old_team_div:
                old_team_name = old_team_div.find('div', class_='transfer-club__name')
                player['Old_team'] = old_team_name.text.strip() if old_team_name else 'N/a'

            new_team_div = cols[1].find('div', class_='transfer-club transfer-club--to')
            if new_team_div:
                new_team_name = new_team_div.find('div', class_='transfer-club__name')
                player['New_team'] = new_team_name.text.strip() if new_team_name else 'N/a'

            # Tìm giá trị 'Price' từ thẻ span trong cols[3]
            price_span = cols[3].find('span')
            if price_span:
                price_text = price_span.text.strip()
            # Nếu giá trị là "Free" thì giữ nguyên. Nếu có tiền chuyển nhượng thì xoá ký hiệu và giữ lại số.
                if "Free" in price_text:
                    player['Price'] = price_text
                else:
                # Xoá ký hiệu tiền tệ, giữ lại phần số và chữ cái (M,K)
                    player['Price'] = price_text.replace('€', '').replace('$', '').strip()
            else:
                player['Price'] = 'N/a'

            # Thêm cầu thủ vào danh sách
            data.append(player)

    print(f"Đã lấy dữ liệu từ trang {page}")

# Đóng driver sau khi hoàn thành
driver.quit()

# Chuyển đổi danh sách dữ liệu thành DataFrame
df = pd.DataFrame(data)

# In kết quả
print(df)

# Lưu DataFrame vào file CSV
df.to_csv('Bài_4.csv', index=False)
