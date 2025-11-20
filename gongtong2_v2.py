import math

def cal_length(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)

def print_length(datas):
        for i in range(len(datas)):
            p1 = i
            p2 = i+1 if i+1 < len(datas) else 0

            distances = cal_length(
                [float(datas[p1][5]), float(datas[p1][6]), float(datas[p1][7])],
                [float(datas[p2][5]), float(datas[p2][6]), float(datas[p2][7])]
            )
            print(f"{datas[p1][1]}-{datas[p2][1]} 거리: {distances:.3f} m")

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

    print("=== Phone 거리 계산 ===")
    print_length(phone_avg_datas)

    print("\n=== RTK 거리 계산 ===")
    print_length(rtk_avg_datas)
