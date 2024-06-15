from reinforcement_learning.enviroment import CustomPokerEnv
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor

from reinforcement_learning.save_best_callback import SaveOnBestTrainingRewardCallback

log_dir = "./logs/"

env = CustomPokerEnv(test=True)
env = Monitor(env, log_dir)

model = PPO('MlpPolicy', env, verbose=1, learning_rate=0.0003,
            device="cuda", tensorboard_log="./board/")

callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir, verbose=0)

model.learn(total_timesteps=200000, progress_bar=True, callback=callback)

model.save("ppo_poker_ai")

model = PPO.load("ppo_poker_ai")

obs, info = env.reset()
for _ in range(40):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, trunc, info = env.step(action)
    env.render()
    print(env.current_turn)
    if done:
        print("done")
        break
