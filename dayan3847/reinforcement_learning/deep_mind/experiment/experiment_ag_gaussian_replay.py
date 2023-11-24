import numpy as np
from dm_control import suite
from dm_control.rl.control import Environment
from dm_control import viewer
from dm_env import TimeStep

from dayan3847.reinforcement_learning.deep_mind.functions_deep_mind import get_action_values, get_state
from dayan3847.reinforcement_learning.deep_mind.agent.QLearningAgentGaussian import QLearningAgentGaussian

random_state = np.random.RandomState(42)
env: Environment = suite.load(domain_name='cartpole',
                              task_name='balance',
                              task_kwargs={
                                  'random': random_state,
                              },
                              visualize_reward=True)

f_name: str = '20231124021704'

app = viewer.application.Application(title='Q-Learning Agent Gaussian Replay "{}"'.format(f_name))
action_count = 7
action_values: np.array = get_action_values(env, action_count)

ag = QLearningAgentGaussian(action_count)
ag.knowledge_model.save_knowledge('epc/{}_knowledge.csv'.format(f_name))

h_actions = np.loadtxt(f'epc/{f_name}_actions.txt').astype(np.int32)
counter: int = 0
r = None


def init_episode():
    global counter, r
    counter = 0
    r = 1


def policy_agent(time_step: TimeStep):
    global ag, action_values, h_actions, counter, r
    s = get_state(time_step)
    if time_step.first():
        init_episode()
    else:
        r = float(time_step.reward)
        ag.train_action(s, r)

    a = h_actions[counter]
    a = ag.select_an_action(s, a)
    counter += 1

    av = action_values[a]

    if r < .35:
        app._restart_runtime()

    if counter == 1000:
        ag.knowledge_model.save_knowledge('epc/{}_knowledge.csv'.format(f_name))

    print('action: {}({}) step: {}/{} r: {}'.format(a, av, counter, 1000, r))
    return av


if __name__ == '__main__':
    # viewer.launch(env, policy=policy_agent)
    app.launch(env, policy=policy_agent)