
---

# Moving Average Crossover Strategy Optimization with Genetic Algorithm

This project uses a genetic algorithm to optimize a moving average crossover strategy for stock trading, helping identify the optimal short and long moving averages for maximizing returns. By using historical data from Yahoo Finance, this strategy tests and evaluates potential buy/sell signals based on stock price trends.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributions](#contributions)
- [License](#license)

## Overview

The Moving Average Crossover Strategy is a popular approach in algorithmic trading that generates buy/sell signals when a stock's short-term moving average crosses above or below a long-term moving average. This repository includes:

- A **Genetic Algorithm (GA)** implemented using DEAP to find the optimal short and long moving average window lengths.
- Data fetching via **yFinance** to retrieve stock data.
- **Performance visualization** using Matplotlib to show the optimized buy and sell signals.

The optimization process maximizes returns by evaluating crossover parameters that yield the highest portfolio value over a set period.

## Requirements

- Python 3.7+
- `numpy`
- `pandas`
- `matplotlib`
- `deap`
- `yfinance`

## Installation

To set up this project locally, clone the repository and install the required libraries:

```bash
git clone https://github.com/your-username/Moving-Average-Crossover-Optimization.git
cd Moving-Average-Crossover-Optimization
pip install -r requirements.txt
```

### Required Libraries
Install the necessary libraries with:
```bash
pip install numpy pandas matplotlib deap yfinance
```

## Usage

1. Download historical data for a selected stock and optimize the strategy.

2. Run the script to execute the genetic algorithm:

    ```python
    python main.py
    ```

3. After the optimization completes, the script will print the best short and long window lengths found and display a plot of the stock's price, moving averages, and buy/sell signals.

### Example Output

The script will display:
- **Best Individual**: Optimized short and long window lengths.
- **Fitness**: Final portfolio value based on the crossover strategy.

A **plot** will show the stock's price, moving averages, and buy/sell points for visualization.

## Project Structure

```plaintext
.
├── main.py                 # Main script with genetic algorithm and crossover strategy
├── README.md               # Project readme file
└── requirements.txt        # Dependencies
```


## License

This project is open-source and available under the MIT License. See the `LICENSE` file for details.

---

