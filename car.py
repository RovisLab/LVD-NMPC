from pygame.math import Vector2
from math import tan, radians, degrees, copysign
import random


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=30.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 15
        self.brake_deceleration = 30
        self.free_deceleration = 5

        self.acceleration = 0.0
        self.steering = 0.0

    def reset_car(self, rs_pos_list):
        rand_pos = random.choice(rs_pos_list)
        self.position = (rand_pos[0], rand_pos[1])
        self.angle = rand_pos[2]

    def accelerate(self, dt):
        if self.velocity.x < 0:
            self.acceleration = self.brake_deceleration
        else:
            self.acceleration += 10 * dt

    def brake(self, dt):
        if self.velocity.x > 0:
            self.acceleration = -self.brake_deceleration
        else:
            self.acceleration -= 10 * dt

    def handbrake(self, dt):
        if abs(self.velocity.x) > dt * self.brake_deceleration:
            self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
        else:
            self.acceleration = -self.velocity.x / dt

    def cruise(self, dt):
        if abs(self.velocity.x) > dt * self.free_deceleration:
            self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
        else:
            if dt != 0:
                self.acceleration = -self.velocity.x / dt

    def steer_right(self, dt):
        self.steering -= 180 * dt

    def steer_left(self, dt):
        self.steering += 180 * dt

    def no_steering(self):
        self.steering = 0

    def update(self, dt):
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        if self.angle < 0:
            self.angle = 360 + self.angle
        if self.angle > 360:
            self.angle = self.angle - 360
