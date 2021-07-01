import random


def initial_sample_generating(size):  # function to create random sample, size = number_of_queens
    return [random.randint(1, number_of_queens) for _ in range(number_of_queens)]  # returning sample, random value of location for each queen


def sample_input(size): # function to take user input for initial sample
    x = [int(i) for i in input().split()] # taking input from user for sample array
    return x


def fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2

    n = len(chromosome)
    left_diagonal = [0] * 2 * n
    right_diagonal = [0] * 2 * n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter / (n - abs(i - n + 1))

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))  # 28-(2+3)=23


def selection(chromosome, fitness):
    return fitness(chromosome) / maxFitness


def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def crossover(x, y):  # doing cross_over between two sample population
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def mutation(x):  # randomly changing the value of a random index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def population_generating(population, fitness):
    mutation_probability = 0.03
    new_population = []
    probabilities = [selection(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)  # best chromosome 1
        y = random_pick(population, probabilities)  # best chromosome 2
        new_samples = crossover(x, y)  # creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            new_samples = mutation(new_samples)
        print_sequence(new_samples)
        new_population.append(new_samples)
        if fitness(new_samples) == maxFitness: break
    return new_population


def print_sequence(chrom):
    print("Sample = {},   Fitness = {}"
          .format(str(chrom), fitness(chrom)))


if __name__ == "__main__":
    number_of_queens = int(input("Enter Number of Queens: "))  # say N = 8
    maxFitness = (number_of_queens * (number_of_queens - 1)) / 2  # 8*7/2 = 28

    option = int(input('1. random sequence sample\n2. given sequence sample\n'))
    if option == 1:
        population = [initial_sample_generating(number_of_queens) for _ in range(10)]
        print('Initial set of population - ')
        print(population)
    else:
        print('Sample input -')
        population = [sample_input(number_of_queens) for _ in range(10)]
        print('Initial set of population - ')
        print(population)

    generation = 1

    while not maxFitness in [fitness(sequence) for sequence in population]:
        print("Samples of generation {} ".format(generation))
        population = population_generating(population, fitness)
        print("")
        print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
    chrom_out = []
    print("Solved in Generation {}!".format(generation - 1))
    for chrom in population:
        if fitness(chrom) == maxFitness:
            print("")
            print("One of the solutions: ")
            chrom_out = chrom
            print_sequence(chrom)

    board = []
    for x in range(number_of_queens):
        board.append(["x"] * number_of_queens)
    for i in range(number_of_queens):
        board[number_of_queens - chrom_out[i]][i] = "Q"


    def output(board):
        for row in board:
            print(" ".join(row))


    output(board)