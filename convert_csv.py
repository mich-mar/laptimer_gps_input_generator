import gpxpy
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta
import random
from shapely.geometry import LineString

# Funkcja do wczytania współrzędnych z pliku GPX
def load_gpx_coordinates(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    coordinates = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinates.append((point.longitude, point.latitude))  # Dodaj współrzędne (lon, lat)
    return coordinates

# Funkcja do generowania odstępów czasowych z losowymi krokami i modyfikacją końcowego czasu
def generate_timestamps_with_random_variation(coordinates, total_time_seconds=300):
    num_points = len(coordinates)
    base_interval = total_time_seconds / num_points  # Średni czas między punktami

    timestamps = []
    current_time = datetime.now()

    for i in range(num_points):
        # Losowy krok czasu w przedziale -10 do +10 sekund
        interval = base_interval + random.uniform(-10, 10)  # Zwiększenie zakresu zmiany czasu
        current_time += timedelta(seconds=interval)
        timestamps.append(current_time)

    # Losowa modyfikacja całkowitego czasu trwania trasy (+/- 30 sekund)
    final_adjustment = random.uniform(-30, 30)
    timestamps[-1] = timestamps[0] + timedelta(seconds=total_time_seconds + final_adjustment)

    return timestamps

# Funkcja do losowej modyfikacji współrzędnych w procentach
def modify_coordinates_randomly(coordinates, percentage_change=1.0):
    modified_coordinates = []
    for lon, lat in coordinates:
        # Oblicz odległość w stopniach (procent zmiany)
        lon_variation = (random.uniform(-percentage_change, percentage_change) / 100) * 0.02  # Zmiana na podstawie 1% odległości 0.02 stopnia
        lat_variation = (random.uniform(-percentage_change, percentage_change) / 100) * 0.02  # Zmiana na podstawie 1% odległości 0.02 stopnia
        modified_coordinates.append((lon + lon_variation, lat + lat_variation))
    return modified_coordinates

# Funkcja do zapisu współrzędnych i czasu do pliku CSV
def save_coordinates_to_csv(coordinates, timestamps, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Longitude', 'Latitude', 'Timestamp'])  # Nagłówki
        for coord, timestamp in zip(coordinates, timestamps):
            csvwriter.writerow([coord[0], coord[1], timestamp.strftime('%Y-%m-%d %H:%M:%S')])  # Zapis danych
    print(f"Dane zostały zapisane do pliku {output_file}.")

# Funkcja do tworzenia wielu plików z losowymi modyfikacjami czasów i współrzędnych
def create_multiple_files_with_random_variations(coordinates, base_filename, num_files, total_time_seconds=300):
    all_coordinates = []
    for i in range(num_files):
        output_file = f"{base_filename}_{i+1}.csv"
        modified_coordinates = modify_coordinates_randomly(coordinates, percentage_change=1.0)  # Użyj procentowej zmiany
        timestamps = generate_timestamps_with_random_variation(
            modified_coordinates,
            total_time_seconds=total_time_seconds
        )
        save_coordinates_to_csv(modified_coordinates, timestamps, output_file)
        all_coordinates.append(modified_coordinates)
    return all_coordinates

# Ścieżka do pliku GPX (zastąp własną)
gpx_file_path = 'gpx_maps/TOR450 Tor des Glaciers FULL.gpx'

# Wczytanie danych z pliku
coordinates = load_gpx_coordinates(gpx_file_path)

# Generowanie wielu plików CSV z losowymi modyfikacjami
output_base_filename = 'TOR450_csv_maps/TOR450_Variations'
num_files = 5  # Liczba plików do utworzenia
total_time_seconds = 300  # Średni czas trwania całej trasy (5 minut)

all_coordinates = create_multiple_files_with_random_variations(coordinates, output_base_filename, num_files, total_time_seconds)

# Funkcja do rysowania wielu tras na jednej mapie
def plot_multiple_gpx(all_coordinates):
    plt.figure(figsize=(10, 10))

    colors = plt.cm.jet(range(0, 256, int(256 / len(all_coordinates))))  # Generowanie kolorów

    for coordinates, color in zip(all_coordinates, colors):
        line = LineString([(lon, lat) for lon, lat in coordinates])  # Tworzenie obiektu LineString
        x, y = line.xy
        plt.plot(x, y, color=color, linewidth=2, alpha=0.7)

    plt.title("Mapa tras z GPX")
    plt.xlabel("Długość geograficzna")
    plt.ylabel("Szerokość geograficzna")
    plt.grid()
    plt.show()

plot_multiple_gpx(all_coordinates)
