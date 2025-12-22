from typing import Callable
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from solver import solve_pde

# --- Method of Manufactured Solutions (MMS) Setup ---

# Parameters for the exact solution functions
# X_p(x, param_a)
def exact_sol_X(x_val: float, param_a: float) -> float:
    return np.exp(param_a) * (x_val - param_a) - (param_a + 1) * (np.exp(x_val) - np.exp(param_a))

# Y_p(y, param_b)
def exact_sol_Y(y_val: float, param_b: float) -> float:
    return np.exp(param_b) * (y_val - param_b) - (param_b + 1) * (np.exp(y_val) - np.exp(param_b))

# X_p''(x, param_a)
def exact_sol_X_dd(x_val: float, param_a: float) -> float:
    return -(param_a + 1) * np.exp(x_val)

# Y_p''(y, param_b)
def exact_sol_Y_dd(y_val: float, param_b: float) -> float:
    return -(param_b + 1) * np.exp(y_val)

# u_exact(x, y) = X_p(x,a) * Y_p(y,b)
def u_exact_func(x_val: float, y_val: float, domain_a: float, domain_b: float) -> float:
    return exact_sol_X(x_val, domain_a) * exact_sol_Y(y_val, domain_b)

# Original f(x,y) function
def f_original_func(x_val: float, y_val: float) -> float:
    return np.sin(x_val)

# Manufactured g_mms(x,y) function
def g_mms_func(x_val: float, y_val: float, domain_a: float, domain_b: float) -> float:
    X_val = exact_sol_X(x_val, domain_a)
    Y_val = exact_sol_Y(y_val, domain_b)
    X_dd_val = exact_sol_X_dd(x_val, domain_a)
    Y_dd_val = exact_sol_Y_dd(y_val, domain_b)

    laplacian_u_exact = X_dd_val * Y_val + X_val * Y_dd_val
    f_u_exact = f_original_func(x_val, y_val) * X_val * Y_val
    
    return laplacian_u_exact + f_u_exact

if __name__ == "__main__":
    # Domain parameters
    a_domain, b_domain = 2.0, 1.0
    # Grid parameter
    n_grid = 20 # You can change this to see convergence, e.g., 10, 20, 40

    print(f"Solving PDE with n={n_grid} using manufactured solution...")
    # Use a lambda to pass domain_a, domain_b to g_mms_func
    g_for_solver = lambda x, y: g_mms_func(x, y, a_domain, b_domain)
    u_numerical = solve_pde(n_grid, a_domain, b_domain, f_original_func, g_for_solver)
    print("Numerical solution obtained.")

    # Create grid for evaluating exact solution and plotting
    x_pts = np.linspace(0, a_domain, n_grid + 1)
    y_pts = np.linspace(0, b_domain, n_grid + 1)
    X_grid, Y_grid = np.meshgrid(x_pts, y_pts, indexing="ij")

    # Evaluate exact solution on the grid
    print("Evaluating exact solution on the grid...")
    u_exact_on_grid = np.zeros_like(X_grid)
    for i in range(n_grid + 1):
        for j in range(n_grid + 1):
            u_exact_on_grid[i, j] = u_exact_func(X_grid[i, j], Y_grid[i, j], a_domain, b_domain)
    print("Exact solution evaluated.")

    # Calculate the error
    error = u_numerical - u_exact_on_grid
    l2_error_norm = np.sqrt(np.sum(error**2) / np.sum(u_exact_on_grid**2))
    max_abs_error = np.max(np.abs(error))
    print(f"L2 Relative Error: {l2_error_norm:.4e}")
    print(f"Max Absolute Error: {max_abs_error:.4e}")


    # --- Plotting ---
    # Determine common color scale based on numerical and exact solutions
    vmin_sol = min(u_numerical.min(), u_exact_on_grid.min())
    vmax_sol = max(u_numerical.max(), u_exact_on_grid.max())

    fig_compare, axes_compare = plt.subplots(1, 2, figsize=(14, 6))
    fig_compare.suptitle(f"Comparison with Manufactured Solution (n={n_grid})", fontsize=16)

    # Numerical Solution Plot
    contour_num = axes_compare[0].contourf(X_grid, Y_grid, u_numerical, levels=50, cmap="viridis", vmin=vmin_sol, vmax=vmax_sol)
    fig_compare.colorbar(contour_num, ax=axes_compare[0], label="u(x,y)")
    axes_compare[0].set_title("Numerical Solution (Your Code)")
    axes_compare[0].set_xlabel("x")
    axes_compare[0].set_ylabel("y")
    axes_compare[0].set_aspect('equal', adjustable='box')

    # Exact Solution Plot
    contour_exact = axes_compare[1].contourf(X_grid, Y_grid, u_exact_on_grid, levels=50, cmap="viridis", vmin=vmin_sol, vmax=vmax_sol)
    fig_compare.colorbar(contour_exact, ax=axes_compare[1], label="u(x,y)")
    axes_compare[1].set_title("Exact Manufactured Solution")
    axes_compare[1].set_xlabel("x")
    axes_compare[1].set_ylabel("y")
    axes_compare[1].set_aspect('equal', adjustable='box')
    
    fig_compare.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"mms_comparison_n{n_grid}.pdf", dpi=300)
    plt.show()

    # Plotting the error
    plt.figure(figsize=(7, 6))
    contour_error = plt.contourf(X_grid, Y_grid, error, levels=50, cmap="coolwarm")
    plt.colorbar(contour_error, label="Error (Numerical - Exact)")
    plt.title(f"Error Distribution (n={n_grid})\nMax Abs Error: {max_abs_error:.2e}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.savefig(f"mms_error_n{n_grid}.pdf", dpi=300)
    plt.show()