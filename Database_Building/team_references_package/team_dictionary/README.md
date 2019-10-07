# seanblack_udacity_distributions_example

Summary

# Files
Binomialdistribution.py - Class that creates a binomial distribution of a binary dataset
Gaussiandistribution.py - Class that creates a gaussian distribution of dataset
Generaldistribution.py - Parent class that calculates distrubtion of a dataset

# Gaussian init arguments
1) mean
2) stdev

# Binomal init arguments
1) probability (float value from 0 to 1)
2) data size or n (integer)

# installation

pip install --upgrade seanblack_udacity_distributions_example

# Gaussian usage

- initialize object with initial params

	>>> from distributions import Gaussian
	>>> gaussian = Gaussian(50,4)
    
- read in a dataset

	>>> gaussian.read_data_file('file.txt')
    
- display new mean/stdev for Gaussian object

	>>> print(gaussian)
    
# Binomial usage

- initialize object with initial params

	>>> from distributions import Binomial
	>>> binomial = Binomial(0.5,100)
    
- read in a dataset

	>>> binomial.read_data_file('file.txt')
    
- calculate and display new binomial stats

	>>> binomial.replace_stats_with_data()
    >>> print(binomial)
