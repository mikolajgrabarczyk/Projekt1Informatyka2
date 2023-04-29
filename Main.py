import argparse
from coordinatetransforms import CoordinateTransforms
import numpy as np

def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            X, Y, Z = map(float, line.strip().split(','))
            coordinates.append((X, Y, Z))
    return np.array(coordinates)

def write_results_to_file(output_file_path, results_array):
    with open(output_file_path, 'w') as output_file:
        for row in results_array:
            formatted_row = ',   '.join(f"{num:.6f}" if isinstance(num, (int, float)) else str(num) for num in row)
            output_file.write(formatted_row + '\n')

def execute():

    arg_parser = argparse.ArgumentParser(description="Coordinate transformation program.")
    arg_parser.add_argument("-i", "--input", help="path to input file with coordinates")
    arg_parser.add_argument("-o", "--output", help="path to output file with results")

    arguments = arg_parser.parse_args()

    if arguments.input and arguments.output:
        input_coordinates = read_coordinates_from_file(arguments.input)
        output_file_path = arguments.output

        rows, columns = np.shape(input_coordinates)
        geodetic_coords = np.zeros((rows, columns))
        geocentric_coords = np.zeros((rows, columns))
        flat_2000_coords = np.zeros((rows, 2))
        flat_1992_coords = np.zeros((rows, 2))
        topocentric_coords = np.zeros((rows, columns))

        transformResults = []

        print('Wybierz elipsoidę:')
        print('1 | WGS84')
        print('2 | GRS80')
        selected = input('Wybór: ')
        if selected == '1':
            ellipsoid = CoordinateTransforms("wgs84")
        elif selected == '2':
            ellipsoid = CoordinateTransforms("grs80")
        else:
            print("Nieznana ellipsoida")

        for i in range(rows):
            geodetic_coords[i] = ellipsoid.hirvonen(input_coordinates[i, 0], input_coordinates[i, 1], input_coordinates[i, 2])
            geocentric_coords[i] = ellipsoid.geodetic_to_geocentric(geodetic_coords[i, 0], geodetic_coords[i, 1], geodetic_coords[i, 2])
            flat_2000_coords[i] = ellipsoid.geo_to_flat_2000(geodetic_coords[i, 0], geodetic_coords[i, 1])
            flat_1992_coords[i] = ellipsoid.geo_to_flat_1992(geodetic_coords[i, 0], geodetic_coords[i, 1])
            topocentric_coords[i] = ellipsoid.compute_neu(input_coordinates[i, 0], input_coordinates[i, 1], input_coordinates[i, 2],
                                            input_coordinates[i, 0] + 1, input_coordinates[i, 1] + 1, input_coordinates[i, 2] + 1)


        while True:
            print("\nOptions:")
            print("1 | Transformacja współrzędnych geocentrycznych na geodezyjne")
            print("2 | Transformacja współrzędnych geodezyjnych na geocentryczne")
            print("3 | Obliczenie współrzędnych topocentrycznych E,N,U")
            print("4 | Transformacja współrzędnych geodezyjnych na płaski układ 2000")
            print("5 | Transformacja współrzędnych geodezyjnych na płaski układ 1992")
            print("6 | Wyjście")
            selected = input("\nChoose option (1-6): ")

            if selected == '1':
                print('Szerokość geodezyjna | Długość geodezyjna | Wysokość elipsoidalna')
                for i in range(rows):
                    geodetic_coords[i] = ellipsoid.hirvonen(input_coordinates[i, 0], input_coordinates[i, 1], input_coordinates[i, 2])
                    print(f'{geodetic_coords[i][0]} | {geodetic_coords[i][1]} | {geodetic_coords[i][2]}')
                    transformResults.append(geodetic_coords[i])
            elif selected == '2':
                print('X | Y | Z')
                for i in range (rows):
                    geocentric_coords[i] = ellipsoid.geodetic_to_geocentric(geodetic_coords[i, 0], geodetic_coords[i, 1], geodetic_coords[i, 2])
                    print(f'{geocentric_coords[i][0]} | {geocentric_coords[i][1]} | {geocentric_coords[i][2]}')
                    transformResults.append(geocentric_coords[i])
            elif selected == '3':
                print('N | E | U')
                for i in range(rows):
                    topocentric_coords[i] = ellipsoid.compute_neu(input_coordinates[i, 0], input_coordinates[i, 1], input_coordinates[i, 2],
                    input_coordinates[i, 0] + 1, input_coordinates[i, 1] + 1, input_coordinates[i, 2] + 1)
                    print(f'{topocentric_coords[i][0]} | {topocentric_coords[i][1]} | {topocentric_coords[i][2]}')
                    transformResults.append(topocentric_coords[i])
            elif selected == '4':
                print('Płaskie_2000_X | Płaskie_2000_Y')
                for i in range(rows):
                    flat_2000_coords[i] = ellipsoid.geo_to_flat_2000(geodetic_coords[i, 0], geodetic_coords[i, 1])
                    print(f'{flat_2000_coords[i][0]} | {flat_2000_coords[i][1]}')
                    transformResults.append(flat_2000_coords[i])
            elif selected == '5':
                print('Płaskie_1992_X | Płaskie_1992_Y')
                for i in range(rows):
                    flat_1992_coords[i] = ellipsoid.geo_to_flat_1992(geodetic_coords[i, 0], geodetic_coords[i, 1])
                    print(f'{flat_1992_coords[i][0]} | {flat_1992_coords[i][1]}')
                    transformResults.append(flat_1992_coords[i])
            elif selected == '6':
                print("Wyjście z programu.")
                break
            else:
                print("Zły wybór, spróbuj ponownie.")

            write_results_to_file(output_file_path, transformResults)
            print("Transformacja przebiegła pomyślnie. Wyniki zostaly zapisane do pliku wyjściowego.")
            break
    else:
        print("Missing input or output file. Please try again with correct arguments.")

if __name__ == "__main__":
    execute()
