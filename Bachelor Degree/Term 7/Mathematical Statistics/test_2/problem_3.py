# First, defining the data points {X, Y}
X = [5.4, 4.6, 6.2, 6.8, 7.1, 7.8, 8.5, 9.1, 10.5, 10.9]
Y = [1.8, 2.1, 2.8, 3.0, 3.2, 3.8, 3.9, 4.2, 4.5, 4.8]

# Next, finding sums of x^2, xy, x, y
sum_xx = sum([x**2 for x in X])
sum_xy = sum([x*y for x, y in zip(X, Y)])
sum_x = sum(X)
sum_y = sum(Y)

# Solve linear equation for a and b
n = len(X)
a = (n*sum_xy - sum_x*sum_y) / (n*sum_xx - sum_x**2)
b = (sum_y - a*sum_x) / n

# Print the values of a and b
print(f"a = {a}, b = {b}")

# Calculate the predicted values for Y
Y_pred = [a*x + b for x in X]
print(f"Predicted values for Y: {Y_pred}")

# Now, calculating the Fischer statistic
# Calculating the numerator
numerator = sum([(y_pred-sum_y/n)**2 for y_pred in Y_pred])
# Calculating the denominator
denominator = sum([(y-y_pred)**2 for y, y_pred in zip(Y, Y_pred)]) / (n-2)
# Finally, calculate the Fischer statistic
F = numerator / denominator
print(f"Fischer statistic: {F}")

# Plot the data points and the regression line
import matplotlib.pyplot as plt
plt.scatter(X, Y, color='red')

# Plot the dashed regression line
plt.plot(X, Y_pred, color='blue', linestyle='dashed')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Regression line')
plt.grid()

# Save the plot
plt.savefig('regression_line.pdf')
