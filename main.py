import googlemaps
from itertools import permutations

gmaps = googlemaps.Client(key='AIzaSyA5b9uc02LfxO0LBYvoq9pmf0jiOZVABHw')

locations = {
    "Ruh Sağlığı Hastanesi": [37.051656793129034, 35.26283059639736], #Adana
    "Duygu Cafe": [37.02876117747951, 35.313462030760064], #Adana
    "Optimum AVM": [36.99170658213755, 35.33938390966201], #Adana
    "Menderes Adası": [37.050649440432714, 35.31678042813558], #Adana
    "Sarıçam Halk Eğitim Merkezi": [37.03531216794115, 35.41561461151117],  #Adana
    "M1 AVM": [37.017544068475104, 35.245246611510204],  #Adana
    "Forum AVM": [36.78537879785163, 34.58849100780505], #Mersin
    "Soli Center AVM": [36.73672611292621, 34.51587001149689], #Mersin
    "Mersin Tren Garı": [36.80284155622529, 34.63377046732356], #Mersin
    "Toros Üniversitesi Mezitli Kampüsü": [36.738084933818044, 34.50591606916749], #Mersin
    "Mersin Marina": [36.77170719290905, 34.570954609498024], #Mersin
    "Toros Üniversitesi 45 Evler Kampüsü": [36.79184309274947, 34.5954615268406], #Mersin
    "Antalya Şehir Merkezi": [36.89845821311691, 30.712608141264873],
    "Osmaniye Şehir Merkezi":[37.07365030733004, 36.27651187469366],
    "Eskişehir Şehir Merkezi": [39.76504996383986, 30.533824576957844],
    "Ankara Şehir Merkezi": [39.93064519089271, 32.87604693474099],
    "Gaziantep Şehir Merkezi": [37.065866041512926, 37.39043289495136]
}

def get_current_location():
    try:
        # Google Maps Geolocation API'si ile canlı konum alma
        current_location = gmaps.geolocate()
        if 'location' in current_location:
            latitude = current_location['location']['lat']
            longitude = current_location['location']['lng']
            return latitude, longitude
        else:
            return None
    except Exception as e:
        print("Konum bilgisi alınamadı:", e)
        return None

def calculate_distance(location1, location2):
    # Google Maps ile iki konum arasındaki mesafeyi al
    directions = gmaps.directions(
        (location1[0], location1[1]),
        (location2[0], location2[1]),
        mode="driving"
    )
    distance = directions[0]['legs'][0]['distance']['value']
    return distance

def calculate_shortest_route(locations, selected_locations):
    current_location = get_current_location()
    if current_location:
        print(f"Canlı konum: {current_location}")

        # Kullanıcının seçtiği lokasyonları al ve sırala
        selected_coords = [locations[loc] for loc in selected_locations]
        selected_coords.insert(0, current_location)
        selected_names = ["Canlı Konum"] + selected_locations

        shortest_route = None
        shortest_distance = float('inf')

        # Seçilen rotaların permütasyonlarını oluştur
        for permutation in permutations(selected_coords):
            total_distance = 0

            # Seçilen rotanın toplam mesafesini hesapla
            for i in range(len(permutation) - 1):
                distance = calculate_distance(permutation[i], permutation[i + 1])
                total_distance += distance

            # En kısa rotayı güncelle
            if total_distance < shortest_distance:
                shortest_distance = total_distance
                shortest_route = permutation

        return shortest_route, shortest_distance, selected_names
    else:
        return None, None, None

# Kullanıcıya lokasyonları göster
print("Lütfen uğramak istediğiniz lokasyonları seçin:")
for i, location in enumerate(locations.keys(), start=1):
    print(f"{i}: {location}")

selected_locations = []
while True:
    try:
        choice = int(input("Uğramak istediğiniz lokasyonun numarasını seçin (0 girerek tamamlayabilirsiniz): "))
        if choice == 0:
            break
        elif choice > 0 and choice <= len(locations):
            selected_locations.append(list(locations.keys())[choice - 1])
        else:
            print("Geçersiz bir numara girdiniz. Lütfen tekrar deneyin.")
    except ValueError:
        print("Lütfen bir sayı girin.")

def generate_maps_link(locations_order):
    base_url = "https://www.google.com/maps/dir/"
    coordinates = "/".join([f"{location[0]},{location[1]}" for location in locations_order])
    return f"{base_url}{coordinates}"

# En kısa rotayı hesapla ve yazdır
shortest_route, shortest_distance, route_names = calculate_shortest_route(locations, selected_locations)
if shortest_route and shortest_distance:
    print("En kısa rota:", route_names)
    print("En kısa mesafe:", shortest_distance, "metre")

    # Tüm duraklarla birlikte doğrudan Google Haritalar Yolculuk Bağlantısını oluştur
    maps_link = generate_maps_link(shortest_route)
    print("Google Maps ile Yolculuk Linki:")
    print(maps_link)
else:
    print("En kısa rota hesaplanamadı.")

