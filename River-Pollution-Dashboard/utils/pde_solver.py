import numpy as np


def simulate_pollution(
    river_length,
    grid_points,
    simulation_time,
    velocity,
    diffusion,
    initial_pollution,
    source_location
):

    # Spatial grid
    x = np.linspace(0, river_length, grid_points)
    dx = x[1] - x[0]

    # Time step
    dt = 0.01
    steps = int(simulation_time / dt)

    # Initial concentration
    concentration = np.zeros(grid_points)
    source_index = int(
    (source_location / river_length) * (grid_points - 1)
)

    concentration[source_index] = initial_pollution

    # Store all time steps
    concentration_history = np.zeros((steps, grid_points))

    for step in range(steps):

        new_concentration = concentration.copy()

        for i in range(1, grid_points - 1):

            diffusion_term = (
                diffusion *
                (concentration[i + 1]
                 - 2 * concentration[i]
                 + concentration[i - 1])
                / dx**2
            )

            advection_term = (
                -velocity *
                (concentration[i]
                 - concentration[i - 1])
                / dx
            )

            new_concentration[i] = (
                concentration[i]
                + dt * (diffusion_term + advection_term)
            )

        # Boundary conditions
        new_concentration[source_index] = initial_pollution
        new_concentration[-1] = new_concentration[-2]

        concentration = new_concentration

        concentration_history[step] = concentration

    return x, concentration, concentration_history