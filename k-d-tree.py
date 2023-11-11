from dataclasses import dataclass

@dataclass
class Node:
    point: tuple
    left: 'Node' = None
    right: 'Node' = None
    axis: int = None

@dataclass
class City:
    name: str
    coordinates: tuple
    population: int

def build_kd_tree(points, depth=0):
    if not points:
        return None

    k = len(points[0].coordinates)
    axis = depth % k
    points.sort(key=lambda x: x.coordinates[axis])
    median = len(points) // 2

    return Node(
        point=points[median].coordinates,
        left=build_kd_tree(points[:median], depth + 1),
        right=build_kd_tree(points[median + 1:], depth + 1),
        axis=axis
    )

def distance_squared(point1, point2):
    return sum((a - b) ** 2 for a, b in zip(point1, point2))

def closest_city_in_tree(tree, target, depth=0, best=None):
    if tree is None:
        return best

    k = len(target.coordinates)
    axis = depth % k

    target_point = target.coordinates if isinstance(target, City) else target

    next_best = tree.point if best is None or distance_squared(tree.point, target_point) < distance_squared(best, target_point) else best
    next_branch = tree.left if target_point[axis] < tree.point[axis] else tree.right

    return closest_city_in_tree(next_branch, target, depth + 1, next_best)

def closest_city(tree, target):
    return closest_city_in_tree(tree, target, 0, None)

if __name__ == "__main__":
    cities = [
        City("CityA", (2, 3, 4), 1000000),
        City("CityB", (5, 4, 2), 1500000),
        City("CityC", (9, 6, 1), 800000),
        City("CityD", (4, 7, 8), 1200000),
        City("CityE", (8, 1, 5), 600000),
        City("CityF", (7, 2, 9), 2000000)
    ]

    target_city = City("Target City", (9, 2, 5), 0)  

    city_kdtree = build_kd_tree(cities, depth=0)

    nearest_city = closest_city(city_kdtree, target_city)

    print("Cities:")
    for city in cities:
        print(f"{city.name}: {city.coordinates}, Population: {city.population}")

    print("\nKD Tree:")
    

    print(f"\nClosest city to {target_city.name}: {nearest_city}")
