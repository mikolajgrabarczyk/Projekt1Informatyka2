import math

class Transformacje:
    def __init__(self, ellipsoid):
        """
        Parametry elipsoid:
            self.a -  promień równikowy
            self.b -  promień południkowy
            flattening - spłaszczenie
            e2 - kwadrat mimośrodu
        """
        if ellipsoid == "wgs84":
            self.a = 6378137.0
            self.b = 6356752.31424518
        elif ellipsoid == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        else:
            print("Błędna elipsoida")
        self.flattening = (self.a - self.b) / self.a
        self.e2 = math.sqrt(2 * self.flattening - self.flattening ** 2)

    def hirvonen(self, X, Y, Z):
        """
        Funkcja przelicza współrzędne geocentryczn na współrzędne geodezyjne.
        Parametry:
      
        X  [float] : współrzędna geocentryczna [m]
        Y  [float] : współrzędna geocentryczna [m]
        Z  [float] : współrzędna geocentryczna [m]
            
        Funkcja zwraca:
      
        fi [float] : szerokość geodezyjna [rad]
        lam [float] : długość geodezyjna [rad]
        h  [float] : wysokość elipsoidalna [m]
        """
        r = math.sqrt(X ** 2 + Y ** 2)
        fi_n = math.atan(Z / (r * (1 - self.e2)))
        eps = 0.000001 / 3600 * math.pi / 180
        fi = fi_n * 2
        while math.fabs(fi - fi_n) > eps:
            fi = fi_n
            N = self.a / math.sqrt(1 - self.e2 * math.sin(fi_n) ** 2)
            h = r / math.cos(fi_n) - N
            fi_n = math.atan(Z / (r * (1 - self.e2 * (N / (N + h)))))
        lam = math.atan(Y / X)
        h = r / math.cos(fi_n) - N
        return fi, lam, h

    def geodetic_to_geocentric(self, fi, lam, h):
        """
        Funkcja przelicza współrzędne geodezyjne  
        na współrzędne geocentryczne.
        Parametry:
       
        fi [float] : szerokość geodezyjna [rad]
        lam[float] : długość geodezyjna [rad]
        h   [float] : wysokość elipsoidalna [m]
        Funkcja zwraca:
        
        X [float] : współrzędna geocentryczna[m]
        Y [float] : współrzędna geocentryczna[m]
        Z [float] : współrzędna geocentryczna[m]
        """
        N = self.a / math.sqrt(1 - self.e2 * math.sin(fi) ** 2)
        X = (N + h) * math.cos(fi) * math.cos(lam)
        Y = (N + h) * math.cos(fi) * math.sin(lam)
        Z = (N * (1 - self.e2) + h) * math.sin(fi)
        return (X, Y, Z)

    def compute_neu(self, X0, Y0, Z0, X, Y, Z):
        """   
        Funkcja przelicza współrzędne geodezyjne  
        na współrzędne topograficzne.
        Parametry:
        X0 [float] : współrzędna geocentryczna[m]
        Y0 [float] : współrzędna geocentryczna[m]
        Z0 [float] : współrzędna geocentryczna[m]
        X [float] : współrzędna geocentryczna[m]
        Y [float] : współrzędna geocentryczna[m]
        Z [float] : współrzędna geocentryczna[m]

        Funkcja zwraca:
        N [float] : wpółrzedna topocentryczna N (north) [m]
        E [float] : wpółrzedna topocentryczna E (east) [m]
        U [float] : wpółrzedna topocentryczna U (up) [m]
        
        Punkty z dopiskiem 0 są początkiem układu współrzędnych.(Początek wektora NEU)
        Punktuy bez dopiska 0 reprezentują nasz punkt.

        """
        import numpy as np
        fi, lam, h = self.hirvonen(X, Y, Z)

        delta_X = X - X0
        delta_Y = Y - Y0
        delta_Z = Z - Z0

        R = np.array([[-np.sin(fi) * np.cos(lam), -np.sin(fi) * np.sin(lam), np.cos(fi)],
                      [-np.sin(lam), np.cos(lam), 0],
                      [np.cos(fi) * np.cos(lam), np.cos(fi) * np.sin(lam), np.sin(fi)]])

        d = np.array([delta_X, delta_Y, delta_Z])
        neu = np.matmul(R, d)
        n = neu[0]
        e = neu[1]
        u = neu[2]
    def geo_to_flat_2000(self, fi, lam):
        """   
        Funkcja przelicza współrzędne geodezyjne  
        na współrzędne układu 2000.
    
        Parametry:
        fi  [float] : szerokość geodezyjna [rad]
        lam [float] : długość geodezyjna [rad]
    
        Funkcja zwraca:
        x00 [float] : współrzędna w układzie płaskim 2000 [m]
        y00 [float] : współrzędna w układzie płaskim 2000 [m]
    
        """
        m = 0.999923
        N = self.a / math.sqrt(1 - self.e2 * math.sin(fi) ** 2)
        t = math.tan(fi)
        e_2 = self.e2 / (1 - self.e2)
        n2 = e_2 * (math.cos(fi)) ** 2

        lam = math.degrees(lam)
        if lam > 13.5 and lam < 16.5:
            s = 5
            lam0 = 15
        elif lam > 16.5 and lam < 19.5:
            s = 6
            lam0 = 18
        elif lam > 19.5 and lam < 22.5:
            s = 7
            lam0 = 21
        elif lam > 22.5 and lam < 25.5:
            s = 8
            lam0 = 24

        lam = math.radians(lam)
        lam0 = math.radians(lam0)
        l = lam - lam0

        A0 = 1 - (self.e2 / 4) - ((3 * (self.e2 ** 2)) / 64) - ((5 * (self.e2 ** 3)) / 256)
        A2 = (3 / 8) * (self.e2 + ((self.e2 ** 2) / 4) + ((15 * (self.e2 ** 3)) / 128))
        A4 = (15 / 256) * (self.e2 ** 2 + ((3 * (self.e2 ** 3)) / 4))
        A6 = (35 * (self.e2 ** 3)) / 3072

        sig = self.a * ((A0 * fi) - (A2 * math.sin(2 * fi)) + (A4 * math.sin(4 * fi)) - (A6 * math.sin(6 * fi)))

        x = sig + ((l ** 2) / 2) * N * math.sin(fi) * math.cos(fi) * (
                    1 + ((l ** 2) / 12) * ((math.cos(fi)) ** 2) * (5 - t ** 2 + 9 * n2 + 4 * (n2 ** 2)) + (
                        (l ** 4) / 360) * ((math.cos(fi)) ** 4) * (
                                61 - (58 * (t ** 2)) + (t ** 4) + (270 * n2) - (330 * n2 * (t ** 2))))
        y = l * (N * math.cos(fi)) * (1 + ((((l ** 2) / 6) * (math.cos(fi)) ** 2) * (1 - t ** 2 + n2)) + (
                    ((l ** 4) / (120)) * (math.cos(fi) ** 4)) * (
                                                  5 - (18 * (t ** 2)) + (t ** 4) + (14 * n2) - (58 * n2 * (t ** 2))))

        x00 = round(m * x, 3)
        y00 = round(m * y + (s * 1000000) + 500000, 3)

        return (x00, y00)

    def geo_to_flat_1992(self, fi, lam):
        """   
        Funkcja przelicza współrzędne geodezyjne  
        na współrzędne układu 1992.
    
        Parametry:
        fi  [float] : szerokość geodezyjna [rad]
        lam [float] : długość geodezyjna [rad]
    
        Funkcja zwraca:
        x92 [float] : współrzędna w układzie płaskim 1992 [m]
        y92 [float] : współrzędna w układzie płaskim 1992 [m]
    
        """
        m_0 = 0.9993
        N = self.a / (math.sqrt(1 - self.e2 * math.sin(fi) ** 2))
        t = math.tan(fi)
        e_2 = self.e2 / (1 - self.e2)
        n2 = e_2 * (math.cos(fi)) ** 2

        lam_0 = math.radians(19)
        l = lam - lam_0

        A0 = 1 - (self.e2 / 4) - ((3 * (self.e2 ** 2)) / 64) - ((5 * (self.e2 ** 3)) / 256)
        A2 = (3 / 8) * (self.e2 + ((self.e2 ** 2) / 4) + ((15 * (self.e2 ** 3)) / 128))
        A4 = (15 / 256) * (self.e2 ** 2 + ((3 * (self.e2 ** 3)) / 4))
        A6 = (35 * (self.e2 ** 3)) / 3072

        sig = self.a * ((A0 * fi) - (A2 * math.sin(2 * fi)) + (A4 * math.sin(4 * fi)) - (A6 * math.sin(6 * fi)))

        x = sig + ((l ** 2) / 2) * N * math.sin(fi) * math.cos(fi) * (
                    1 + ((l ** 2) / 12) * ((math.cos(fi)) ** 2) * (5 - t ** 2 + 9 * n2 + 4 * (n2 ** 2)) + (
                        (l ** 4) / 360) * ((math.cos(fi)) ** 4) * (
                                61 - (58 * (t ** 2)) + (t ** 4) + (270 * n2) - (330 * n2 * (t ** 2))))
        y = l * (N * math.cos(fi)) * (1 + ((((l ** 2) / 6) * (math.cos(fi)) ** 2) * (1 - t ** 2 + n2)) + (
                    ((l ** 4) / (120)) * (math.cos(fi) ** 4)) * (
                                                  5 - (18 * (t ** 2)) + (t ** 4) + (14 * n2) - (58 * n2 * (t ** 2))))

        x92 = round(m_0 * x - 5300000, 3)
        y92 = round(m_0 * y + 500000, 3)
        return x92, y92
