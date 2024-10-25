import numpy as np
import pandas as pd
import yfinance as yf
from deap import base, creator, tools, algorithms
import random
import matplotlib.pyplot as plt

def moving_average_crossover_strategy(data, short_window, long_window):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    # Create short and long moving averages
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Create signals
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    # Generate trading orders
    signals['positions'] = signals['signal'].diff()

    return signals

def fitness(individual, data):
    short_window, long_window = individual
    signals = moving_average_crossover_strategy(data, int(short_window), int(long_window))

    initial_capital = 100000.0
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions['Stock'] = 1000 * signals['signal']  # 1000 shares

    portfolio = positions.multiply(data['Close'], axis=0)
    pos_diff = positions.diff()

    portfolio['holdings'] = (positions.multiply(data['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Close'], axis=0)).sum(axis=1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()

    return portfolio['total'][-1],

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 10, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutUniformInt, low=10, up=100, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Pass data to the fitness function using lambda
toolbox.register("evaluate", lambda individual: fitness(individual, data))

def run_ga(data, ngen=10, pop_size=50, cxpb=0.5, mutpb=0.2):
    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, 
                                   stats=stats, halloffame=hof, verbose=True)
    
    return pop, log, hof

data = yf.download("AAPL", start="2020-01-01", end="2022-01-01")

pop, log, hof = run_ga(data)

# best_individual = hof[0]
# print(f'Best individual: {best_individual}, Fitness: {best_individual.fitness.values[0]}')

# signals = moving_average_crossover_strategy(data, int(best_individual[0]), int(best_individual[1]))

# plt.figure(figsize=(10, 5))
# plt.plot(data['Close'], label='Price')
# plt.plot(signals['short_mavg'], label='Short MAvg')
# plt.plot(signals['long_mavg'], label='Long MAvg')
# plt.plot(signals.loc[signals.positions == 1.0].index, 
#          signals.short_mavg[signals.positions == 1.0], 
#          '^', markersize=10, color='m', lw=0, label='Buy')
# plt.plot(signals.loc[signals.positions == -1.0].index, 
#          signals.short_mavg[signals.positions == -1.0], 
#          'v', markersize=10, color='k', lw=0, label='Sell')
# plt.legend()
# plt.show()

# Display the best individual and its fitness value
best_individual = hof[0]
print(f'Best individual: {best_individual}, Fitness: {best_individual.fitness.values[0]}')

# Generate signals using the best parameters
signals = moving_average_crossover_strategy(data, int(best_individual[0]), int(best_individual[1]))

# Plot the stock's closing price, short and long moving averages, and buy/sell signals
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Price')
plt.plot(signals['short_mavg'], label='Short MAvg')
plt.plot(signals['long_mavg'], label='Long MAvg')
plt.plot(signals.loc[signals.positions == 1.0].index, 
         signals.short_mavg[signals.positions == 1.0], 
         '^', markersize=10, color='m', lw=0, label='Buy')
plt.plot(signals.loc[signals.positions == -1.0].index, 
         signals.short_mavg[signals.positions == -1.0], 
         'v', markersize=10, color='k', lw=0, label='Sell')
plt.legend()
plt.show()

