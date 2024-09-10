

import numpy as np
import matplotlib.pyplot as plt


def linearPointGenerator(lower_bound, upper_bound, n_points):
    # Generate some random points with smooth fluctuations
# Parameters
    x = np.linspace(0, n_points, n_points + 1)

    y = np.linspace(lower_bound, upper_bound, n_points + 1)


    return (x, y)

if __name__ == '__main__':
    
    (x, y) = linearPointGenerator(60, 100, 500)
    print(x)
    print(y)

    plt.scatter(x, y)
    plt.plot(x, y, linestyle='dotted', color='gray')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Random Smooth Fluctuating Points')
    plt.show()
