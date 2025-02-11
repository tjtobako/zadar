import numpy as np
from scipy.stats import linregress

# Sample data points
x = np.array([6,6,8,8,8,9])  # Replace x1, x2, ..., xn with your x values
y = np.array([0.6, 1.1, 2.4,2.5,3,3.5])  # Replace y1, y2, ..., yn with your y values

# Calculate averages
mean_x = np.mean(x)
mean_y = np.mean(y)
print(mean_x)
# Calculate variances
variance_x = np.var(x, ddof=0)  # Use ddof=1 for sample variance
print(variance_x)
variance_y = np.var(y, ddof=0)

# Calculate covariance
covariance_xy = np.cov(x, y, ddof=0)[0, 1]  # Use ddof=1 for sample covariance

# Calculate correlation coefficient
correlation_coefficient = np.corrcoef(x, y)[0, 1]

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)
# Output results
print(f"Averages: Mean_x = {mean_x}, Mean_y = {mean_y}")
print(f"Variances: Variance_x = {variance_x}, Variance_y = {variance_y}")
print(f"Covariance: Cov(x, y) = {covariance_xy}")
print(f"Correlation Coefficient: Corr(x, y) = {correlation_coefficient}")
print(f"Regression Coefficient: Cov(x,y)/std(x)std(y) = {slope}")
print(f"Linear Regression Line: y = {slope}x + {intercept}")