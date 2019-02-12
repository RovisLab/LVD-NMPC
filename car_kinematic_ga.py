from deap import base, creator, tools, algorithms
from keras.layers import Dense
from keras.models import Sequential
from keras.models import model_from_json
import pygame
import pygame.gfxdraw
from car import Car
from math_util import *
import pickle
import time
from car_kinematic_model import Game
from action_handler import *
from read_write_trajectory import write_data
population = []


class NeuroTrainer(object):
    def __init__(self, population_size=20, num_generations=30, init_ind_func=None):
        self.population_size = population_size
        self.num_generations = num_generations
        self.init_individual = init_ind_func
        self.best_individual = None

    def train(self, eval_function):
        # fitness function, maximizes the accuracy
        creator.create('FitnessMax', base.Fitness, weights=(1.0,))
        # tie fitness function to individual
        creator.create('Individual', list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()

        # create an individual with the random selection attribute
        toolbox.register("individual", creator.Individual, self.init_individual())
        # declare population of indivduals
        toolbox.register('population', tools.initRepeat, list, toolbox.individual)

        # mate
        toolbox.register('mate', tools.cxBlend, alpha=0)
        # mutate
        toolbox.register('mutate', tools.mutGaussian, mu=0, sigma=3, indpb=0.3)

        # selectia
        toolbox.register('select', tools.selTournament, tournsize=10)
        # evaluare
        toolbox.register('evaluate', eval_function, population_size=self.population_size)

        # training
        global population
        population = toolbox.population(n=self.population_size)
        # self.load_population("./np_population/pop_generation_38.pkl")
        r = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.5, ngen=self.num_generations, verbose=False)
        self.best_individual = tools.selBest(population, k=1)

    def load_population(self, path_to_data):
        with open(path_to_data, 'rb') as input:
            global population
            population = pickle.load(input)

    def test(self, test_features, test_labels, test_function):
        test_function(self.best_individual, test_features, test_labels)

    @staticmethod
    def save_population_data(path_where_to_save, generation_idx):
        global population
        with open(path_where_to_save + 'pop_generation_' + str(generation_idx) + '.pkl', 'wb') as output:
            pickle.dump(population, output, pickle.HIGHEST_PROTOCOL)


class GAGame(Game):
    def __init__(self,screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, False, False)
        pygame.display.set_caption("Car kinematic GA model")

        # Green
        self.bkd_color = [0, 87, 0, 255]
        self.background = pygame.image.load("resources/backgrounds/seamless_road_2000_2000_Green_No_Crossroads_2.png").convert()
        self.bgWidth, self.bgHeight = self.background.get_rect().size

    def run_ga(self, nn_model):
        # place car on road
        car = Car(pygame.display.get_surface().get_width() / self.ppu / 2,
                  pygame.display.get_surface().get_height() / self.ppu / 2 - 24)
        # 100,997 for seamless complex road
        car.max_steering = 27
        car.max_velocity = 30
        # car.velocity[0] = car.max_velocity
        global_distance = 0
        predicted_action = -1
        single_save_elite = False
        sanity_check = 15
        avg_vel_vec = np.array([])
        while not self.exit:
            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            current_position = [0, 0]
            next_position = [0, 0]
            current_position[0], current_position[1] = car.position[0], car.position[1]

            if predicted_action != Actions.reverse.value:
                apply_action(predicted_action, car, dt)

            # Logic
            car.update(dt)

            if not self.on_road(car, self.screen):
                break

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
            rot_rect = rotated.get_rect()

            center_x = int(self.screen_width / 2) - int(rot_rect.width / 2)
            center_y = int(self.screen_height / 2) - int(rot_rect.height / 2)

            # draw the ego car
            self.screen.blit(rotated, (center_x, center_y))

            sensor_distances = self.enable_sensor(car, self.screen, self.screen)
            input_data = np.append(sensor_distances, car.velocity[0])
            input_data_tensor = np.reshape(input_data, (1, input_data.shape[0]))
            prediction = nn_model.predict(input_data_tensor)
            predicted_action = np.argmax(prediction[0])

            myfont = pygame.font.SysFont('Arial', 30)
            text = myfont.render('Car velocity: ' + str(round(car.velocity[0], 2)), True, (255, 0, 255))
            self.screen.blit(text, (20, 20))
            pygame.display.update()

            next_position = car.position[0], car.position[1]
            local_distance = round(
                np.sqrt((current_position[0] - next_position[0]) ** 2 + (current_position[1] - next_position[1]) ** 2),
                4)
            if local_distance == 0:
                sanity_check -= 1
            else:
                sanity_check = 15
            if sanity_check < 0:
                break

            global_distance += local_distance
            avg_vel_vec = np.append(avg_vel_vec, car.velocity[0])
            # print(self.clock.get_fps())

            self.clock.tick(self.ticks)
            if global_distance > 2000 and (single_save_elite == False):
                timestr = time.strftime("%Y%m%d_%H%M")
                model_json = nn_model.to_json()
                with open("./models/model_" + str(global_distance) + ".json", "w") as json_file:
                    json_file.write(model_json)
                # serialize weights to HDF5
                nn_model.save_weights("./models/model_" + str(global_distance) + ".h5")
                print("Saved model to disk")
                single_save_elite = True
        pygame.quit()
        avg_vel = np.mean(avg_vel_vec)
        return global_distance, avg_vel


