import scipy.optimize

# Objective Function: 50x₁ + 80x₂
# Constraint 1: 5x₁ + 2x₂ ≤ 20
# Constraint 2: -10x₁ + -12x₂ ≤ -90

result = scipy.optimize.linprog(
    [50, 80],  # Cost function: 50x₁ + 80x₂
    A_ub=[[5, 2], [-10, -12]],  # Coefficients for inequalities
    b_ub=[20, -90],  # Constraints for inequalities: 20 and -90
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} hours")
    print(f"X2: {round(result.x[1], 2)} hours")
else:
    print("No solution")
