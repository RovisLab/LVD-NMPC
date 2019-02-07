from car import Car
from read_write_trajectory import read_coords
import pygame
import car_kinematic_config as config
import os


class TrafficCar(Car):
    def __init__(self, data_file, index, x=0, y=0, angle=0.0, length=4, max_steering=30, max_acceleration=30.0):
        current_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        super().__init__(x, y, angle, length, max_steering, max_acceleration)
        self.data = read_coords(os.path.join(current_dir, "resources/traffic_cars_data/" + data_file). replace('\\', '/'))
        self.data_x = [x[0] for x in self.data]
        self.data_y = [x[1] for x in self.data]
        self.index = index

    def trajectory(self, stagePos, screen, object_mask, traffic_car_image, object_car_image, bgWidth, bgHeight):
        # ------------------------- Infinite traffic cars -----------------------------------
        min_pos_x = min(self.data_x)
        min_pos_y = min(self.data_y)
        max_pos_x = max(self.data_x)
        max_pos_y = max(self.data_y)
        if stagePos[0] >= bgWidth + min_pos_x - config.screen_width / 2:
            self.data_x = [x + bgWidth for x in self.data_x]
        if stagePos[1] >= bgHeight + min_pos_y - config.screen_height / 2:
            self.data_y = [x + bgHeight for x in self.data_y]
        if stagePos[0] <= max_pos_x - bgWidth + config.screen_width / 2:
            self.data_x = [x - bgWidth for x in self.data_x]
        if stagePos[1] <= max_pos_y - bgHeight + config.screen_height / 2:
            self.data_y = [x - bgHeight for x in self.data_y]
        # ------------------------------------------------------------------------------------
        pos_x = self.data_x[self.index]
        pos_y = self.data_y[self.index]
        if abs(pos_x - stagePos[0]) <= config.screen_width / 2:
            if abs(pos_y - stagePos[1]) <= config.screen_height / 2:
                self.angle = self.data[self.index][2]
                rotated = pygame.transform.rotate(traffic_car_image, self.angle)
                obj_rotated = pygame.transform.rotate(object_car_image, self.angle)
                x = abs(config.screen_width / 2 - (pos_x - stagePos[0]) - 10)
                y = abs(config.screen_height / 2 - (pos_y - stagePos[1]) - 10)
                screen.blit(rotated, (x, y))
                object_mask.blit(obj_rotated, (x, y))
        self.index = (self.index + 1) % len(self.data)

