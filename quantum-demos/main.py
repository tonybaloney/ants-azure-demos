#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import time
from typing import List, Sequence

# Instantiate Workspace object which allows you to connect to the Workspace you've previously deployed in Azure.
# Be sure to fill in the settings below which can be retrieved by running 'az quantum workspace show' in the terminal.
from azure.quantum import Workspace
from azure.quantum.optimization import (ParallelTempering, Problem,
                                        ProblemType, Term)

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn, BarColumn
from rich.console import Console
from rich.table import Table

import numpy as np

NUM_CONTAINERS = 100
CONTAINER_MIN_WEIGHT = 1
CONTAINER_MAX_WEIGHT = 50

# Copy the settings for your workspace below
workspace = Workspace(
    resource_id = os.getenv('AZURE_RESOURCE_ID'), # add the Resource ID of your Azure Quantum workspace
    location = os.getenv('AZURE_LOCATION', 'westus')     # add the location of your Azure Quantum workspace (e.g. "westus")
)


def create_problem_for_container_weights(container_weights: Sequence[int]) -> Problem:
    terms: List[Term] = []

    # Expand the squared summation
    for i in range(len(container_weights)):
        for j in range(len(container_weights)):
            if i == j:
                # Skip the terms where i == j as they form constant terms in an Ising problem and can be disregarded:
                # w_i∗w_j∗x_i∗x_j = w_i​*w_j∗(x_i)^2 = w_i∗w_j​​
                # for x_i = x_j, x_i ∈ {1, -1}
                continue

            terms.append(
                Term(
                    c = container_weights[i] * container_weights[j],
                    indices = [i, j]
                )
            )

    # Return an Ising-type problem
    return Problem(name="Ship Sample Problem", problem_type=ProblemType.ising, terms=terms)

# This array contains a list of the weights of the containers
rng = np.random.default_rng()
container_weights = rng.integers(low=CONTAINER_MIN_WEIGHT, high=CONTAINER_MAX_WEIGHT, size=NUM_CONTAINERS)

# Create a problem for the list of containers:
problem1 = create_problem_for_container_weights(container_weights)


# Instantiate a solver to solve the problem.
parallel_solver = ParallelTempering(workspace, timeout=100)

# Print out a summary of the results:
def print_result_summary(result, console):
    table = Table(title="Container Allocations")

    table.add_column("Container", justify="right", style="cyan", no_wrap=True)
    table.add_column("Weight", style="magenta")
    table.add_column("Ship", justify="right", style="green")

    # Print a summary of the result
    ship_a_weight = 0
    ship_b_weight = 0
    for container in result['configuration']:
        container_assignment = result['configuration'][container]
        container_weight = container_weights[int(container)]
        ship = ''
        if container_assignment == 1:
            ship = 'A'
            ship_a_weight += container_weight
        else:
            ship = 'B'
            ship_b_weight += container_weight

        table.add_row(container, str(container_weight), ship)

    console.print(table)
    print(f'\nTotal weights: \n\tShip A: {ship_a_weight} tonnes \n\tShip B: {ship_b_weight} tonnes\n')


# We can reduce the number of terms by removing duplicates (see associated Jupyter notebook for details)
# In code, this means a small modification to the create_problem_for_container_weights function:
def create_simplified_problem_for_container_weights(container_weights: List[int]) -> Problem:
    terms: List[Term] = []

    # Expand the squared summation
    for i in range(len(container_weights)-1):
        for j in range(i+1, len(container_weights)):
            terms.append(
                Term(
                    c = container_weights[i] * container_weights[j],
                    indices = [i, j]
                )
            )

    # Return an Ising-type problem
    return Problem(name="Ship Sample Problem (Simplified)", problem_type=ProblemType.ising, terms=terms)

# Check that this creates a smaller problem
# Create the simplified problem
problem2 = create_simplified_problem_for_container_weights(container_weights)

job1 = parallel_solver.submit(problem1)
job2 = parallel_solver.submit(problem2)

console = Console()

with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:

        task1 = progress.add_task(f"[yellow]Processing {job1.details.name}", total=1000, start=True)
        task2 = progress.add_task(f"[yellow]Processing {job2.details.name}", total=1000, start=True)

        while not job1.has_completed() and not job2.has_completed():
            time.sleep(0.01)
            job1.refresh()
            job2.refresh()

print_result_summary(job1.get_results(), console)
print_result_summary(job2.get_results(), console)
