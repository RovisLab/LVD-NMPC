from math import sin, cos, radians


class Collision:
    @staticmethod
    def offroad(car, bounding_factor=1.2):
        car.velocity.x = -car.velocity.x / bounding_factor
        car.velocity.y = -car.velocity.y / bounding_factor
        car.acceleration = 0

    @staticmethod
    def center_rect(width, height):
        x = int(width / 2)
        y = int(height / 2)
        return x, y

    @staticmethod
    def point_rotation(car, x, y, center_rect, ox = 32, oy = 16):
        rotated_x = center_rect[0] + int((x - ox) * cos(radians(-car.angle))) + int((y - oy) * sin(radians(-car.angle)))
        rotated_y = center_rect[1] + int((x - ox) * sin(radians(-car.angle))) - int((y - oy) * cos(radians(-car.angle)))
        return rotated_x, rotated_y
