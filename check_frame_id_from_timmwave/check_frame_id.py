import json
import matplotlib.pyplot as plt

def read_log_file(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # 解析每行为字典
                entry = json.loads(line.strip())
                data.append(entry)
    except IOError:
        print(f"Error: Could not read file {file_path}")
    return data

def log_error(message, log_file):
    with open(log_file, 'a') as file:
        file.write(message + '\n')

def check_frame_ids(data, dt_threshold=0.033, log_file='error_log.txt'):
    previous_frame_id = None
    previous_dt = None
    total_frames = 0
    discontinuous_frames = 0
    excessive_dt_frames = 0
    excessive_dt_values = []

    for entry in data:
        current_frame_id = entry.get("frame_id")
        current_dt = entry.get("dt")
        total_frames += 1

        if previous_frame_id is not None:
            # 检查frame_id是否连续
            if not (current_frame_id == 0 and previous_frame_id == 65535) and not (current_frame_id == previous_frame_id + 1):
                error_message = f"Error: Unexpected frame_id sequence at {entry}"
                print(error_message)
                log_error(error_message, log_file)
                discontinuous_frames += 1

            # 检查dt是否超过阈值
            if previous_dt is not None and (current_dt - previous_dt) > dt_threshold:
                dt_difference = current_dt - previous_dt
                error_message = f"Error: dt difference too large at {entry} with difference {dt_difference:.6f}s"
                print(error_message)
                log_error(error_message, log_file)
                excessive_dt_frames += 1
                excessive_dt_values.append(dt_difference)

        previous_frame_id = current_frame_id
        previous_dt = current_dt

    discontinuous_ratio = (discontinuous_frames / total_frames) * 100 if total_frames > 0 else 0
    excessive_dt_ratio = (excessive_dt_frames / total_frames) * 100 if total_frames > 0 else 0
    
    print(f"Total frame_ids: {total_frames}")
    print(f"Discontinuous frame_ids: {discontinuous_frames}")
    print(f"Discontinuous ratio: {discontinuous_ratio:.2f}%")
    print(f"Excessive dt frames: {excessive_dt_frames}")
    print(f"Excessive dt ratio: {excessive_dt_ratio:.2f}%")
    
    return excessive_dt_values

def plot_thresholds_exceeded(thresholds_exceeded):
    plt.figure(figsize=(10, 6))
    plt.plot(thresholds_exceeded, marker='o', linestyle='-', color='b')
    plt.title('Dt Threshold Exceeded Levels')
    plt.xlabel('Frame Index')
    plt.ylabel('Threshold Exceeded Level')
    plt.grid(True)
    plt.show()

# 路径到日志文件
file_path = 'log.txt'

# 读取日志文件
data = read_log_file(file_path)

# 定义时间差的阈值（例如0.033秒）
dt_threshold = 0.033

# 设置错误日志的文件名
log_file = 'error_log.txt'

# 检查frame_id和dt差值，记录和输出超出的差值
excessive_dt_values = check_frame_ids(data, dt_threshold, log_file)

# 使用差值计算阈值超出倍数
thresholds_exceeded = [int(dt_difference // dt_threshold) for dt_difference in excessive_dt_values]

# 绘制图形
plot_thresholds_exceeded(thresholds_exceeded)
