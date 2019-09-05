import pygame
import pygame.gfxdraw
from car_kinematic_model import Car, Game
import dynamic_window_approach
from car_kinematic_obstacle import update_object_mask
from read_write_trajectory import save_frame, resize_image, write_data
import numpy as np
import os
from car_kinematic_collision import Collision
import dynamic_window_approach as dwa
from math import radians, sqrt, pi
from math_util import get_arc_points, get_equidistant_points


def drive(car, car_data, index):
    car.position = (car_data[index][0], car_data[index][1])
    car.angle = car_data[index][2]
    index = (index + 1) % len(car_data)
    return index


class Replay(Game):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height)
        self.background = pygame.image.load("resources/backgrounds/maps_overlay.png").convert()
        self.background = pygame.transform.scale(self.background, (2500, 1261))
        self.bgWidth, self.bgHeight = self.background.get_rect().size
        self.dwa_config = None
        self.trajectory_file = None
        self.obstacle_file = None
        self.list_of_obstacles = None
        self.dwa_goal = None
        self.dwa_initial_state = None
        self.dwa_dts = list()

    def draw_trajectory(self, car, car_data, index):
        center_screen = (int(self.screen_width / 2), int(self.screen_height / 2))
        trajectory_points = []
        self.draw_trajectory_points(car, car_data, index, center_screen, trajectory_points)
        self.draw_trajectory_lines(trajectory_points)

    def draw_trajectory_points(self, car, car_data, index, center_screen, trajectory_points):
        for add_elem in range(5, 30, 5):
            delta_position = (
                car.position[0] - car_data[index + add_elem][0], car.position[1] - car_data[index + add_elem][1])
            traj_point = (center_screen[0] + int(delta_position[0] * self.ppu),
                          center_screen[1] + int(delta_position[1] * self.ppu))
            trajectory_points.append(traj_point)
            # draw each trajectory point
            pygame.draw.circle(self.screen, (255, 255, 0), traj_point, 7, 7)

    def draw_trajectory_lines(self, trajectory_points):
        for traj_point, next_traj_point in zip(trajectory_points, trajectory_points[1:]):
            pygame.draw.aaline(self.screen, (255, 255, 0), traj_point, next_traj_point, 10)

    def _update_map(self, car, rel_x, rel_y):
        self.screen.blit(self.background, (rel_x - self.bgWidth, rel_y - self.bgHeight))
        self.screen.blit(self.background, (rel_x, rel_y))
        self.screen.blit(self.background, (rel_x - self.bgWidth, rel_y))
        self.screen.blit(self.background, (rel_x, rel_y - self.bgHeight))

        rotated = pygame.transform.rotate(self.car_image, car.angle)
        center_x = int(self.screen_width / 2) - int(rotated.get_rect().width / 2)
        center_y = int(self.screen_height / 2) - int(rotated.get_rect().height / 2)

        # draw the ego car
        self.screen.blit(rotated, (center_x, center_y))

    def _get_dwa_goals(self, step):
        self.trajectory_file = os.path.join(os.path.dirname(__file__), "resources", "dwa_data", "reference.csv")
        traj_points = list()
        with open(self.trajectory_file, "r") as traj_file:
            lines = traj_file.readlines()
        for line in lines:
            numbers = line.split(",")
            traj_points.append((float(numbers[0]), float(numbers[1])))

        return [traj_points[i] for i in range(0, len(traj_points), step)]

    def _get_dwa_initial_state(self, car):
        """
        Get initial DWA state
        initial state [x(m), y(m), yaw(rad), v(m/s), omega(rad/s)]
        :param car:
        :return: numpy array representing initial state for DWA
        """
        return np.array([car.position[0], car.position[1], dwa.deg2rad(car.angle), 0.0, 0.0])

    def _prepare_dwa_planner(self, car):
        self.dwa_config = dwa.Config()
        self.dwa_initial_state = self._get_dwa_initial_state(car)
        self.dwa_u = np.array([0.0, 0.0])

    def get_obstacles(self, car, object_mask):
        # Front of the car
        # act_mask is a separate image where you can only see what the sensor sees
        center_rect = Collision.center_rect(self.screen_width, self.screen_height)
        mid_of_front_axle = Collision.point_rotation(car, -1, 16, center_rect)

        arc_points = get_arc_points(mid_of_front_axle, 150, radians(90 + car.angle), radians(270 + car.angle), 180)

        offroad_edge_points = []

        for end_point in arc_points:
            points_to_be_checked = list(get_equidistant_points(mid_of_front_axle, end_point, 25))
            check = False
            for line_point in points_to_be_checked:
                if np.array_equal(object_mask.get_at((int(line_point[0]), int(line_point[1]))), self.bkd_color):
                    check = True
                    offroad_edge_points.append(line_point)
                    break
            if check is False:
                offroad_edge_points.append(end_point)

        obstacle_point_list = list()
        for index in range(0, len(arc_points)):
            if offroad_edge_points[index] != arc_points[index]:
                pygame.draw.circle(self.screen,
                                   (255, 0, 0),
                                   (int(offroad_edge_points[index][0]), int(offroad_edge_points[index][1])),
                                   3,
                                   2)
                diff_x = (offroad_edge_points[index][0] - mid_of_front_axle[0]) / self.ppu
                diff_y = (offroad_edge_points[index][1] - mid_of_front_axle[1]) / self.ppu
                obstacle_point_list.append((car.position[0] - diff_x, car.position[1] - diff_y))
        return obstacle_point_list

    def map_car_coordinates_to_drawing_coordinates(self, car, coordinates):
        center_screen = (int(self.screen_width / 2), int(self.screen_height / 2))
        # trajectory 1
        trajectory_points = []
        for add_elem in range(0, len(coordinates)):
            delta_position = (
                car.position[0] - coordinates[add_elem][0],
                car.position[1] - coordinates[add_elem][1])
            x_coord = center_screen[0] + int(delta_position[0] * self.ppu)
            y_coord = center_screen[1] + int(delta_position[1] * self.ppu)
            if x_coord < 0:
                x_coord = 3
            if y_coord < 0:
                y_coord = 3
            traj_point = (x_coord, y_coord)
            trajectory_points.append(traj_point)
        return trajectory_points

    def replay_mode(self):
        self.init_traffic_cars()
        # place car on road
        car = Car(5, 27)
        object_mask = pygame.Surface((self.screen_width, self.screen_height))
        u = [0.0, 0.0]
        x = self._get_dwa_initial_state(car)
        self._prepare_dwa_planner(car)
        goals = self._get_dwa_goals(20)

        goal_idx = 0
        num_iterations = 0
        while not self.exit:
            collision_list = [False] * len(self.traffic_list)
            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # Drawing
            stagePosX = car.position[0] * self.ppu
            stagePosY = car.position[1] * self.ppu

            rel_x = stagePosX % self.bgWidth
            rel_y = stagePosY % self.bgHeight

            # blit (BLock Image Transfer) the seamless background
            self._update_map(car, rel_x, rel_y)

            # self.optimized_front_sensor(car)
            object_mask.fill((0, 0, 0))
            object_mask.blit(self.screen, (0, 0))
            update_object_mask(object_mask, rel_x, rel_y, self.bgWidth, self.bgHeight)
            stagePos = (stagePosX, stagePosY)
            self.check_collisions(collision_list)
            self.traffic_movement(collision_list, object_mask, stagePos)

            obstacles = np.array(self.get_obstacles(car=car, object_mask=object_mask))
            goal = goals[goal_idx]
            g_c = self.map_car_coordinates_to_drawing_coordinates(car, [goal])
            pygame.draw.circle(self.screen, (0, 255, 255), g_c[0], 3, 3)
            u, ltraj = dwa.dwa_control(x, u, self.dwa_config, goal, obstacles)

            traj_coordinates = self.map_car_coordinates_to_drawing_coordinates(car, ltraj)
            # draw each trajectory point
            for i in range(0, len(traj_coordinates)):
                pygame.draw.circle(self.screen, (255, 255, 0), traj_coordinates[i], 3, 3)

            x = dwa.motion(x, u, self.dwa_config.dt)
            self.record_data = False
            if self.record_data is True:
                write_data(os.path.join(os.path.dirname(__file__), "resources", "dwa_data", "dwa_path.csv"), x[0], x[1],
                           -dwa.rad2deg(x[2]))
                image_name = 'image_' + str(num_iterations) + '.png'
                save_frame(self.screen, image_name, os.path.join(os.path.dirname(__file__),
                                                                 'resources',
                                                                 'dwa_data',
                                                                 "images"))
            car.position = (x[0], x[1])
            car.angle = -dwa.rad2deg(x[2])
            num_iterations += 1

            if sqrt((x[0] - goal[0]) ** 2 + (x[1] - goal[1]) ** 2) <= self.dwa_config.robot_radius:
                goal_idx += 1
                if goal_idx == len(goals) - 1:
                    break
            if num_iterations >= 2000:
                break

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()


if __name__ == '__main__':
    screen = pygame.display.set_mode((1280, 720))
    game = Game(screen, 1280, 720)
    replay = Replay(game.screen, game.screen_width, game.screen_height)
    replay.replay_mode()
