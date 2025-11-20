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
        

if __name__ == "__main__":
    file = 'output.csv'
    phone_avg_datas = [] #[코너넘버][요소값]
    rtk_avg_datas = []

    with open(file, 'r', encoding='utf-8') as data: # Receiver, CornerNum, Index, Sati, Longi, X, Y, Z, Dx, Dy, Dz
        lines = data.readlines()
        for line in lines:
            values = line.strip().split(',')
            if values[2] == 'Avg' and values[0] == 'Phone':
                phone_avg_datas.append(values)
            elif values[2] == 'Avg' and values[0] == 'RTK':
                rtk_avg_datas.append(values)

    phone_distances = process_length(phone_avg_datas)
    for i in range(len(phone_distances)):
        print(f"Phone 점{i+1}-점{(i+2) if (i+2)<=len(phone_distances) else 1} 거리: {phone_distances[i]:.3f} m")

    phone_width = (phone_distances[0] + phone_distances[2]) / 2
    phone_length = (phone_distances[1] + phone_distances[3]) / 2
    phone_area = phone_width * phone_length

    rtk_distances = process_length(rtk_avg_datas)
    
    rtk_width = (rtk_distances[0] + rtk_distances[2]) / 2
    rtk_length = (rtk_distances[1] + rtk_distances[3]) / 2
    rtk_area = rtk_width * rtk_length

    print(f"Phone Area: {phone_area:.3f} m^2 | Width: {phone_width:.3f} m | Length: {phone_length:.3f} m")
    print(f"RTK Area: {rtk_area:.3f} m^2 | Width: {rtk_width:.3f} m | Length: {rtk_length:.3f} m")
