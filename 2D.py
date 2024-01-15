import random
import numpy as np
import tkinter as tk
from tkinter import messagebox
# Genetic Algorithm Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.7
GENERATIONS = 1000

# Problem Parameters
def degerler():
    try:
        width = int(genislik.get())
        height = int(yukseklik.get())
        if width > 20 or height > 20:
            messagebox.showerror("Hata", "Giriş değerleri maksimum 20 olabilir.")
        else:
            rectangles.append((width, height))
            listbox.insert(tk.END, f"({width}, {height})")

    except ValueError:
        messagebox.showerror("Hata", "Geçersiz giriş. Lütfen geçerli bir sayı girin.")

def done():
    window.quit()

rectangles = []
window = tk.Tk()
window.geometry("300x400")

genislik = tk.Entry(window)
genislik.pack()
yukseklik = tk.Entry(window)
yukseklik.pack()

eklebtn = tk.Button(window, text="Dikdörtgen Ekle", command=degerler)
eklebtn.pack()

donebtn = tk.Button(window, text="Bitti", command=done)
donebtn.pack()

listbox = tk.Listbox(window,height=20,width=20)
listbox.pack()

window.mainloop()

container = (20, 20)

# Genetic Algorithm Functions
def generate_individual():
    return random.sample(rectangles, len(rectangles))

def fitness(individual):
    # Try to pack the rectangles
    result = paketleme(individual, container)
    # Fitness is the number of rectangles successfully packed
    return len(result)

def mutate(individual):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]

def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        i = random.randint(0, len(parent1) - 1)
        child1 = parent1[:i] + [item for item in parent2 if item not in parent1[:i]]
        child2 = parent2[:i] + [item for item in parent1 if item not in parent2[:i]]
        return child1, child2
    else:
        return parent1, parent2

def paketleme(rectangles, container):
    rectangles.sort(key=lambda r: r[0]*r[1], reverse=True)
    spaces = [[0, 0, container[0], container[1]]]
    result = []
    for rectangle in rectangles:
        for i, space in enumerate(spaces):
            if rectangle[0] <= space[2] and rectangle[1] <= space[3]:
                result.append([space[0], space[1], rectangle[0], rectangle[1]])
                if rectangle[0] < space[2]:
                    spaces.append([space[0] + rectangle[0], space[1], space[2] - rectangle[0], rectangle[1]])
                if rectangle[1] < space[3]:
                    spaces.append([space[0], space[1] + rectangle[1], rectangle[0], space[3] - rectangle[1]])
                del spaces[i]
                break
    return result

def show(result, container):
    window = tk.Tk()
    scale = min(400 / container[0], 400 / container[1])
    canvas = tk.Canvas(window, width=container[0]*scale, height=container[1]*scale)
    canvas.pack()
    for rectangle in result:
        x1, y1, w, h = rectangle
        x2, y2 = x1 + w, y1 + h
        canvas.create_rectangle(x1*scale, y1*scale, x2*scale, y2*scale, fill="red")
    window.mainloop()

# Genetic Algorithm Main Loop
population = [generate_individual() for _ in range(POPULATION_SIZE)]
best_fitness = 0
best_individual = None
best_cozum = None
best_packing = None
for generation in range(GENERATIONS):
    for individual in population:
        fitness_value = fitness(individual)
        if fitness_value > best_fitness:
            best_fitness = fitness_value
            best_individual = individual
            best_cozum = list(individual)
            best_packing = paketleme(individual, container)

    population = sorted(population, key=fitness, reverse=True)
    next_population = population[:2]  # Initialize next_population here

    while len(next_population) < POPULATION_SIZE:
        parent1, parent2 = random.choices(population, weights=[fitness(ind) for ind in population], k=2)
        child1, child2 = crossover(parent1, parent2)
        mutate(child1)
        mutate(child2)
        next_population += [child1, child2]

    population = next_population

# Print best solution
best = max(population, key=fitness)
print("Kullanıcı girdileri ", best_cozum)
print("Kaç kutu yerleştirildi: ", best_fitness)

# Print the packing of the best solution
print("En iyi çözüm kümesi")
for rectangle in best_packing:
    print(rectangle)
# Visualize the packing
show(best_packing, container)
# Print statistics
print("Average fitness:", sum([fitness(ind) for ind in population]) / len(population))
print("Standard sapma:", np.std([fitness(ind) for ind in population]))

