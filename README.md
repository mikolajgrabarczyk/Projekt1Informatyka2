# Program do przekształceń współrzędnych

## Opis

Ten program oferuje funkcjonalność przekształcania współrzędnych pomiędzy dwoma formatami: XYZ i BLH. Obsługuje wiele elipsoid, w tym WGS84, GRS80.

## Wymagania

Aby uruchomić ten program na swoim komputerze, musisz spełnić następujące wymagania:

- Zainstalować Pythona w wersji 3.7 lub nowszej
- Zainstalować bibliotekę numpy

## Kompatybilność z systemami operacyjnymi

Program został napisany z myślą o systemach operacyjnych Windows, Linux i macOS.

## Instrukcja użycia

Przykład użycia programu:

1. Zapisz współrzędne XYZ w pliku tekstowym (np. `input_coordinates.txt`) w następującym formacie:

```
3664940.500,1409153.590,5009571.170
3664940.510,1409153.580,5009571.167
3664940.520,1409153.570,5009571.167
```

2. Uruchom program z linii poleceń, podając ścieżki do plików wejściowego i wyjściowego:

```
python main.py --input input_coordinates.txt --output output_results.txt
```

3. Wybierz elipsoidę, na której zostały zapisane współrzędne XYZ (np. `WGS84`).


4. Wyniki przekształceń zostaną zapisane w pliku wyjściowym (np. `output_results.txt`).

## Znane błędy i nietypowe zachowania
Transformacja Krasowski -> 2000 daje błedne rezultaty i nie powinna być uzywana

- 