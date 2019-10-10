"""Steps for finding stock safety."""

from csv import reader
from sklearn.cluster import KMeans
import numpy as np
from statistics import pvariance


def safe_shares(filename):
    """Find which shares are safe for investment."""
    x = {}
    companies = {}
    with open(filename, 'r') as csvfile:
        csvFileReader = reader(csvfile)
        next(csvFileReader)  # skipping column names
        # get share values for each company
        for row in csvFileReader:
            # get company name if it is missing
            if row[1] not in companies.keys():
                companies[row[1]] = []
            # add values in that order for each day
            companies[row[1]].append(float(row[3]))  # close
            companies[row[1]].append(float(row[4]))  # low
            companies[row[1]].append(float(row[5]))  # high

        for company in companies.keys():
            # get the population variance of closing prices and an index
            close = []  # close
            high_low_mean = []  # mean value of high and low
            temp = 0.0
            i = 0
            for val in companies[company]:
                if i % 3 == 0:
                    close.append(val)
                elif i % 3 == 1:
                    temp = val
                elif i % 3 == 2:
                    high_low_mean.append((temp + val) / 2)
                i += 1
            # each company's values to be clustered are:
            # poulation variances of: mean value of high and low,
            #  and of closing value
            x[company] = [pvariance(high_low_mean), pvariance(close)]

        # Do k-means clustering ,given the above data points.
        cluster_maker = KMeans(n_clusters=2).fit(
            np.array([[a[0], a[1]] for a in x.values()]))

        # Check centers of each cluster
        x1 = cluster_maker.cluster_centers_[0]
        x2 = cluster_maker.cluster_centers_[1]
        # values in both axes have to be higer or lower, for results to be valid.
        if x1[0] > x2[0] and x1[1] > x2[1]:
            pass
        elif x1[0] < x2[0] and x1[1] < x2[1]:
            x1, x2 = x2, x1
        else:
            print("Warning! Centroids don't indicate a clear distinction!!!")
            print("Data is too small or needs cleaning...")
            return
        print("Centroids for Variance of shares:")
        print("                   High+Low/2      ,      Close")
        print("For unsafe shares:", x1[0], ",", x1[1])
        print("For safe shares:", x2[0], ",", x2[1])
        xvals = [a[0] for a in x.values()]
        yvals = [a[1] for a in x.values()]
        low = [min(xvals), min(yvals)]
        high = [max(xvals), max(yvals)]
        print("Variances in the given set")
        print("Minimum Variance in the set is:", low[0], low[1])
        print("Maximum Variance in the set is:", high[0], high[1])

        # only the shares with variance lower than the low centroid are considered safe.
        print("========================Share Safety=================================")
        for company in x.keys():
            if x[company][0] < x2[0] and x[company][1] < x2[1]:
                print("Company with label", company,
                      "is relatively safe for investment")
            else:
                print("Company with label", company,
                      "is unsafe for investment")
