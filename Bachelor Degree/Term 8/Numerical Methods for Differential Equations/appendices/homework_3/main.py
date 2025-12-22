from solver import solve_pde

import numpy as np

# For visualization
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # First, solve the equation
    a, b = 2.0, 1.0
    n = 30
    f_func = lambda x, y: np.sin(x)
    g_func = lambda x, y: 20 * np.round(x+y)**2
    
    u_solution = solve_pde(n, a, b, f_func, g_func)
    u_solution_2n = solve_pde(2*n, a, b, f_func, g_func)
    
    # Validate that the difference between the two solutions is small
    diff = np.mean(np.abs(u_solution - u_solution_2n[::2, ::2]))
    print(f"Max difference between n={n} and n={2*n} solutions: {diff:.2e}")

    x = np.linspace(0, a, n + 1)
    y = np.linspace(0, b, n + 1)
    X, Y = np.meshgrid(x, y, indexing="ij")
    
    # Contour plot with colorbar (already done)
    plt.figure(figsize=(6, 5))
    plt.contourf(X, Y, u_solution, levels=50, cmap="viridis")
    plt.colorbar(label="u(x,y)")
    plt.title("Solution to the PDE")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig("contour_plot.pdf", dpi=300)
    plt.show()
    
    # 3D surface plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, u_solution, cmap='viridis', edgecolor='none')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="u(x,y)")
    ax.set_title("Surface Plot of the Solution")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("u(x,y)")
    plt.tight_layout()
    plt.savefig("surface_plot.pdf", dpi=300)
    plt.show()