import math
from itertools import combinations


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth
    given their latitude/longitude, using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in km

    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def build_distance_matrix(treks):
    """
    Given a list of trek objects (each with .latitude and .longitude),
    build a 2D matrix where matrix[i][j] = distance between trek i and trek j.
    """
    n = len(treks)
    matrix = [[0.0] * n for _ in range(n)]

    for i, j in combinations(range(n), 2):
        d = haversine_distance(
            float(treks[i].latitude), float(treks[i].longitude),
            float(treks[j].latitude), float(treks[j].longitude)
        )
        matrix[i][j] = d
        matrix[j][i] = d  # distance is symmetric

    return matrix


def route_distance(route, matrix):
    """Total distance of visiting treks in the given order (list of indices)."""
    return sum(matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))


def nearest_neighbor_route(matrix, start=0):
    """
    Build an initial route by always moving to the closest unvisited trek.
    Fast to compute, but not always optimal on its own.
    """
    n = len(matrix)
    unvisited = set(range(n))
    unvisited.remove(start)
    route = [start]
    current = start

    while unvisited:
        next_stop = min(unvisited, key=lambda j: matrix[current][j])
        route.append(next_stop)
        unvisited.remove(next_stop)
        current = next_stop

    return route


def two_opt(route, matrix):
    """
    Improve a route by repeatedly reversing segments if doing so shortens
    the total distance. This removes "crossings" in the path.
    """
    improved = True
    best_route = route[:]

    while improved:
        improved = False
        for i in range(1, len(best_route) - 1):
            for j in range(i + 1, len(best_route)):
                new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
                if route_distance(new_route, matrix) < route_distance(best_route, matrix):
                    best_route = new_route
                    improved = True

    return best_route


def optimize_route(treks):
    """
    Main entry point. Takes a list of Trek objects (each needs .latitude
    and .longitude set), returns:
      - ordered list of Trek objects (optimized visiting order)
      - total distance in km
    """
    treks = [t for t in treks if t.latitude is not None and t.longitude is not None]

    if len(treks) < 2:
        return treks, 0.0

    matrix = build_distance_matrix(treks)
    initial_route = nearest_neighbor_route(matrix)
    optimized_route = two_opt(initial_route, matrix)

    ordered_treks = [treks[i] for i in optimized_route]
    total_distance = route_distance(optimized_route, matrix)

    return ordered_treks, round(total_distance, 1)
