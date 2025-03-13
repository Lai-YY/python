import pandas as pd
import sys

file_path = input("輸入檔案位置及檔名(包含附檔名):")
output_path1 = input('輸出"全院電簽"路徑及檔名(包含附檔名):')
output_path2 = input('輸出"急診病歷"路徑及檔名(包含附檔名):')
output_path3 = input('輸出"電簽表單"路徑及檔名(包含附檔名):')

try:
    # 檢查是否包含指定的工作表
    excel_file = pd.ExcelFile(file_path)  # 加載 Excel 文件
    if '全院電簽' not in excel_file.sheet_names:
        print("未將工作表名稱修改為 '全院電簽',修改完再重新執行")
        sys.exit()  # 提前結束程序
    else:
        # 如果存在，讀取指定的工作表
        df = pd.read_excel(file_path, sheet_name='全院電簽')
except FileNotFoundError:
    print(f"找不到檔案: {file_path}")
    
    sys.exit()


#輸紐函數
def process_and_write_pivot(data, writer, sheet_name, index_columns):
    if data.empty:
        print(f"警告: '{sheet_name}' 沒有符合條件的數據，將跳過！")
        return

    # 建立樞紐分析表
    pivot_table = pd.pivot_table(
        data,
        values=['24小時簽章量', '簽核量', '總量'],
        index=index_columns,  # 多個索引欄位可作為列表傳入
        aggfunc='sum'
    )
    # 計算簽章率並格式化（百分比，保留兩位小數）
    pivot_table['24小時簽章率'] = (pivot_table['24小時簽章量'] / pivot_table['簽核量']) * 100
    pivot_table['總簽章率'] = (pivot_table['簽核量'] / pivot_table['總量']) * 100
    pivot_table = pivot_table.round(2)  # 保留小數點後兩位

    # 寫入指定的 Excel 工作表
    pivot_table.to_excel(writer, sheet_name=sheet_name)

# 假設你已經有輸入的 DataFrame `df` 和輸出檔案路徑

with pd.ExcelWriter(output_path1, engine='openpyxl') as writer1:
    # 處理 "身分別" 為 'N' 的護理師資料
    nurse_data = df[df['身分別'] == 'N']
    process_and_write_pivot(nurse_data, writer1, '護理師', ['員代', '名稱'])
    process_and_write_pivot(nurse_data, writer1, '護理單位', ['單位'])
    #刪除科別
    '''
    del_departments = [
    '乳房外科', '家庭醫學科', '新陳代謝科', '病理科', '中醫', '外科部', 
    '急診醫學', '放射腫瘤科', '放射診斷科', '核子醫學', '牙科', 
    '癌症中心', '皮膚科', '精神醫學部', '麻醉科'
    ]
    '''
    # 處理 "身分別" 為 'D' 的醫師資料
    doctor_data = df[df['身分別'] == 'D']
    #若有科別需要刪除
    #select_doctor_data = doctor_data[~doctor_data['單位'].isin(del_departments)]   
    process_and_write_pivot(doctor_data, writer1, '醫師', ['員代', '名稱'])
    process_and_write_pivot(doctor_data, writer1, '科別', ['單位'])  

print("輸出'全院電簽'至指定位置")
print(" ")

with pd.ExcelWriter(output_path2, engine='openpyxl') as writer2:
    selected_forms = [
        "急診護理記錄",
        ]
    
    form_data = df[df['表單名稱'].isin(selected_forms)]
    process_and_write_pivot(form_data, writer2, '急診護理記錄', ['員代', '名稱','表單名稱'])
    
    selected_forms = [
        "急診護理病歷",
        ]
    
    form_data = df[df['表單名稱'].isin(selected_forms)]
    process_and_write_pivot(form_data, writer2, '急診護理病歷', ['員代', '名稱','表單名稱']) 
    
print("輸出'急診病歷'至指定位置")
print(" ")


df = pd.read_excel(file_path, sheet_name=u'全院電簽')
with pd.ExcelWriter(output_path3, engine='openpyxl') as writer3:
    selected_forms = [
        "入院病歷紀錄", "手術記錄", "出院病歷摘要", "住院病人護理紀錄單",
        "住院醫、藥囑病歷", "放射線部醫療影像報告", "門診病歷",
        "急診護理病歷", "急診護理記錄", "病程紀錄", "會診回覆單",
        "檢查報告", "檢驗報告", "轉科(床)病歷記錄"
        ]
        
    form_data = df[df['表單名稱'].isin(selected_forms)]
    process_and_write_pivot(form_data, writer3, '表單電簽', ['表單名稱'])
    
print("輸出'電簽表單'至指定位置")




    



