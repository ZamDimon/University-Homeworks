## :one: Lab 1

This folder contains materials and files for lab 1. Task is simple:

1. Build Lagrange, Newton forward and backwards polynomials given interval and function $f$ defined on this interval.
2. At specified points, find values of polynomials and a given function. Calculate the error (absolute difference between value of polynomial and a function).

### Prerequisites

Make sure you have the following packages installed:
- `rich` (you can install it via `pip install rich`)
- `abc`
- `typing`

And Python as well for sure :wink:

### Running

Simply run
```bash
python3 cli.py
```

You will see 6 tables as requested in the task.

To experiment with different functions and $\alpha$ values, navigate to the [`cli.py`](cli.py) file and change the following fields:
```python
# Defining the task parameters
interval = (-2.0, 2.0) # Change the interval here
segments_number = 20 # Change the number of segments here
alpha = 0.0 # Change the alpha here
fn = lambda x: exp(x / 10.0) * sin(x) + x**3 + cos(x) # Change the function here
```
