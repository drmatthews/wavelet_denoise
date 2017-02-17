import numpy as np

class BSpline:
    def __init__(self, order, scale, samples):
        self.k = order
        self.s = scale
        self.t = samples

    def bspline_blender(self):
        k = self.k
        t = np.add(np.divide(self.t, self.s), float(self.k) / 2.0)
        return self.normalize(self.N(k, t))

    def N(self, k, t):
        if k <= 1:
            return self.haar(t)
        else:
            res = np.zeros((t.shape[0],))
            for i, el in enumerate(t):
                ti = np.array([t[i],])
                Nt = self.N(k - 1, ti)
                Nt_1 = self.N(k - 1, ti - 1)
                res[i] = ti / (k - 1) * Nt[0] + (k - ti) / (k - 1) * Nt_1[0]
            return res

    def haar(self, t):
        res = np.array(range(t.shape[0]))
        for i in range(t.shape[0]):
            if (t[i] >= 0) and (t[i] < 1):
                res[i] = 1.0
            else:
                res[i] = 0.0
        return res        

    def normalize(self,arr):
        return np.divide(arr, np.sum(arr))