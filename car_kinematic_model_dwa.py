import os
import pygame
import pygame.gfxdraw
from math import radians
from checkbox import Checkbox
from car_kinematic_collision import Collision
from car_kinematic_debug import Debug
from read_write_trajectory import write_data, read_traffic_data
from car import Car
from math_util import *
from car_kinematic_obstacle import update_object_mask
from traffic_car import TrafficCar
import dynamic_window_approach as dwa


class Game:
    def __init__(self, screen, screen_width, screen_height,
                 traffic=True,
                 record_data=False):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        # the color of the green background, used to detect if the car is on/off road

        # Yellow
        self.bkd_color = [255, 255, 0, 255]
        # Green
        # self.bkd_color = [0, 88, 0, 255]
        # Olive
        # self.bkd_color = [83, 125, 10, 255]

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.current_dir, "resources/cars/car_eb_2.png")
        self.car_image = pygame.image.load(self.image_path).convert_alpha()
        self.car_image = pygame.transform.scale(self.car_image, (42, 20))
        self.ppu = 16

        self.traffic_list = []

        self.traffic_image_path = os.path.join(self.current_dir, "resources/cars/car_traffic.png")
        self.traffic_car_image = pygame.image.load(self.traffic_image_path).convert_alpha()
        self.traffic_car_image = pygame.transform.scale(self.traffic_car_image, (42, 20))

        self.object_car_image_path = os.path.join(self.current_dir, "resources/cars/object_car.png")
        self.object_car_image = pygame.image.load(self.object_car_image_path).convert_alpha()
        self.object_car_image = pygame.transform.scale(self.object_car_image, (42, 20))

        self.background = pygame.image.load(
            os.path.join(self.current_dir, "resources/backgrounds/maps_overlay.png")).convert()
        self.background = pygame.transform.scale(self.background, (2500, 1261))
        self.bgWidth, self.bgHeight = self.background.get_rect().size
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        self.input_image = pygame.surfarray.array3d(self.screen)

        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.record_data = record_data
        self.traffic = traffic
        self.traffic_obstacle_points = list()

    def on_road(self, car, screen):
        Ox = 32
        Oy = 16
        center_world_x = int(self.screen_width / 2)
        center_world_y = int(self.screen_height / 2)

        bot_right_x = center_world_x + int(Ox * cos(radians(-car.angle))) - int(Oy * sin(radians(-car.angle)))
        bot_right_y = center_world_y + int(Ox * sin(radians(-car.angle))) + int(Oy * cos(radians(-car.angle)))

        bot_left_x = center_world_x - int(Ox * cos(radians(-car.angle))) - int(Oy * sin(radians(-car.angle)))
        bot_left_y = center_world_y - int(Ox * sin(radians(-car.angle))) + int(Oy * cos(radians(-car.angle)))

        top_left_x = center_world_x - int(Ox * cos(radians(-car.angle))) + int(Oy * sin(radians(-car.angle)))
        top_left_y = center_world_y - int(Ox * sin(radians(-car.angle))) - int(Oy * cos(radians(-car.angle)))

        top_right_x = center_world_x + int(Ox * cos(radians(-car.angle))) + int(Oy * sin(radians(-car.angle)))
        top_right_y = center_world_y + int(Ox * sin(radians(-car.angle))) - int(Oy * cos(radians(-car.angle)))

        if (np.array_equal(screen.get_at((bot_right_x, bot_right_y)), self.bkd_color) or np.array_equal
            (screen.get_at((bot_left_x, bot_left_y)), self.bkd_color) or
                np.array_equal(screen.get_at((top_left_x, top_left_y)), self.bkd_color) or
                np.array_equal(screen.get_at((top_right_x, top_right_y)), self.bkd_color)):
            Debug.debug_text(screen, "test")
            Collision.offroad(car)
            return False
        else:
            return True

    def compute_sensor_distance(self, car, base_point, sensor_length, sensor_angle, data_screen, draw_screen):
        end_point_x = base_point[0] + sensor_length * cos(radians(sensor_angle - car.angle))
        end_point_y = base_point[1] + sensor_length * sin(radians(sensor_angle - car.angle))

        for index in range(0, sensor_length):
            coll_point_x = base_point[0] + index * cos(radians(sensor_angle - car.angle))
            coll_point_y = base_point[1] + index * sin(radians(sensor_angle - car.angle))

            if np.array_equal(data_screen.get_at((int(coll_point_x), int(coll_point_y))), self.bkd_color):
                break

        pygame.draw.line(draw_screen, (0, 255, 0), base_point, (coll_point_x, coll_point_y), True)
        pygame.draw.line(draw_screen, (255, 0, 0), (coll_point_x, coll_point_y), (end_point_x, end_point_y), True)

        coll_point = (coll_point_x, coll_point_y)

        distance = euclidean_norm(base_point, coll_point)
        # print(distance)

        return distance

    def optimized_front_sensor(self, car, object_mask, act_mask, display_obstacle_on_sensor=False):
        # act_mask is a separate image where you can only see what the sensor sees
        center_rect = Collision.center_rect(self.screen_width, self.screen_height)
        mid_of_front_axle = Collision.point_rotation(car, -1, 16, center_rect)

        arc_points = get_arc_points(mid_of_front_axle, 150, radians(90 + car.angle), radians(270 + car.angle), 320)

        offroad_edge_points = []

        for end_point in arc_points:
            points_to_be_checked = list(get_equidistant_points(mid_of_front_axle, end_point, 25))

            check = False

            for line_point in points_to_be_checked:
                if (np.array_equal(object_mask.get_at((int(line_point[0]), int(line_point[1]))), self.bkd_color)):
                    check = True
                    break

            if (check == False):
                offroad_edge_points.append(end_point)
            else:
                offroad_edge_points.append(line_point)

        obstacle_point_list = list()
        for index in range(0, len(arc_points)):
            if (offroad_edge_points[index] == arc_points[index]):
                pygame.draw.line(self.screen, (0, 255, 0), mid_of_front_axle, arc_points[index], True)
                pygame.draw.line(act_mask, (0, 255, 0), mid_of_front_axle, arc_points[index], True)
            else:
                diff_x = offroad_edge_points[index][0] - mid_of_front_axle[0]
                diff_y = offroad_edge_points[index][1] - mid_of_front_axle[1]
                coords = (car.position[0] + diff_x, car.position[1] + diff_y)
                obstacle_point_list.append(coords)
                pygame.draw.circle(self.screen,
                                   (255, 255, 255),
                                   (int(offroad_edge_points[index][0]), int(offroad_edge_points[index][1])),
                                   3,
                                   2)
                pygame.draw.line(self.screen, (0, 255, 0), mid_of_front_axle, offroad_edge_points[index], True)
                pygame.draw.line(act_mask, (0, 255, 0), mid_of_front_axle, offroad_edge_points[index], True)

                if display_obstacle_on_sensor is True:
                    pygame.draw.line(self.screen, (255, 0, 0), offroad_edge_points[index], arc_points[index], True)
                    pygame.draw.line(act_mask, (255, 0, 0), offroad_edge_points[index], arc_points[index], True)
        self.traffic_obstacle_points.extend(obstacle_point_list)

    def optimized_rear_sensor(self, car, object_mask, act_mask, display_obstacle_on_sensor=False):
        # act_mask is a separate image where you can only see what the sensor sees
        center_rect = Collision.center_rect(self.screen_width, self.screen_height)
        mid_of_rear_axle = Collision.point_rotation(car, 65, 16, center_rect)

        arc_points = get_arc_points(mid_of_rear_axle, 150, radians(-90 + car.angle), radians(90 + car.angle), 320)

        offroad_edge_points = []

        for end_point in arc_points:
            points_to_be_checked = list(get_equidistant_points(mid_of_rear_axle, end_point, 25))

            check = False

            for line_point in points_to_be_checked:
                if (np.array_equal(object_mask.get_at((int(line_point[0]), int(line_point[1]))), self.bkd_color)):
                    check = True
                    break

            if (check == False):
                offroad_edge_points.append(end_point)
            else:
                offroad_edge_points.append(line_point)

        for index in range(0, len(arc_points)):
            if (offroad_edge_points[index] == arc_points[index]):
                pygame.draw.line(self.screen, (0, 255, 0), mid_of_rear_axle, arc_points[index], True)
                pygame.draw.line(act_mask, (0, 255, 0), mid_of_rear_axle, arc_points[index], True)
            else:
                pygame.draw.line(self.screen, (0, 255, 0), mid_of_rear_axle, offroad_edge_points[index], True)
                pygame.draw.line(act_mask, (0, 255, 0), mid_of_rear_axle, offroad_edge_points[index], True)
                if display_obstacle_on_sensor is True:
                    pygame.draw.line(self.screen, (255, 0, 0), offroad_edge_points[index], arc_points[index], True)
                    pygame.draw.line(act_mask, (255, 0, 0), offroad_edge_points[index], arc_points[index], True)

    def enable_sensor(self, car, data_screen, draw_screen):
        center_rect = Collision.center_rect(self.screen_width, self.screen_height)
        mid_of_front_axle = Collision.point_rotation(car, 0, 16, center_rect)
        #mid_of_rear_axle = Collision.point_rotation(car, 65, 16, center_rect)
        # pygame.draw.circle(self.screen, (255, 255, 0), (mid_of_front_axle[0], mid_of_front_axle[1]), 5)
        distance = np.array([])
        for angle_index in range(120, 240, 24):
            distance = np.append(distance,
                                 self.compute_sensor_distance(car, mid_of_front_axle, 200, angle_index, data_screen,
                                                              self.screen))
        # for angle_index in range(300, 360, 4):
        #     self.compute_sensor_distance(car, mid_of_rear_axle, 200, angle_index, data_screen, draw_screen)
        # for angle_index in range(0, 60, 4):
        #     self.compute_sensor_distance(car, mid_of_rear_axle, 200, angle_index, data_screen, draw_screen)
        return distance

    def draw_sim_environment(self, car, object_mask, cbox_front_sensor, cbox_rear_sensor, print_coords=False,
                             record_coords=False, file_path=None, file_name=None,
                             record_traffic_car_coords=False, traffic_file_path=None, traffic_file_name=None):
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

        cbox_front_sensor.update()
        cbox_rear_sensor.update()

        rotated = pygame.transform.rotate(self.car_image, car.angle)
        rot_rect = rotated.get_rect()

        center_x = int(self.screen_width / 2) - int(rot_rect.width / 2)
        center_y = int(self.screen_height / 2) - int(rot_rect.height / 2)

        # draw the ego car
        self.screen.blit(rotated, (center_x, center_y))
        object_mask.fill((0, 0, 0))
        object_mask.blit(self.screen, (0, 0))
        update_object_mask(object_mask, rel_x, rel_y, self.bgWidth, self.bgHeight)

        if print_coords is True:
            myfont = pygame.font.SysFont('Arial', 30)
            text1 = myfont.render('Car pos x: ' + str(round(stagePosX, 2)), True, (250, 0, 0))
            text2 = myfont.render('Car pos y: ' + str(round(stagePosY, 2)), True, (250, 0, 0))
            text3 = myfont.render('rel x: ' + str(round(rel_x, 2)), True, (250, 0, 0))
            text4 = myfont.render('rel y: ' + str(round(rel_y, 2)), True, (250, 0, 0))
            text5 = myfont.render('velocity: ' + str(round(car.velocity.x, 2) * self.ppu/4) + ' km/h', True, (250, 0, 0))

            self.screen.blit(text1, (20, 20))
            self.screen.blit(text2, (20, 50))
            self.screen.blit(text3, (20, 80))
            self.screen.blit(text4, (20, 110))
            self.screen.blit(text5, (20, 140))

        # Record ego_car positions in GridSim
        if record_coords is True:
            if file_name is None:
                print('no file name given')
                quit()
            if file_path is None:
                print('no file path given')
                quit()
            write_data(file_path + '/' + file_name, round(stagePosX, 2), round(stagePosY, 2), round(rel_x, 2),
                       round(rel_y, 2), (round(car.velocity.x, 2) * self.ppu/4))

        # Record traffic car trajectory
        if record_traffic_car_coords is True:
            if traffic_file_name is None:
                print('no file name given')
                quit()
            if traffic_file_path is None:
                print('no file path given')
                quit()
            write_data(traffic_file_path + '/' + traffic_file_name, stagePosX, stagePosY, car.angle)

        return stagePosX, stagePosY, rel_x, rel_y

    def key_handler(self, car, dt, rs_pos_list):
        # User input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
            car.reset_car(rs_pos_list)
        if pressed[pygame.K_UP]:
            car.accelerate(dt)
        elif pressed[pygame.K_DOWN]:
            car.brake(dt)
        elif pressed[pygame.K_SPACE]:
            car.handbrake(dt)
        else:
            car.cruise(dt)
        if pressed[pygame.K_RIGHT]:
            car.steer_right(dt)
        elif pressed[pygame.K_LEFT]:
            car.steer_left(dt)
        else:
            car.no_steering()

    def event_handler(self, cbox_front_sensor, cbox_rear_sensor, mouse_button_pressed):
        # Event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if cbox_front_sensor.onCheckbox(mouse_pos) and mouse_button_pressed == False:
                    cbox_front_sensor.changeState()
                if cbox_rear_sensor.onCheckbox(mouse_pos) and mouse_button_pressed == False:
                    cbox_rear_sensor.changeState()
                mouse_button_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_button_pressed = False

    @staticmethod
    def traffic_car_collision(traffic_car_1, traffic_car_2, collision_list, collision_index):
        for x1, y1 in zip(traffic_car_1.data_x[traffic_car_1.index: traffic_car_1.index + 40], traffic_car_1.data_y[
                                                                                               traffic_car_1.index:
                                                                                               traffic_car_1.index + 40]):
            for x2, y2 in zip(traffic_car_2.data_x[traffic_car_2.index: traffic_car_2.index + 40], traffic_car_2.data_y[
                                                                                                   traffic_car_2.index:
                                                                                                   traffic_car_2.index + 40]):
                if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 20:
                    collision_list[collision_index] = True

    def init_traffic_cars(self):
        trajectories = read_traffic_data(os.path.join(self.current_dir, "resources/traffic_cars_data/traffic_trajectories.csv"))
        for trajectory in trajectories:
            traffic_car = TrafficCar(trajectory[0], int(trajectory[1]))
            self.traffic_list.append(traffic_car)

    def check_collisions(self, collision_list):
        for i in range(0, len(self.traffic_list) - 1):
            for j in range(i + 1, len(self.traffic_list)):
                self.traffic_car_collision(self.traffic_list[i], self.traffic_list[j], collision_list, j)

    def traffic_movement(self, collision_list, object_mask, stagePos):
        for i in self.traffic_list:
            if collision_list[self.traffic_list.index(i)]:
                i.index -= 1
            i.trajectory(stagePos, self.screen, object_mask, self.traffic_car_image, self.object_car_image,
                         2 * self.bgWidth,
                         2 * self.bgHeight)

    def run(self):
        # place car on road
        car = Car(5, 27)

        # initialize traffic
        self.init_traffic_cars()

        # sensor checkboxes on top right corner
        cbox_front_sensor = Checkbox(self.screen_width - 200, 10, 'Enable front sensor', True)
        cbox_rear_sensor = Checkbox(self.screen_width - 200, 35, 'Enable rear sensor', True)

        # reset position list -> to be updated
        rs_pos_list = [[650, 258, 90.0], [650, 258, 270.0], [0, 0, 180.0], [0, 0, 0.0], [302, 200, 45.0],
                       [40, 997, 0.0], [40, 997, 180.0], [100, 997, 0.0], [100, 997, 180.0], [400, 998, 0.0],
                       [400, 998, 180.0], [385, 315, 135.0]]

        # boolean variable needed to check for single-click press
        mouse_button_pressed = False

        # initialize object mask
        object_mask = pygame.Surface((self.screen_width, self.screen_height))

        if self.record_data is True:
            index_image = 0

        while not self.exit:
            # VARIABLE_UPDATE
            if self.traffic is True:
                collision_list = [False] * len(self.traffic_list)

            dt = self.clock.get_time() / 1000

            self.event_handler(cbox_front_sensor, cbox_rear_sensor, mouse_button_pressed)

            # LOGIC
            self.key_handler(car, dt, rs_pos_list)
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # DRAWING
            stagePos = self.draw_sim_environment(car, object_mask, cbox_front_sensor, cbox_rear_sensor,
                                                 print_coords=True)
            relPos = (stagePos[2], stagePos[3])
            stagePos = (stagePos[0], stagePos[1])

            # UPDATE
            # ------------------------ traffic car -----------------------------------------------
            if self.traffic is True:
                self.check_collisions(collision_list)
                self.traffic_movement(collision_list, object_mask, stagePos)
            # -------------------------------------------------------------------------------------------
            car.update(dt)

            act_mask = pygame.Surface((self.screen_width, self.screen_height))
            if cbox_front_sensor.isChecked():
                self.optimized_front_sensor(car, object_mask, act_mask, display_obstacle_on_sensor=True)
            if cbox_rear_sensor.isChecked():
                self.optimized_rear_sensor(car, object_mask, act_mask, display_obstacle_on_sensor=True)

            if self.record_data is True:
                image_name = 'image_' + str(index_image) + '.png'
                print(index_image)
                index_image += 1

            if self.record_data is True:
                # RECORD TAB

                # Save replay
                # Write reference trajectory
                write_data(os.path.join(os.path.dirname(__file__), "recorded_data", "reference.csv"),
                           car.position, car.angle)
                write_data(os.path.join(os.path.dirname(__file__), "recorded_data", "obstacles.csv"),
                           self.traffic_obstacle_points)

            # reset obstacle point list
            self.traffic_obstacle_points = list()

            pygame.display.update()
            self.clock.tick(self.ticks)

        pygame.quit()


if __name__ == '__main__':
    screen = pygame.display.set_mode((1280, 720))
    game = Game(screen=screen, screen_width=1280, screen_height=720, record_data=True, traffic=True)
    game.run()

	