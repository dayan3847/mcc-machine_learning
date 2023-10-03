import pygame

from dayan3847.reinforcement_learning.case_1d import Agent, Environment, AgentPhysical


class GrapherPyGame(Agent):
    R = 20

    def __init__(self, env: Environment):
        super().__init__(env)
        self.window = None
        self.window_size = (600, 600)

    def draw(self):
        # background color
        self.window.fill((255, 255, 255))
        # print grid
        for _x in range(-1 * self.env.MAX[0] + 1, self.env.MAX[0]):
            pygame.draw.circle(
                self.window,
                (200, 200, 200),
                self.convert_point((_x, 0)),
                GrapherPyGame.R,
            )
        for agent in self.env.agents:
            if not isinstance(agent, AgentPhysical):
                continue
            pygame.draw.circle(
                self.window,
                agent.color,
                self.convert_point(agent.point),
                GrapherPyGame.R,
            )
        pygame.display.update()

    def convert_point(self, point):
        return (
            int((point[0] + self.env.MAX[0]) * self.window_size[0] / (2 * self.env.MAX[0])),
            int(self.window_size[1] - (point[1] + self.env.MAX[1]) * self.window_size[1] / (2 * self.env.MAX[1])),
        )

    def run_callback(self):
        pygame.display.set_caption('Pointing Simulation')
        self.window = pygame.display.set_mode(self.window_size)
        while self.running:
            self.draw()
            self.check_close()
        pygame.quit()

    def check_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.env.stop()
        keys = pygame.key.get_pressed()
        # if press 'q' key, stop simulation
        if keys[pygame.K_q]:
            self.env.stop()
