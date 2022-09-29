import gym
import cv2
import numpy as np

env = gym.make("PongDeterministic-v4", render_mode="human", frameskip=1, repeat_action_probability=0)
print(env.unwrapped.get_action_meanings())

obs = env.reset()
# env.unwrapped.ale.setRAM(57,255) # Set lives to 255
env.unwrapped.ale.setDifficulty(0)

action = 1
cv2.namedWindow("Output", cv2.WINDOW_NORMAL)

import time

pre_action = 2

video_writer = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 90, (160,210))

pre_y_ball = 0
pre_x_ball = 0

for i in range(10_0000):
    obs,_,_,done,_ = env.step(action)
    video_writer.write(obs[:,:,::-1])
    pre_action = action
    action = 1
    
    ball_roi = obs[34:192]
    bat_roi = obs[34:192]
    
    # Find ball location
    mask = cv2.inRange(ball_roi, (200,200,200), (255,255,255))
    ret,_,_,centroids_ball = cv2.connectedComponentsWithStats(mask)
    
    # Find bat location
    mask = cv2.inRange(bat_roi, (90,180,90), (100,200,100))
    ret,_,_,centroids_bat = cv2.connectedComponentsWithStats(mask)
    cv2.imshow("mask", mask)
    
    action = 1 # FIRE


    # Choose action based on locations of ball and bat
    if len(centroids_ball) > 1 and len(centroids_bat) > 1:

        y_ball = centroids_ball[1][1] + 34
        x_ball = centroids_ball[1][0]
        slop = (y_ball-pre_y_ball)/(x_ball-pre_x_ball)

        target_x = 141
        target_y = pre_y_ball + (target_x - pre_x_ball) * slop
        pre_x_ball, pre_y_ball = x_ball, y_ball
        cv2.line(obs,np.int0((pre_x_ball, pre_y_ball)), np.int0((x_ball, y_ball)), (0,0,255), 2)
        try:
            cv2.line(obs,np.int0((pre_x_ball, pre_y_ball)), np.int0((target_x, target_y)), (0,0,255), 2)
        except:
            pass
        y_bat = centroids_bat[1][1] + 34
        cv2.circle(obs, (140, int(y_bat)), 4, (255,0,0),-1)
        
        if target_y > y_bat + 2:
            action = 3
            # print("RIGHT")
        elif target_y < y_bat - 2:
            action = 4
            # print("LEFT")
        else:
            if x_ball < 135:
                action = pre_action
            else:
                action = 0#pre_action

    
    cv2.imshow("Output", obs)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if done:
        break

video_writer.release()