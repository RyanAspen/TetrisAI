from TetrisAICollection import TetrisAICollection

collection = TetrisAICollection()
collection.train_model()
#collection.validateEnv()


#from TetrisEnvironment import TetrisEnvironment
#from tf_agents.environments import tf_py_environment
#import cv2
#import numpy as np
#from tf_agents.policies import random_tf_policy
#def getRGBGrid(grid):
#    colors = np.array([[255,255,255], [135,206,235], [0,0,139],[255,165,0], [0,255,0], [128, 0, 128], [255,0,0], [255,255,0], [0,0,0]], dtype=np.uint8)
#    rgbGrid = np.zeros((280, 160, 3), dtype=np.uint8)
#    for r in range(28):
#        for c in range(16):
#            for a in range(10):
#                for b in range(10):
#                    for x in range(3):
#                        rgbGrid[(r*10)+a][(c*10)+b][x] = colors[grid[27-r][c]][x]
#    return rgbGrid

#def create_video(policy, env, pyEnv):
#    print("Creating Video")
#    time_step = env.reset()
#    grid = np.array(pyEnv.currentGame.grid)
#    frameWidth, frameHeight = (280, 160)
#    videoName = "test.avi"
#    out = cv2.VideoWriter(videoName, cv2.VideoWriter_fourcc(*'DIVX'), 0.25, (frameHeight, frameWidth))
#    out.write(getRGBGrid(pyEnv.currentGame.grid))
#    while not time_step.is_last():
#        action_step = policy.action(time_step)
#        time_step = env.step(action_step.action)
#        out.write(getRGBGrid(pyEnv.currentGame.grid))
#    out.release()
#    print("Finished Video")

#train_env_py = TetrisEnvironment()
#train_env = tf_py_environment.TFPyEnvironment(train_env_py)
#random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(), train_env.action_spec())
#create_video(random_policy, train_env, train_env_py)
