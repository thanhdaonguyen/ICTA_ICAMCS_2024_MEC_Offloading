import numpy as np
import matplotlib.pyplot as plt


def flucPointGenerator(lower_bound, upper_bound, n_points):
    # Generate some random points with smooth fluctuations
# Parameters
    x = np.linspace(0, n_points, n_points + 1)

    # Generate random y-values
    y_random = np.random.randn(n_points + 1)

    # Apply a cumulative sum to make the fluctuations smoother
    y_cumsum = np.cumsum(y_random)

    # Normalize the cumulative sum to the desired range
    y = (y_cumsum - np.min(y_cumsum)) / (np.max(y_cumsum) - np.min(y_cumsum))

    y = lower_bound + (upper_bound - lower_bound) * y

    # Optionally, add some noise to make it more random
    # y += 3 + 0.01 * np.random.randn(n_points)

    # Plot the points
    x = np.round(x).astype(int)
    y = np.round(y).astype(int)

    return (x, y)

if __name__ == '__main__':
    
    (x, y) = flucPointGenerator(60, 100, 500)
    print(x)
    print(y)

    plt.scatter(x, y)
    plt.plot(x, y, linestyle='dotted', color='gray')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Random Smooth Fluctuating Points')
    plt.show()
