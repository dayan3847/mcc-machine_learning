import numpy as np

from dayan3847.reinforcement_learning.agent.Agent import Agent


class KnowledgeModel:
    def read_q_value(self,
                     s: np.array,  # state
                     a: int,  # action
                     ) -> float:
        pass

    def update_q_value(self,
                       s: np.array,  # state (normalmente seria el estado previo)
                       a: int,  # action
                       q: float,  # q_value
                       ):
        pass

    def save_knowledge(self):
        pass

    def load_knowledge(self):
        pass

    def reset_knowledge(self):
        pass


class HistoryItem:
    def __init__(self,
                 state: np.array,
                 action: int,
                 q: float,
                 random: bool,
                 ):
        self.state: np.array = state
        self.action: int = action
        self.q: float = q
        self.random: bool = random
        self.reward: float | None = None


class TemporalDifferenceLearningAgent(Agent):
    def __init__(self, action_count: int, knowledge_model: KnowledgeModel):
        super().__init__(action_count)
        self.alpha = .1
        self.gamma = 1
        self.epsilon = .1
        self.knowledge_model: KnowledgeModel = knowledge_model

        self.history: list[HistoryItem] = []

        self.algorithm_name: str = 'td_learning'

    def select_an_action_policy_e_greedy(self,
                                         s: np.array,  # State
                                         a: int | None = None  # if is not None, then is the action to apply per force
                                         ) -> int:
        q = None
        ran = False
        if a is not None:
            q = self.knowledge_model.read_q_value(s, a)
        elif np.random.random() < self.epsilon:
            a = self.select_an_action_random()
            ran = True
            q = self.knowledge_model.read_q_value(s, a)
        else:
            a, q, _ = self.select_an_action_best_q(s)

        self.history.append(HistoryItem(s, a, q, ran))

        return a

    def select_an_action_best_q(self, s: np.array) -> tuple[int, float, bool]:  # best_action, best_q_value
        # Obtener la lista de valores Q de todas las acciones para el estado "s"
        q_values: list[float] = self.read_q_values_x_actions(s)
        best_q_value = np.max(q_values)
        best_actions_list = np.argwhere(q_values == best_q_value).flatten()
        best_actions_list_len = len(best_actions_list)
        best_action = best_actions_list[best_actions_list_len // 2]
        # print('max: a: {} q: {}'.format(best_action, best_q_value))
        return int(best_action), float(best_q_value), False

    def read_q_values_x_actions(self, s: np.array) -> list[float]:
        return [self.knowledge_model.read_q_value(s, a) for a in range(self.action_count)]

    def save_knowledge(self):
        self.knowledge_model.save_knowledge()


class QLearningAgent(TemporalDifferenceLearningAgent):
    def __init__(self, action_count: int, knowledge_model: KnowledgeModel):
        super().__init__(action_count, knowledge_model)
        self.algorithm_name = 'qlearning'

    def select_an_action(self,
                         s: np.array,  # State
                         a: int | None = None  # if is not None, then is the action to apply per force
                         ) -> int:
        return self.select_an_action_policy_e_greedy(s, a)

    def train_action(self,
                     s: np.array,  # State
                     r_prev: float,  # reward prev
                     ):
        self.history[-1].reward = r_prev
        q_prev: float = self.history[-1].q
        a_prev: int = self.history[-1].action
        s_prev: np.array = self.history[-1].state
        q_max: float = self.select_an_action_best_q(s)[1]

        _q_fixed: float = q_prev + self.alpha * (r_prev + self.gamma * q_max - q_prev)
        self.knowledge_model.update_q_value(s_prev, a_prev, _q_fixed)


class SarsaAgent(TemporalDifferenceLearningAgent):
    def __init__(self, action_count: int, knowledge_model: KnowledgeModel):
        super().__init__(action_count, knowledge_model)
        self.A: int | None = None
        self.algorithm_name = 'sarsa'

    def select_an_action(self,
                         s: np.array,  # State
                         a: int | None = None  # if is not None, then is the action to apply per force
                         ) -> int:
        if self.A is None:
            self.A = self.select_an_action_policy_e_greedy(s, a)
        else:
            self.A = self.select_an_action_policy_e_greedy(s, self.A)

        return self.A

    def train_action(self,
                     s: np.array,  # S'
                     r_prev: float,  # R
                     ):
        self.history[-1].reward = r_prev
        Sp: np.array = s
        R: float = r_prev
        S: np.array = self.history[-1].state
        A: int = self.history[-1].action
        Q_SA: float = self.history[-1].q
        Ap: int = self.select_an_action_policy_e_greedy(Sp)
        # Q(S',A')
        Q_SpAp = self.history.pop().q

        Q_SA_fixed: float = Q_SA + self.alpha * (R + self.gamma * Q_SpAp - Q_SA)
        self.knowledge_model.update_q_value(S, A, Q_SA_fixed)
        self.A = Ap
