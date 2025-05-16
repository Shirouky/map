import matplotlib.pyplot as plt
import folium
import osmnx as ox


def visualize_png(graph, routes, place, uid):
    route = []
    for r in routes:
        route += r
    ox.plot_graph_route(
        graph,
        route,
        route_color='red',
        route_linewidth=4,
        node_size=0,
        bgcolor='white',
        show=False,
        close=False
    )
    plt.title(f"Маршрут перемещения в {place} человека с uid {uid}")
    plt.savefig("route_plot.png")
    plt.show()


def visualize_interactive(G, routes, name, uid):
    # Интерактивная карта с folium (открывается в браузере)
    print("\nСоздание интерактивной карты (folium)...")
    # Создаем карту с центром в первой точке маршрута
    m = folium.Map(
        location=(G.nodes[routes[0][0]]['y'], G.nodes[routes[0][0]]['x']),
        zoom_start=14,
        tiles="OpenStreetMap"
    )

    for route in routes:
        # Получаем координаты всех точек маршрута
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

        # Добавляем линию маршрута
        folium.PolyLine(
            route_coords,
            color="red",
            weight=5,
            opacity=0.8
        ).add_to(m)

        # Добавляем маркеры
        folium.Marker(
            route_coords[0],
            icon=folium.Icon(color="green")
        ).add_to(m)

    # Сохраняем HTML с картой
    m.save(f"interactive_route_{name}_{uid}.html")
    print("Интерактивная карта сохранена в interactive_route.html")
