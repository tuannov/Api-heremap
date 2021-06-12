import requests
import json

def import_api_key(filepath):
    with open(filepath) as f:
        api_key = f.read().rstrip()
    return api_key


def get_data(api_key):
    url = "https://discover.search.hereapi.com/v1/discover"
    payload = {
        "in": "circle:21.02984,105.859306;r=5000",
        "q": "hotel",
        "apiKey": api_key,
    }
    ses = requests.Session()
    r = ses.get(url, params=payload, timeout=5)
    return r.json()

def out_put(data):
    features = []
    for hotel in data["items"]:
        address = hotel["address"]["label"]
        name = hotel["title"]
        distance = str(hotel["distance"]) + " meter"
        lng = hotel["position"]["lng"]
        lat = hotel["position"]["lat"]
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat],
            },
            "properties": {"address": address, "name": name, "distance": distance},
        }
        features.append(feature)

    with open("map.geojson", "wt", encoding="utf8") as f:
        geojson_data = {"type": "FeatureCollection", "features": features}
        json.dump(geojson_data, f, indent=4, ensure_ascii=False)

def main():
    api_key = import_api_key("api_key.txt")
    data = get_data(api_key)
    out_put(data)
    print("Success !!!")

if __name__=='__main__':
    main()
