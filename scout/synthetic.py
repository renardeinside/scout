"""Synthetic image / data generation

This module provides functions for generating synthetic images and point clouds.
The synthetic data is useful for initial testing of image processing code.

"""
import numpy as np
from skimage.filters import gaussian
from tqdm import tqdm
from scout.utils import insert_box


def random_points(n, shape):
    """Generate `n` d-dimensional points randomly distributed from the origin to `shape`

    Parameters
    ----------
    n : int
        number of points to generate
    shape : array-like
        indices of the upper limit for each dimension

    Returns
    -------
    points : tuple of index arrays
        d arrays containing n randomly generated indices

    """
    n = int(n)
    if n < 0:
        raise ValueError("n must be a positive integer")
    else:
        try:
            d = len(shape)
            if d == 0:
                raise ValueError("shape must contain at least one integer value")
        except TypeError:
            raise ValueError("shape must be array-like")
    idx = np.random.choice(np.prod(shape), size=n, replace=False)
    return np.unravel_index(idx, shape)


def points_to_binary(points, shape, dtype="uint8", cval=255, size=1):
    """Convert `points` to a binary image of size `shape` with hot pixels at each point

    Parameters
    ----------
    points : tuple of arrays
        indices of foreground pixels
    shape : array-like
        output image shape
    dtype : str, optional
        data type of the output image
    cval : int or float, optional
        intensity value to place at all points
    size : int, optional
        width of each point in the binary image

    Returns
    -------
    binary : array
        resulting binary image

    """
    try:
        if len(points) != len(shape):
            raise ValueError(
                "points and shape need to contain the same number of dimensions"
            )
        else:
            d = len(points)
            if d == 0:
                raise ValueError("points and shape need to be at least 1-dimensional")
    except TypeError:
        raise ValueError("points and shape need to be array-like")
    binary = np.zeros(shape, dtype=dtype)
    if size == 1:
        binary[points] = cval
    else:
        radius = size // 2
        for coords in tqdm(zip(*points), total=len(points[0])):
            start = np.asarray(coords, np.int) - radius
            stop = np.asarray(coords, np.int) + radius
            binary = insert_box(binary, start, stop, cval)
    return binary


def binary_to_blobs(binary, sigma=1, peakval=1, dtype="float32"):
    """Blur a binary image of one-hot points into blobs

    Parameters
    ----------
    binary : array
        input image with one-hot point encoding
    sigma : float
        gaussian blurring amount
    peakval : int or float
        intensity value for the blob peaks
    dtype : str
        data type for the output array

    Returns
    -------
    blobs : array
        output image with gaussian blobs

    """
    smooth = gaussian(binary, sigma=sigma, preserve_range=True)
    blobs = peakval * (smooth / smooth.max())
    return blobs.astype(dtype)


def generate_blobs(n, shape, sigma=1, peakval=1, dtype="float32"):
    """Generate an image with uniformly-shaped, randomly-placed gaussian blobs

    The blob image is generated by gaussian blurring an intermediate image of random points.

    Parameters
    ----------
    n : int
        number of blobs
    shape : tuple
        shape of the output image
    sigma : int or tuple, optional
        gaussian filter width
    peakval : int or float
        intensity value at blob centers
    dtype : str


    Returns
    -------
    blobs : array
        an array containing `n` blobs of size `sigma`

    """
    n = int(n)
    if n <= 0:
        raise ValueError("n must be at least one")
    points = random_points(n, shape)
    binary = points_to_binary(points, shape)
    return binary_to_blobs(binary, sigma, peakval, dtype)


def remove_random_points(points, amount):
    """Remove a random subset from a set of points

    Parameters
    ----------
    points : tuple of arrays
        input point cloud to remove points from
    amount : int or float
        number or fraction of points to remove

    Returns
    -------
    sample : tuple of arrays
        output point cloud with a random subset removed

    """
    try:
        n = len(points[0])
    except TypeError:
        raise ValueError("points needs to contain array-like objects")
    except IndexError:
        raise ValueError("points needs to have at least one dimension")

    if isinstance(amount, float) and 0 <= amount <= 1:
        nb_removed = int(amount * n)
    elif isinstance(amount, int) and amount >= 0:
        nb_removed = amount
    else:
        raise ValueError(
            "amount must be a non-negative integer or a float between 0 and 1"
        )

    idx = np.arange(n)
    np.random.shuffle(idx)
    keep_idx = idx[nb_removed:]
    sample = tuple(map(lambda d, i: d[i], points, len(points) * [keep_idx]))
    return sample


def generate_random_noise(shape, clim):
    """Generate an image of random noise scaled within `clim` bounds

    Parameters
    ----------
    shape : tuple
        shape of the noise image
    clim : array-like
        (2,) array of with the minimum and maximum values possible in the random noise

    Returns
    -------
    noise : ndarray
        output noise array

    """
    if len(clim) != 2:
        raise ValueError("clim must contain a minimum and maximum value")
    return np.random.rand(*shape) * (clim[1] - clim[0]) + clim[0]
