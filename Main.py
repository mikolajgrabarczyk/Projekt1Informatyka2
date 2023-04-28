class Main:
    def __init__(self, input_file, output_file, ellipsoid_type):
        self.input_file = input_file
        self.output_file = output_file
        self.coordinate_transform = CoordinateTransform(ellipsoid_type)
        self.data = []

    def read_input_file(self):
        data = []
        with open(self.input_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                X, Y, Z = [float(val) for val in line.strip().split(',')]
                data.append((X, Y, Z))
        return data


    def display_menu(self):
        print("Wybierz rodzaj transformacji:")
        print("1. XYZ -> BLH")
        print("2. BLH -> XYZ")
        print("3. XYZ -> NEUp")
        print("4. BL (GRS80, WGS84, ew. Krasowski) -> 2000")
        print("5. BL (GRS80, WGS84, ew. Krasowski) -> 1992")
        choice = input("Wpisz numer opcji (1/2/3/4/5): ")
        return choice
