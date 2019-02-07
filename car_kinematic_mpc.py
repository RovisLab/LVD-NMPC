from car_kinematic_model import Game, Car
import pygame
from read_write_trajectory import read_coords
from math import copysign, cos, sin
import numpy as np
import ctypes
from threading import Thread
import math
import matplotlib
from mpc_development import MPCController
matplotlib.use("TkAgg")
prev_ref_index = 40
video_writer = None
MUL_FACTOR = 1


class MPCGame(Game):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, False, False)
        self.mpc_input_data = None
        self.mpc_trajectory_points = []
        self.mpc_delta = 0
        self.mpc_acc = 0
        self.mpc_angle = 0
        self.mpc_coords = [0, 0]

    def run_mpc(self):
        # place car on road
        global MUL_FACTOR
        car = Car(MUL_FACTOR*5, MUL_FACTOR*27)
        car.max_velocity = 10
        self.mpc_coords[0] = car.position[0]
        self.mpc_coords[1] = car.position[1]
        car_data = read_coords("resources/mpc_ref.csv")
        car_data = np.multiply(car_data, MUL_FACTOR)
        thread = Thread(target=self.run_dll, args=())
        thread.start()

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # User input
            pressed = pygame.key.get_pressed()

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 10 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 10 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
            if pressed[pygame.K_RIGHT]:
                car.steering -= 180 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 180 * dt
            else:
                car.steering = 0
            car.steering = np.rad2deg(self.mpc_delta)
            #print(self.mpc_delta)
            car.acceleration = self.mpc_acc

            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt)

            # Drawing
            stagePosX = car.position[0] * self.ppu
            stagePosY = car.position[1] * self.ppu

            rel_x = stagePosX % self.bgWidth
            rel_y = stagePosY % self.bgHeight

            # blit (BLock Image Transfer) the seamless background
            self.screen.blit(self.background, (rel_x - self.bgWidth, rel_y - self.bgHeight))
            self.screen.blit(self.background, (rel_x, rel_y))
            self.screen.blit(self.background, (rel_x - self.bgWidth, rel_y))
            self.screen.blit(self.background, (rel_x, rel_y - self.bgHeight))

            rotated = pygame.transform.rotate(self.car_image, car.angle)
            center_x = int(self.screen_width / 2) - int(rotated.get_rect().width / 2)
            center_y = int(self.screen_height / 2) - int(rotated.get_rect().height / 2)

            # draw the ego car
            self.screen.blit(rotated, (center_x, center_y))

            self.draw_trajectory(car, car_data)
            self.mpc_coords[0] = car.position[0]
            self.mpc_coords[1] = car.position[1]
            self.mpc_angle = car.angle
            pygame.display.update()

            self.clock.tick(60)
        pygame.quit()

    def draw_trajectory(self, car, car_data):
        # draw trajectory
        center_screen = (int(self.screen_width / 2), int(self.screen_height / 2))

        trajectory_points = []
        waypoints = []
        min = 1000
        idx = -1
        global prev_ref_index
        for elem in range(prev_ref_index-40, prev_ref_index+40):
            dx = car_data[elem][0] - car.position[0]
            dy = car_data[elem][1] - car.position[1]
            d = abs(math.sqrt(dx**2+dy**2))
            if d < min:
                min = d
                idx = elem
                prev_ref_index = idx

        for add_elem in range(idx, idx + 150, 15):
            if add_elem < len(car_data):
                delta_position = (
                    car.position[0] - car_data[add_elem][0],
                    car.position[1] - car_data[add_elem][1])
                x_point = center_screen[0] + int(delta_position[0] * self.ppu)
                y_point = center_screen[1] + int(delta_position[1] * self.ppu)
                traj_point = (x_point, y_point)
                trajectory_points.append(traj_point)

                if len(waypoints) < 9:
                    waypoints.append((car_data[add_elem][0], car_data[add_elem][1]))

                # draw each trajectory point
                pygame.draw.circle(self.screen, (255, 255, 0), traj_point, 2, 2)

        # draw lines between trajectory points
        for traj_point, next_traj_point in zip(trajectory_points, trajectory_points[1:]):
            pygame.draw.aaline(self.screen, (255, 255, 0), traj_point, next_traj_point, 10)
        self.prepare_mpc_input(car, waypoints)
        if len(self.mpc_trajectory_points) > 0:
            for traj_point, next_traj_point in zip(self.mpc_trajectory_points, self.mpc_trajectory_points[1:]):
                pygame.draw.aaline(self.screen, (0, 255, 0), traj_point, next_traj_point, 10)

    def prepare_mpc_input(self, car, waypoints):
        self.mpc_input_data = (ctypes.c_double * 14)()
        for index in range(6):
            self.mpc_input_data[index*2] = waypoints[index][0]
        for index in range(6):
            self.mpc_input_data[index*2+1] = waypoints[index][1]
        self.mpc_input_data[12] = np.deg2rad(car.angle)
        self.mpc_input_data[13] = car.velocity[0]

    def run_dll(self):
        controller = MPCController(target_speed=30)
        while True:
            mpc_solution = controller.control(self.mpc_input_data)
            self.mpc_delta = mpc_solution[0]
            self.mpc_acc = mpc_solution[1]
            self.draw_mpc_prediction(mpc_solution)

    def draw_mpc_prediction(self, mpc_solution):
        center_screen = (int(self.screen_width / 2), int(self.screen_height / 2))
        self.mpc_trajectory_points = []
        for index in range(2, 20, 2):
            delta_position = (
                 -mpc_solution[index] * cos(-np.deg2rad(self.mpc_angle)) + mpc_solution[index + 1] * sin(-np.deg2rad(self.mpc_angle)),
                 -mpc_solution[index] * sin(-np.deg2rad(self.mpc_angle)) - mpc_solution[index + 1] * cos(-np.deg2rad(self.mpc_angle)))
            x_point = center_screen[0] + int(delta_position[0] * self.ppu)
            y_point = center_screen[1] + int(delta_position[1] * self.ppu)
            traj_point = (x_point, y_point)
            self.mpc_trajectory_points.append(traj_point)


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    mpc = MPCGame(screen, 1280, 720)
    mpc.run_mpc()
