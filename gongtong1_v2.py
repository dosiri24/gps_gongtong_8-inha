import math

def get_gps_from_nmea(file_path): # [위도, N or S, 경도, E or W, 고도, 해발고도]
    def nmea2deg(input):
        degree = int(float(input)/100)
        minute = float(input) - degree*100  
        result = degree + (minute/60)  

        return result

    nmedata = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            temp = line.strip().split(',')
            result = []
            
            if temp[0] == '$GNGGA' or temp[0] == '$GPGGA': #gnss or gps
                

                result.append(nmea2deg(temp[2]))  #0: 위도 float
                result.append(temp[3])  #1: N or S str
                result.append(nmea2deg(temp[4]))  #2: 경도 float
                result.append(temp[5])  #3: E or W str
                result.append(float(temp[9]))  #4: 고도 float
                result.append(float(temp[11])) #5: 해발 고도 float
                
                nmedata.append(result)
                
    return nmedata
    
def latlong2xyz(lati, longi, alti):
    lati_rad = math.radians(lati)
    longi_rad = math.radians(longi)
    a = 6378137  #(m) WGS84 장축 반경
    e = 0.0818191908426215 #WGS84 이심률
    b = a * math.sqrt(1 - e**2) #(m) WGS84 단축 반경

    N = (a**2) / math.sqrt(((a**2)*(math.cos(lati_rad)**2)) + (b**2)* (math.sin(lati_rad)**2)) #묘유선 곡률반경

    x = (N + alti) * math.cos(lati_rad) * math.cos(longi_rad)
    y = (N + alti) * math.cos(lati_rad) * math.sin(longi_rad)
    z = (((b**2)/(a**2))*N + alti) * math.sin(lati_rad)
    
    return x, y, z

def cal_avg_and_dxdydz(corner_data):
    dxdydz = []
    xxs, yys, zzs = [], [], [] 
    
    for data in corner_data:
        lati = data[0]
        longi = data[2]
        alti = data[4] + data[5]
        x, y, z = latlong2xyz(lati, longi, alti)
        xxs.append(x)
        yys.append(y)
        zzs.append(z)
        
    avg_x = sum(xxs) / len(xxs)
    avg_y = sum(yys) / len(yys)
    avg_z = sum(zzs) / len(zzs)
    
    for i in range(len(xxs)):
        dx = xxs[i] - avg_x
        dy = yys[i] - avg_y
        dz = zzs[i] - avg_z
        
        dxdydz.append([dx, dy, dz])
        
    return [avg_x, avg_y, avg_z], [xxs, yys, zzs], dxdydz

def save_csv(receiver_type, corner_num, avg_xyz, all_xyz, dxdydz , satilongi):
    filename = "output.csv"
    
    with open(filename, 'a', encoding='utf-8') as file:
        for i in range(len(all_xyz[0])):
            dx, dy, dz = dxdydz[i]
            index = i
            file.write(f"{receiver_type},{corner_num},{index},{satilongi[i][0]},{satilongi[i][2]},{all_xyz[0][i]},{all_xyz[1][i]},{all_xyz[2][i]},{dx},{dy},{dz}\n")
        index = 'Avg'
        file.write(f"{receiver_type},{corner_num},{index},{None},{None},{avg_xyz[0]},{avg_xyz[1]},{avg_xyz[2]},0,0,0\n")

if __name__ == "__main__":
    phone_corners = {1: [], 2: [], 3: [], 4: []} #[꼭짓점번호][gngga데이터리스트][내부값]]
    rtk_corners = {1: [], 2: [], 3: [], 4: []}  #[꼭짓점번호][gngga데이터리스트][내부값]]
    corners = 4
    
    with open("output.csv", 'w', encoding='utf-8') as f:
        f.write("Receiver, CornerNum, Index, Sati, Longi, X, Y, Z, Dx, Dy, Dz\n")
    
    for i in range(1, 1+corners):
        phone_file_path = f"phone_data/phone{i}.txt"
        rtk_file_path = f"rtk_data/rtk{i}.txt"
        phone_corners[i] = (get_gps_from_nmea(phone_file_path))
        rtk_corners[i] = (get_gps_from_nmea(rtk_file_path))
        
    for i in range(1, 1+corners):     
        avg_phone_xyz, all_phone_xyz, phone_dxdydz = cal_avg_and_dxdydz(phone_corners[i])
        save_csv("Phone", i, avg_phone_xyz, all_phone_xyz, phone_dxdydz, phone_corners[i])
    
    for i in range(1, 1+corners):     
        avg_rtk_xyz, all_rtk_xyz, rtk_dxdydz = cal_avg_and_dxdydz(rtk_corners[i])
        save_csv("RTK", i, avg_rtk_xyz, all_rtk_xyz, rtk_dxdydz, rtk_corners[i])
        
            