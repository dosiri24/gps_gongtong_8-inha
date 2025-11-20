import math

def cal_length(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)

def process_length(datas):
    result = []

    for i in range(len(datas)):
        p1 = i
        p2 = i+1 if i+1 < len(datas) else 0

        distance = cal_length(
            [float(datas[p1][5]), float(datas[p1][6]), float(datas[p1][7])],
            [float(datas[p2][5]), float(datas[p2][6]), float(datas[p2][7])]
        )
        result.append(distance)
    return result
  
def cal_static(dxdydz): # 통계적 특성 (정밀도)
    dxs = [float(data[0]) for data in dxdydz]
    dys = [float(data[1]) for data in dxdydz]
    dzs = [float(data[2]) for data in dxdydz]
    
    #표준편차
    std_x = math.sqrt(sum([d**2 for d in dxs]) / len(dxs))
    std_y = math.sqrt(sum([d**2 for d in dys]) / len(dys))
    std_z = math.sqrt(sum([d**2 for d in dzs]) / len(dzs))
    
    #RMS
    sum_sq_3d = sum([x**2 + y**2 + z**2 for x, y, z in zip(dxs, dys, dzs)])
    rms_3d = math.sqrt(sum_sq_3d / len(dxdydz))
    
    return [std_x, std_y, std_z, rms_3d]

def cal_pos_error(phone_avg_xyz, rtk_avg_xyz): # phone 평균좌표와 rtk 평균좌표(참값) 차이 (정확도)
    error_x = float(phone_avg_xyz[5]) - float(rtk_avg_xyz[5])
    error_y = float(phone_avg_xyz[6]) - float(rtk_avg_xyz[6])
    error_z = float(phone_avg_xyz[7]) - float(rtk_avg_xyz[7])
    
    error_3d = math.sqrt(error_x**2 + error_y**2 + error_z**2) #3d 총오차
    error_2d = math.sqrt(error_x**2 + error_y**2) #2d 수평오차
    error_vert = abs(error_z) #수직오차
    
    return [error_x, error_y, error_z, error_2d, error_vert, error_3d]

if __name__ == "__main__":
    file = 'output.csv'
    phone_avg_datas = [] #[코너넘버][요소값]
    rtk_avg_datas = []#[코너넘버][요소값]
    phone_raw_dxdydz = {0: [], 1: [], 2: [], 3: []}
    rtk_raw_dxdydz = {0: [], 1: [], 2: [], 3: []}

    with open(file, 'r', encoding='utf-8') as data: # Receiver, CornerNum, Index, Sati, Longi, X, Y, Z, Dx, Dy, Dz
        lines = data.readlines()
        for line in lines:
            values = line.strip().split(',')

            if values[0] == 'Phone':
              if values[2] == 'Avg':
                  phone_avg_datas.append(values)
              else:
                  corner_num = int(values[1]) - 1
                  phone_raw_dxdydz[corner_num].append([values[8], values[9], values[10]])

            elif values[0] == 'RTK':
                if values[2] == 'Avg':
                    rtk_avg_datas.append(values)
                else:
                    corner_num = int(values[1]) - 1
                    rtk_raw_dxdydz[corner_num].append([values[8], values[9], values[10]])
                
    # 거리, 면적 계산
    print("\n==거리 및 면적 계산==")
    phone_distances = process_length(phone_avg_datas)
    for i in range(len(phone_distances)):
        next_point = (i+1) % len(phone_distances) + 1  # 다음 점 번호 계산 (1-2-3-4-1 순환)
        print(f"Phone 점{i+1}-점{next_point} 거리: {phone_distances[i]:.3f} m")

    phone_width = (phone_distances[0] + phone_distances[2]) / 2
    phone_length = (phone_distances[1] + phone_distances[3]) / 2
    phone_area = phone_width * phone_length
    print(f"Phone Area: {phone_area:.3f} m^2 | Width: {phone_width:.3f} m | Length: {phone_length:.3f} m\n")

    rtk_distances = process_length(rtk_avg_datas)
    for i in range(len(rtk_distances)):
        next_point = (i+1) % len(rtk_distances) + 1  # 다음 점 번호 계산 (1-2-3-4-1 순환)
        print(f"RTAP2U 점{i+1}-점{next_point} 거리: {rtk_distances[i]:.3f} m")
    
    rtk_width = (rtk_distances[0] + rtk_distances[2]) / 2
    rtk_length = (rtk_distances[1] + rtk_distances[3]) / 2
    rtk_area = rtk_width * rtk_length
    print(f"RTAP2U Area: {rtk_area:.3f} m^2 | Width: {rtk_width:.3f} m | Length: {rtk_length:.3f} m")
    
    for corner in range(4):
        print(f"\n ==점 {corner+1} 통계 분석==")
        print(f"[참값(RTAP2U)]: X={rtk_avg_datas[corner][5]}, Y={rtk_avg_datas[corner][6]}, Z={rtk_avg_datas[corner][7]}")
        print(f"[측정값(Phone)]: X={phone_avg_datas[corner][5]}, Y={phone_avg_datas[corner][6]}, Z={phone_avg_datas[corner][7]}")
        
        # Phone 정밀도
        precision = cal_static(phone_raw_dxdydz[corner])
        print(f"\n폰 n데이터 분산(표준편차)")
        print(f"Std x: {precision[0]:.3f} m")
        print(f"Std y: {precision[1]:.3f} m")
        print(f"Std z: {precision[2]:.3f} m")
        print(f"RMS 3D: {precision[3]:.3f} m")
        
        # RTK 정밀도
        rtk_precision = cal_static(rtk_raw_dxdydz[corner])
        print(f"\nRTK n데이터 분산(표준편차)")
        print(f"Std x: {rtk_precision[0]:.3f} m")
        print(f"Std y: {rtk_precision[1]:.3f} m")
        print(f"Std z: {rtk_precision[2]:.3f} m")
        print(f"RMS 3D: {rtk_precision[3]:.3f} m")
        
        #정확도
        print(f"\n참값과의 오차")
        accuracy = cal_pos_error(phone_avg_datas[corner], rtk_avg_datas[corner])
        print(f"Error x: {accuracy[0]:.3f} m")
        print(f"Error y: {accuracy[1]:.3f} m")
        print(f"Error z: {accuracy[2]:.3f} m")
        print(f"Error 2D: {accuracy[3]:.3f} m")
        print(f"Error Vert: {accuracy[4]:.3f} m")
        print(f"Error 3D: {accuracy[5]:.3f} m")
        

