import os
import glob
import re
import json
import pandas as pd

def read_allFile(path):
    all_file = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files: 
            all_file.append(os.path.abspath(f))
    return all_file

# Load data in JSON file
def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    fixed_content = "[" + re.sub(r"}\s*{", "},{", content) + "]"
    
    try:
        # Parse nội dung JSON đã sửa thành danh sách các đối tượng
        data = json.loads(fixed_content)
    except json.JSONDecodeError as e:
        print("Lỗi JSON khi decode:", e)
        return None
    # Chuyển danh sách các đối tượng thành DataFrame
    df = pd.DataFrame(data)
    return df
def extract_data(path_json, path_csv):
    data = []
    # Đọc dữ liệu log
    for file in read_allFile(path_json):
        df = read_json(file)
        if df is not None:
            data.append(df)
    # Hợp nhất tất cả các DataFrame nếu có
    if data:
        data = pd.concat(data, ignore_index=True)
    else:
        data = pd.DataFrame()
    # Đảm bảo thư mục processed tồn tại
    os.makedirs("./data/processed", exist_ok=True)
    
    # Nếu file tồn tại, xóa file trước (mặc dù to_csv sẽ ghi đè file nếu có)
    if os.path.exists(path_csv):
        os.remove(path_csv)
    data.to_csv(path_csv, index=False)  
