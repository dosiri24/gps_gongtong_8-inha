
def get_gps_from_nmea(file_path):
    nmedata = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            temp = line.strip().split(',')
            result = []
            
            if temp[0] == '$GNGGA' or temp[0] == '$GPGGA': #gnss or gps
                result.append(float(temp[2])/100)  #0: 위도 float
                result.append(temp[3])  #1: N or S str
                result.append(float(temp[4])/100)  #2: 경도 float
                result.append(temp[5])  #3: E or W str
                result.append(float(temp[9]))  #4: 고도 float
                result.append(float(temp[11])) #5: 해발 고도 float
                
                nmedata.append(result)
                
    return nmedata
    
if __name__ == "__main__":
    phone_corners = {1: [], 2: [], 3: [], 4: []} #[꼭짓점번호][gngga데이터리스트][내부값]]
    rtk_corners = {1: [], 2: [], 3: [], 4: []}  #[꼭짓점번호][gngga데이터리스트][내부값]]
    
    for i in range(1, 5):
        phone_file_path = f"phone_data/phone{i}.txt"
        rtk_file_path = f"rtk_data/rtk{i}.txt"
        phone_corners[i] = (get_gps_from_nmea(phone_file_path))
        rtk_corners[i] = (get_gps_from_nmea(rtk_file_path))
        
    print(phone_corners[1][1])