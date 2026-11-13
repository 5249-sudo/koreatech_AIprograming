import heapq
from math import inf


campus = {
    'A': [('B', 10), ('E', 8), ('D', 20)],
    'B': [('A', 10), ('C', 12), ('F', 6)],
    'C': [('B', 12), ('G', 10)],
    'D': [('A', 20), ('E', 7), ('H', 11)],
    'E': [('A', 8), ('D', 7), ('F', 5), ('H', 9)],
    'F': [('B', 6), ('E', 5), ('G', 4), ('H', 3)],
    'G': [('C', 10), ('F', 4)],
    'H': [('D', 11), ('E', 9), ('F', 3)],
}


def _validate_graph(graph, start):
    """그래프와 시작 정점을 검사하고 잘못된 입력이면 ValueError를 발생시킵니다."""
    if not graph:
        raise ValueError("graph must not be empty")
    if start not in graph:
        raise ValueError("start must be a vertex in graph")
    for edges in graph.values():
        for _, weight in edges:
            if weight < 0:
                raise ValueError("edge weights must be nonnegative")


def dijkstra_array(graph, start):
    """배열 탐색 방식으로 시작점에서 모든 정점까지의 거리와 이전 정점을 구합니다."""
    _validate_graph(graph, start)

    dist = {vertex: inf for vertex in graph}
    prev = {vertex: None for vertex in graph}
    dist[start] = 0
    visited = set()

    while len(visited) < len(graph):
        current = None
        for vertex in graph:
            if vertex not in visited and (
                current is None or dist[vertex] < dist[current]
            ):
                current = vertex

        if current is None or dist[current] == inf:
            break

        visited.add(current)
        for neighbor, weight in graph[current]:
            if neighbor in visited:
                continue
            new_distance = dist[current] + weight
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                prev[neighbor] = current

    return dist, prev


def dijkstra_heap(graph, start):
    """heapq를 사용해 시작점에서 모든 정점까지의 거리와 이전 정점을 구합니다."""
    _validate_graph(graph, start)

    dist = {vertex: inf for vertex in graph}
    prev = {vertex: None for vertex in graph}
    dist[start] = 0
    sequence = 0
    candidates = [(0, sequence, start)]

    while candidates:
        current_distance, _, current = heapq.heappop(candidates)
        if current_distance != dist[current]:
            continue

        for neighbor, weight in graph[current]:
            new_distance = current_distance + weight
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                prev[neighbor] = current
                sequence += 1
                heapq.heappush(candidates, (new_distance, sequence, neighbor))

    return dist, prev

import random


def make_graph(v, degree=6, seed=42, wmax=100):
    """정점 0~v-1의 연결된 무방향 가중 그래프를 만든다."""
    rng = random.Random(seed)
    g = {i: {} for i in range(v)}

    def add(a, b):
        if a == b or b in g[a]:
            return False
        w = rng.randint(1, wmax)
        g[a][b] = g[b][a] = w
        return True

    edges = 0
    for i in range(1, v):
        edges += add(i, rng.randrange(i))

    target = min(
        v * (v - 1) // 2,
        max(v - 1, round(v * degree / 2)),
    )

    while edges < target:
        a, b = rng.randrange(v), rng.randrange(v)
        edges += add(a, b)

    return {u: list(neighbors.items()) for u, neighbors in g.items()}

def build_path(prev, start, end):
    """prev 딕셔너리를 따라 start에서 end까지의 정점 경로를 복원합니다."""
    if start == end:
        return [start]

    path = []
    current = end
    visited = set()
    while current is not None and current not in visited:
        visited.add(current)
        path.append(current)
        if current == start:
            return path[::-1]
        current = prev.get(current)

    return []
