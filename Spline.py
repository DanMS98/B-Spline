import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


def create_figure(t, c, k=3, imagePath='./static/uploads/kn2c.jpg', outputName='Spline.jpg'):

    I = plt.imread(imagePath)
    ctr = c
    tck = [t, [ctr[:, 0], ctr[:, 1]], k]
    u3 = np.linspace(0, 1, (max(len(c)*2, 70)), endpoint=True)
    out = interpolate.splev(u3, tck)
    plt.imshow(I)
    plt.plot(ctr[:, 0], ctr[:, 1], 'k--', label='Control polygon', marker='o', markerfacecolor='red')
    plt.plot(out[0], out[1], 'b', linewidth=2.0, label='B-spline curve')
    plt.title('B-spline curve')
    figurePath = f'./static/images/{outputName}'
    plt.savefig(figurePath)
    plt.close()
    return figurePath


if __name__ == "__main__":
    create_figure()
