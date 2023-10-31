## Lab :two:

This folder contains materials and files for lab 2. Task is simple:

1. Build a cubic spline given interval and function $f$ defined on this interval.
2. At specified points, find values of spline and a given function. Calculate the error (absolute difference between value of spline and a function).

### Prerequisites

Make sure you have the following packages installed:
- `rich` (you can install it via `pip install rich`)
- `matplotlib`
- `numpy`
- `abc`
- `typing`

And Python as well for sure :wink:.

### Running

Simply run
```bash
python3 cli.py
```

You will see 2 tables as requested in the task. Also, we depict the comparison between the spline and the function on the interval.

To experiment with different functions and $\alpha$ values, navigate to the [`cli.py`](cli.py) file and change the following fields:
```python
# Defining the task parameters
interval = (0.0, 1.0)
segments_number = 20
alpha = 0.2
fn = lambda x: x**3 + cos(x) + exp(x / 10.0) * sin(x)
```