class KinematicGA(object):
    def __init__(self, shape, num_actions):
        self.model = self.build_classifier(shape, num_actions)
        self.valid_layer_names = ['hidden1', 'hidden2', 'hidden3']
        self.layer_weights, self.layer_shapes = self.init_shapes()
        self.individual_idx = 0
        self.generation_idx = 0
        self.generative_ptsX = []
        self.generative_ptsY = []

    def build_classifier(self, shape, num_actions):
        # create classifier to train
        classifier = Sequential()

        classifier.add(
            Dense(units=6, input_dim=shape, activation='relu', name='hidden1', kernel_initializer='glorot_uniform',
                  bias_initializer='zeros'))

        classifier.add(Dense(units=7, activation='relu', kernel_initializer='glorot_uniform', name='hidden2',
                             bias_initializer='zeros'))

        classifier.add(
            Dense(units=int(num_actions), activation='softmax', kernel_initializer='glorot_uniform', name='hidden3',
                  bias_initializer='zeros'))

        # Compile the CNN
        classifier.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return classifier

    def neuro_eval(self, individual, population_size):
        # get the weights, extract weights from individual, change the weights with evo weights
        individual = np.asarray(individual)
        for layer_name, weight, bias in zip(self.valid_layer_names, self.layer_shapes[0::2], self.layer_shapes[1::2]):
            self.model.get_layer(layer_name).set_weights(
                [individual[weight[0]:weight[0] + np.prod(weight[1])].reshape(weight[1]),
                 individual[bias[0]:bias[0] + np.prod(bias[1])].reshape(bias[1])])

        screen = pygame.display.set_mode((1280, 720))
        game = GAGame(screen, 1280, 720)
        fitness, avg_vel = game.run_ga(self.model)
        self.generative_ptsY.append(fitness)
        print("ind %i gen %i distance: %.2f" % (
            self.individual_idx, self.generation_idx, fitness))
        checkpoint_freq = 2
        if (self.generation_idx % checkpoint_freq == 0) and (self.individual_idx == population_size):
            NeuroTrainer.save_population_data("./np_population/", self.generation_idx)
        if self.individual_idx < population_size:
            self.generative_ptsX.append(self.generation_idx)
            self.individual_idx += 1
        elif self.individual_idx:
            self.generation_idx += 1
            self.generative_ptsX.append(self.generation_idx)
            self.individual_idx = 1
        # write_data("./fitness_vel_gen.csv", fitness, avg_vel, self.generation_idx)
        return fitness,

    def init_shapes(self):
        layer_weights = []
        layer_shapes = []
        # get layer weights
        for layer_name in self.valid_layer_names:
            layer_weights.append(self.model.get_layer(layer_name).get_weights())

        # break up the weights and biases
        # layer_weights = np.concatenate(layer_weights) ???
        layer_wb = []
        for w in layer_weights:
            layer_wb.append(w[0])
            layer_wb.append(w[1])

        # set starting index and shape of weight/bias
        for layer in layer_wb:
            layer_shapes.append(
                [0 if layer_shapes.__len__() == 0 else layer_shapes[-1][0] + np.prod(
                    layer_shapes[-1][1]), layer.shape])

        layer_weights = np.asarray(layer_wb)
        # flatten all the vectors
        layer_weights = [layer_weight.flatten() for layer_weight in layer_weights]

        # make one vector of all weights and biases
        layer_weights = np.concatenate(layer_weights)
        return layer_weights, layer_shapes

    def initInd(self):
        # init individual with w
        ind = self.layer_weights.tolist()
        return ind

    def load_model(self, model_name):
        json_file = open('./models/' + model_name + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights("./models/" + model_name + ".h5")
        print("Loaded model from disk")


if __name__ == "__main__":
    nr_population = 20
    nr_generations = 50
    agent = KinematicGA(31, 8)

    train_ga = True

    if train_ga is True:
        neuro_trainer = NeuroTrainer(nr_population, nr_generations, agent.initInd)
        neuro_trainer.train(agent.neuro_eval)
    else:
        agent.load_model("model_acclr_elite")
        screen = pygame.display.set_mode((1280, 720))
        game = GAGame(screen, 1280, 720)
        game.run_ga(agent.model)
