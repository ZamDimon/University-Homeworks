## Lab :three:

This folder contains materials and files for Lab 3. 

### Task

Given a dataset $\mathcal{D}$ consisting of a set of points $(x_i,y_i) \in \mathbb{R}^2$ we want to find a polynomial using the least squares method. Task is to have a polynomial of degree 3, but the code allows one to use any degree (as long as there is sufficiently enough data).

### Prerequisites

Make sure you have the following packages installed:
- `rich` (you can install it via `pip install rich`)
- `matplotlib`
- `numpy`
- `abc`
- `typing`

And Python as well for sure :wink:.

In case you don't have some of the packages, you can install them via 
```bash
pip install <package_name>
```

### Running

Simply run
```bash
python3 main.py
```

You will see a table requested in a task. Also, we display the plots containing the data and the polynomial we found. We also save the plots in the [`images`](images) folder.
