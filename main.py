import random
import networkx as nx
import pandas as pd
import json
import numpy
import osmnx as ox

from factory import *
from visualize import visualize_interactive


def create_graph(place, network):
    graph = ox.graph_from_place(place, network_type=network)
    G = ox.convert.to_digraph(graph)

    return graph, G


def json_save(output_data):
    with open('movement.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print("Данные о перемещении сохранены в movement.json")


def calculate_time(start_point, end_point, has_car=True, is_raining=False, is_urgent=False):
    speeds = {
        'walk': 5000,
        'bike': 15000,
        'drive': 60000
    }

    if is_raining: speeds['walk'] *= 0.7
    if is_urgent: speeds['drive'] *= 1.2

    graphs = {}
    # if has_car: graphs['drive'] = G_drive
    # graphs.update({'walk': G_walk, 'bike': G_bike})

    best_time = float('inf')
    best_result = None

    for transport, G in graphs.items():
        try:
            route = nx.shortest_path(G, ox.nearest_nodes(G, *start_point[::-1]),
                                     ox.nearest_nodes(G, *end_point[::-1]),
                                     weight='length')
            dist = sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length'))
            time = dist / speeds[transport] * 60  # В минутах

            if transport == 'drive':
                time += 5  # Парковка
            elif transport == 'bike':
                time += 3  # Замок

            if time < best_time:
                best_time = time
                best_result = (G, route, transport, timedelta(minutes=time))
        except:
            continue

    return best_result


def generate_track(nodes, place, places):
    # Получаем случайный жилой дом
    gdf = ox.features.features_from_place(place, tags={"building": ["apartments", "residential", "house"]})
    houses = gdf[pd.notnull(gdf["building"])]
    home = houses.sample(1).iloc[0]
    home_point = home.geometry.centroid

    # Находим ближайший узел графа для стартовой точки
    start_node = ox.distance.nearest_nodes(G, home_point.x, home_point.y)
    start_address = f"Лобня, {home.get('addr:street', 'улица не указана')}, {home.get('addr:housenumber', 'номер не указан')}"

    movement_data = []
    current_node = start_node
    routes = []
    current_time = 0
    distance = 3000

    speeds = {
        'walk': 5000,
        'bike': 15000,
        'drive': 50000
    }
    transport = 'drive'

    for i, place_info in enumerate(places):
        tag, value, time_type, time_value = place_info

        if time_type == "time":
            current_time = time_value
        elif time_type == "delta":
            current_time += time_value

        print(current_time, tag)

        # Ищем объекты нужного типа в радиусе search_radius
        if i == len(places) - 1:  # Возвращаемся домой
            end_place = home
        else:
            # Поиск в радиусе от текущей позиции
            point = G.nodes[current_node]
            current_location = (point['y'], point['x'])

            try:
                nearby_objects = ox.features_from_point(
                    center_point=current_location,
                    dist=distance,
                    tags={tag: value}
                )
            except ox._errors.InsufficientResponseError as e:
                print(f"Не найдено объектов {tag}={value} в радиусе {distance} м")
                continue

            end_place = nearby_objects.sample(1).iloc[0]

        end_point = end_place.geometry.centroid
        end_node = ox.distance.nearest_nodes(G, end_point.x, end_point.y)

        # Находим ближайший узел графа для конечной точки
        end_node = ox.distance.nearest_nodes(G, end_point.x, end_point.y)
        # Строим маршрут
        try:
            new_route = nx.shortest_path(G, current_node, end_node, weight='length')
            routes.append(new_route)

            # Генерируем данные движения
            _point = {'y': G.nodes[current_node]['y'], 'x': G.nodes[current_node]['x']}
            for i, node in enumerate(new_route):
                point = G.nodes[node]
                lat, lon = point['y'], point['x']

                dist = ox.distance.euclidean(_point['y'], _point['x'], point['y'], point['x']) * 10 ** 5
                time_spent = round(dist / speeds[transport] * 3600)
                current_time += timedelta(seconds=time_spent)

                movement_entry = {
                    "latitude": int(lat * 10 ** 6),
                    "longitude": int(lon * 10 ** 6),
                    "timestamp": int(current_time.timestamp())
                }
                movement_data.append(movement_entry)
                _point = point

                current_node = end_node

        except nx.NetworkXNoPath:
            continue

    return routes, movement_data


place = "Россия, Лобня"
female = 1054
male = 1000
rosstat_gender = [male / (female + male), female / (female + male)]

network = 'drive'
graph, G = create_graph(place, network)
nodes = list(G.nodes())
start_time = datetime.now()
output_data = []

factories = [DoctorFactory(), SchoolChildFactory(), OfficeWorkerFactory(), SalesmanFactory()]

for uid in range(10):
    person = random.choice(factories).create()
    print(person.get_name())
    routes, movement_data = generate_track(nodes, place, person.get_places())
    output_data.append({
        "id": uid,
        "track": movement_data,
        "optional_data": {
            "gender": int(numpy.random.choice((0, 1), p=rosstat_gender)),
            "age": random.randint(15, 50),
        },
    })
    visualize_interactive(G, routes, person.get_name(), uid)
    # visualize_png(graph, routes, place, uid)

json_save(output_data)
