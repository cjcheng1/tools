import cv2
import mediapipe as mp
import time

# 初始化 MediaPipe Pose 模組
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 打開網絡攝像頭
cap = cv2.VideoCapture(0)  # 替換為你的攝像頭地址

cap.set(cv2.CAP_PROP_FRAME_WIDTH,960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,800)


sit_count = 0
stand_count = 0
prev_position = None
threshold = 0.03  # 用於判斷關鍵點的位置變化的閾值

def detect_pose(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    return results.pose_landmarks

def get_position(landmarks):
    if landmarks:
        nose = landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        left_hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        
        # 假如膝蓋在臀部之上且鼻子位於相對較高的位置時表示站立
        # 膝蓋在臀部之下且鼻子位於相對較低的位置時表示坐下
        #for test
        print("nose.y=" ,nose.y, "knee=",left_knee.y,"hip=",left_hip.y,"\t\r")
        #print
        #print("l_knee.y=",left_knee.y,"left_hip.=y",left_hip.y,  " ===========> threshold and nose.y=",threshold and nose.y ,"left_hip.y = ",left_hip.y )

        #if left_knee.y > left_hip.y + threshold and nose.y > left_hip.y:
        #    return 'Sitting'
        if (nose.y < 0.3) and ((left_knee.y - left_hip.y) >0.25):
            return 'Sitting'
        elif (nose.y > 0.3) and ((left_knee.y - left_hip.y) < 0.15):
            return 'Standing'

    return None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    landmarks = detect_pose(frame)
    current_position = get_position(landmarks)
    #time.sleep(0.1)
    
    if current_position != prev_position:
        if current_position == 'Sitting':
            sit_count += 1
        elif current_position == 'Standing':
            stand_count += 1        
        prev_position = current_position
    
    # 在影像上標出關鍵點
    if landmarks:
        nose = landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        left_hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        
        # 獲取影像的高度和寬度
        h, w, _ = frame.shape



        # 轉換到像素座標
        nose_x, nose_y = int(nose.x * w), int(nose.y * h)
        hip_x, hip_y = int(left_hip.x * w), int(left_hip.y * h)
        knee_x, knee_y = int(left_knee.x * w), int(left_knee.y * h)

        #print("nose_x=",nose_x, "   nose_y=",nose_y)
        
        # 畫出關鍵點
        cv2.circle(frame, (nose_x, nose_y), 10, (0, 255, 0), -1)  # 綠色表示鼻子
        cv2.circle(frame, (hip_x, hip_y), 10, (255, 0, 0), -1)   # 藍色表示臀部
        cv2.circle(frame, (knee_x, knee_y), 10, (0, 0, 255), -1) # 紅色表示膝蓋
    
    # 在影像上顯示計數
    cv2.putText(frame, f'Sit Count: {sit_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Stand Count: {stand_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.putText(frame, f'nose: {nose.y}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'hip: {left_hip.y}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'knee: {left_knee.y}', (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(5) & 0xFF == 27:  # 按 ESC 鍵退出
        break

cap.release()
cv2.destroyAllWindows()
