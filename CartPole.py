import gym
gym.logger.set_level(40)
import random



class Trainer():
    def __init__(self):
        self.env = gym.make("CartPole-v1")
        self.agent = Agent(self.env)

    def fun_action(self):
        for episode in range(100):
            print("-----------------episode:", episode)
            state = self.env.reset()
            done = False
            t = 0
            while not done:
                t += 1
                print("step:", t)
                action = self.agent.get_action(state)
                state, reward, done, info = self.env.step(action)
                rollout = [state, reward, done]
                ''' self.agent.memory.remember(rollout)'''
                self.env.render()
                '''if len(self.agent.memory.done) >= 4000:
                    self.agent.learn()
                    self.agent.memory.clear()

class Memory():
    def __init__(self):
        pass # TODO: memory nin kendi state reward done tutucuları olsun
    def remember(self, rollout):
        pass # TODO: bu metot içine gelen datayı kendi hafızasına kaydedecek
    def clear(self):
        pass # TODO: bu metot memory nin kendi hafızasını silicek, boşaltıcak, temizlicek'''

class Agent():
    def __init__(self, env):
        ''' self.memory = Memory()'''
        self.action_sizen = env.action_space.n

    def get_action(self, state):
        pole_angle = state[2]
        action = 0 if pole_angle < 0 else 1
        return action

    def learn(self):
        pass



trainer = Trainer()
trainer.fun_action()

