from enum import Enum
from math import copysign


class Actions(Enum):
    acc = 0
    left = 1
    right = 2
    brake = 3
    no_action = 4
    acc_left = 5
    acc_right = 6
    reverse = 7


def apply_action(predicted_action, car, dt):
    if predicted_action == Actions.acc.value or predicted_action == Actions.acc_left.value or predicted_action == Actions.acc_right.value:
        if car.velocity.x < 0:
            car.acceleration = car.brake_deceleration
        else:
            car.acceleration += 10 * dt
    elif predicted_action == Actions.reverse.value:
        if car.velocity.x > 0:
            car.acceleration = -car.brake_deceleration
        else:
            car.acceleration -= 10 * dt
    elif predicted_action == Actions.brake.value:
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

    if predicted_action == Actions.right.value or predicted_action == Actions.acc_right.value:
        car.steering -= 180 * dt
    elif predicted_action == Actions.left.value or predicted_action == Actions.acc_left.value:
        car.steering += 180 * dt
    else:
        car.steering = 0
    car.steering = max(-car.max_steering, min(car.steering, car.max_steering))