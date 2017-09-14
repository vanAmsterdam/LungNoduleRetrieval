import numpy as np
import matplotlib.pyplot as plt
import pickle

from sklearn.neighbors import DistanceMetric
from sklearn.metrics import pairwise
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import pearsonr, spearmanr, kendalltau
from scipy.spatial.distance import pdist, cdist, squareform

import LIDC.lidcUtils


def calc_distance_matrix(X, method):
    precalc_var = np.array(
        [1.3731895, 0.03974337, 0.89052489, 0.89331349, 1.37905025, 1.09002916, 1.07042897, 1.33024606, 1.33381279])
    precalc_inv_cov = np.array([[  7.28125436e-01,   1.34050971e+02,  -5.12486474e+00,
          7.30312998e+01,   2.72001370e+00,   4.64116113e+00,
          4.11725258e+00,   1.89716927e+00,   3.11645901e+00],
       [  1.34050971e+02,   2.51577591e+01,   2.03904002e+02,
          2.24102058e+03,  -8.23156338e+01,   2.33231302e+02,
          1.18055018e+02,  -1.33743011e+02,   1.31300759e+02],
       [ -5.12486474e+00,   2.03904002e+02,   1.12276952e+00,
         -9.25662338e+00,  -3.34603002e+00,   8.51188431e+00,
          8.11612617e+00,  -5.25316411e+00,   1.70636132e+00],
       [  7.30312998e+01,   2.24102058e+03,  -9.25662338e+00,
          1.11926465e+00,   3.37588094e+00,  -5.16312839e+00,
         -5.16023295e+00,   1.31923564e+01,  -6.39611977e+00],
       [  2.72001370e+00,  -8.23156338e+01,  -3.34603002e+00,
          3.37588094e+00,   7.25031017e-01,  -3.27441893e+00,
         -3.22150175e+00,   1.12212162e+00,  -3.34856559e+00],
       [  4.64116113e+00,   2.33231302e+02,   8.51188431e+00,
         -5.16312839e+00,  -3.27441893e+00,   9.17272900e-01,
          1.77987606e+00,  -3.12902591e+01,   2.40619405e+00],
       [  4.11725258e+00,   1.18055018e+02,   8.11612617e+00,
         -5.16023295e+00,  -3.22150175e+00,   1.77987606e+00,
          9.34068708e-01,  -2.35575211e+01,   2.22446280e+00],
       [  1.89716927e+00,  -1.33743011e+02,  -5.25316411e+00,
          1.31923564e+01,   1.12212162e+00,  -3.12902591e+01,
         -2.35575211e+01,   7.51631020e-01,  -1.06070550e+01],
       [  3.11645901e+00,   1.31300759e+02,   1.70636132e+00,
         -6.39611977e+00,  -3.34856559e+00,   2.40619405e+00,
          2.22446280e+00,  -1.06070550e+01,   7.49621094e-01]])


    if method in ['chebyshev', 'euclidean']:
        DM = DistanceMetric.get_metric(method).pairwise(X)
    elif method in ['seuclidean']:
        DM = squareform(pdist(X, method, V=precalc_var))
    elif method in ['mahalanobis']:
        DM = squareform(pdist(X, method, VI=precalc_inv_cov))
    elif method in ['cosine']:
        DM = pairwise.cosine_distances(X)
    elif method in ['minkowski3']:
        DM = squareform(pdist(X, 'minkowski', 3))
    elif method in ['correlation', 'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'cosine', 'dice', 'euclidean', 'hamming', 'jaccard', 'kulsinski', 'matching', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath', 'yule']:
        DM = squareform(pdist(X, method))
    else:
        return None

    return DM

def calc_cross_distance_matrix(X, Y, method):
    if method in ['chebyshev', 'euclidean', 'cosine', 'correlation']:
        #DM = squareform(cdist(X, Y, method))
        DM = cdist(X, Y, method)
    else:
        return None

    return DM

def flatten_dm(DM):
    return DM[np.triu_indices(DM.shape[0], 1)].reshape(-1, 1)



#metrics =   [ 'euclidean'    # L2
#            , 'chebyshev'    # L-inf
#            , 'cosine'
#            , 'hamming'
#            , 'manhaten'
#            ]

metrics =   ['cityblock', 'euclidean', 'seuclidean', 'minkowski3', 'chebyshev', 'cosine', 'correlation', 'hamming', 'mahalanobis', 'braycurtis', 'canberra', 'jaccard']
#

dataset = pickle.load(open('NodulePatches.p', 'br'))
Ratings = np.concatenate([entry['rating'] for entry in dataset])

for metric in metrics[:]:

    # intra
    # =======
    intra = []
    for entry in dataset:

        dm = calc_distance_matrix(entry['rating'], metric)
        if dm.shape[0] > 1:
            dm = flatten_dm(dm)
            intra.append(np.mean(dm))
        else:
            intra.append(dm)

    intra_dist = np.mean(intra)

    # inter
    # ========
    dm = calc_distance_matrix(Ratings, metric)
    dm = flatten_dm(dm)

    innter_dist = np.mean(dm)

    print('Metric: {} - \tFactor = {:.2f}'.format(metric, intra_dist/innter_dist))
    #print('\tinter dist = {:.2f}'.format(innter_dist))
    #print('\tintra dist = {:.2f}'.format(intra_dist))