class Transformacje:
    def __init__(self, ellipsoid="wgs84"):
        if ellipsoid == "wgs84":
            self.a = 6378137.0
            self.b = 6356752.31424518
        elif ellipsoid == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        else:
            print("This ellipsoid is not supported")
        self.flattening = (self.a - self.b) / self.a
        self.e2 = sqrt(2 * self.flattening - self.flattening ** 2)

    def hirvonen(self, X, Y, Z):
        r = math.sqrt(X ** 2 + Y ** 2)
        fi_n = math.atan(Z / (r * (1 - self.e2)))
        eps = 0.000001 / 3600 * math.pi / 180
        fi = fi_n * 2
        while np.abs(fi_n - fi) > eps:
            fi = fi_n
            N = self.a / np.sqrt(1 - self.e2 * np.sin(fi_n) ** 2)
            h = r / np.cos(fi_n) - N
            fi_n = math.atan(Z / (r * (1 - self.e2 * (N / (N + h)))))
        lam = math.atan(Y / X)
        h = r / np.cos(fi_n) - N
        return fi, lam, h
    def geodetic_to_geocentric(self, fi, lam, h):
        N = self.a / math.sqrt(1 - self.e2 * math.sin(fi) ** 2)
        X = (N + h) * math.cos(fi) * math.cos(lam)
        Y = (N + h) * math.cos(fi) * math.sin(lam)
        Z = (N * (1 - self.e2) + h) * math.sin(fi)
        return (X, Y, Z)

    def compute_neu(self, X0, Y0, Z0, X, Y, Z):
        fi, lam, h = self.hirvonen(X, Y, Z)

        delta_X = X - X0
        delta_Y = Y - Y0
        delta_Z = Z - Z0

        R = np.matrix([((-np.sin(fi) * np.cos(lam)), (-np.sin(fi) * np.sin(lam)), (np.cos(fi))),
                       ((-np.sin(lam)), (np.cos(lam)), (0)),
                       ((np.cos(fi) * np.cos(lam)), (np.cos(fi) * np.sin(lam)), (np.sin(fi)))])

        d = np.matrix([delta_X, delta_Y, delta_Z])
        d = d.T
        neu = R * d
        n = neu[0, 0]
        e = neu[1, 0]
        u = neu[2, 0]
        return (n, e, u)
