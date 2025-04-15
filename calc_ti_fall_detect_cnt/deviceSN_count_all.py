from datetime import datetime, timedelta
from collections import defaultdict
import re, pandas as pd


def Data_Cleaning():
    # 定義文件名
    input_file = 'line_messages.txt'
    output_file = 'filtered_data.txt'

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # 檢查每一行是否匹配指定的模式
                if line.startswith("Site: ") or line.startswith("sn: ") or line.startswith("Frame Number TI: ") or line.startswith("Frame Number: ") or line.startswith("Time: "):
                    # 如果匹配，則寫入該行
                    outfile.write(line)
                else:
                    # 否則寫入一行空行
                    outfile.write('\n')
    except UnicodeDecodeError:
        print("解碼失敗，請檢查文件編碼，確保其為 UTF-8 或嘗試其他編碼格式。")
    except FileNotFoundError:
        print(f"找不到文件: {input_file}")



def count_sn_by_date(file_path, start_date, end_date, target_sn=None):
    date_counts = {}
    pattern_sn = "sn:\\s*([\\w]+)"
    # Modify the time pattern to specifically capture hh:mm:ss format
    pattern_time = "Time:\\s*([\\d\\-]+\\s([\\d]{2}:[\\d]{2}:[\\d]{2})\\.[\\d]+)"
    
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read()
    messages = lines.split("\n\n")
    sn_counts_by_date = defaultdict((lambda: defaultdict(int)))
    
    for message in messages:
        match_sn = re.search(pattern_sn, message)
        match_time = re.search(pattern_time, message)
        
        if match_sn:
            if match_time:
                sn = match_sn.group(1).strip()
                full_time_str = match_time.group(1).strip()
                time_str = match_time.group(2).strip()  # Extract the hh:mm:ss part
                
                # Ensure that the time matches exactly hh:mm:ss format
                if re.match(r"^\d{2}:\d{2}:\d{2}$", time_str):
                    time_format = "%Y-%m-%d %H:%M:%S.%f"
                    time = datetime.strptime(full_time_str, time_format)
                    if start_date <= time <= end_date:
                        print(f"sn: {sn}")
                        print(f"Time: {full_time_str}")
                        date_key = time.strftime("%Y-%m-%d")
                        for sn_ in target_sn:
                            if sn == sn_:
                                sn_counts_by_date[sn][date_key] += 1
                            else:
                                sn_counts_by_date[sn_][date_key] += 0
                else:
                    print("Time format is not hh:mm:ss")

            else:
                print("Date is not within the specified range")   # 20240711 revised by yuliia
        else:
            print("No matching data found")   # 20240711 revised by yuliia

    return sn_counts_by_date



def main():
    file_path = "filtered_data.txt"
    start_date = datetime(2023, 1, 25, 0, 0, 0)
    end_date = datetime(2026, 12, 31, 0, 0, 0)
    # 20240711 add device sn by yuliia
    
    Data_Cleaning()
    
    for field in range(0,11):
        if field == 0:
            #板榮
            target_sn = ('7e3fc7','7e40c7','7e4317','7e3fad','7e3fab','7e40e1','7e4257','7e4139','7e40d7','7e42ef','7e4007','7e41b7','7e3e19','7e43db','7e3f8d','7e452b','079f73','079ff1')            
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("vacbq_output.csv")
    
        elif field == 1: 
            #原民會
            target_sn = ('7e4401','7e445b','7e44d5','7e440b','7e439f','7e4435','7e4349','7e3ffd','7e4137','7e411d','7e3f6d','7e4053','7e4115','7e3df9','ae16a5','7e43b9','7e3f5b','7e439d','7e4561','7e42b5')            
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("cip_output.csv")

        elif field == 2: 
            #斗六
            target_sn = ('7e4135','7e438b',)  
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
        #    df.to_csv("d6_output.csv")
            
        elif field == 3: 
            #仁愛
            target_sn = ('7e4107','7e4217','7e3f8b','7e4213','7e434b','7e42bb','7e41c9','7e4347','7e41d7','7e4215','7e40f1','7e41c3','7e430f','7e410b','7e4369','7e419d','7e42f7','7e40d3','7e40eb','7e424d','7e424f','7e41f1','7e42cb','7e42f3')  
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("renai_output.csv")
        elif field == 4: 
            #四維
            target_sn = ('7e4509','7e3f29','7e425b','7e4189','ae10c9','ae0d73','7e3da7','7e3e0b','7e44bb','7e3ec9','7e3e7f','7e444f','7e4545','7e41ef','7e453d','7e418f','7e439b','7e40bb','7e44a3','7e44d3') 
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("eyon_output.csv")
        elif field == 5: 
            #西松
            target_sn = ('07700f','076f45','079ffd','07a041','07a20f','07a05b','07a203','076fc1','076f2f','07a0d3','076f95','7e43b3') 
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("hondao_output.csv")
        elif field == 6: 
            #璽悅明水館
            target_sn = ('ae147f','7e41b9','7e3d93','7e417b','7e4095','7e4359','7e41d9','7e3edb') 
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("macherie_output.csv")
        elif field == 7: 
            #仁康醫院
            target_sn = ('7e40f7','7e41bd','7e408b','7e3f49','7e43cd','7e4119','7e41ad','7e3e37','7e4517','7e3da1','7e4065','7e43b5','7e4333','7e400f','7e4177','7e4087','7e4093','7e412b','d75bcd','7e400d','7e4461','7e447d','adfe81','7e4029','7e3e8d','7e4171','7e3e63','7e40b9','7e4205','7e3f99','7e445f','7e43d1','7e3e49','7e412d') 
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("njkh_output.csv")
        elif field == 8: 
            #POC_彰榮
            target_sn = ('07a1ad','079fc3') 
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("poc_vacch_output.csv")
        elif field == 9: 
            #POC_葉爸爸
            target_sn = ('076eb3','07d2f9') 
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("poc_yehpapa_output.csv")
        elif field == 10: 
            #POC_中彰榮
            target_sn = ('07d2cb','076fad') 
            sn_counts = count_sn_by_date(file_path, start_date, end_date, target_sn)
            df = pd.DataFrame.from_dict(sn_counts, orient="index").fillna(0)
            df.to_csv("poc_vaczz_output.csv")
        else:
            #reserved
            print("No field matching data found")        


if __name__ == "__main__":
    main()