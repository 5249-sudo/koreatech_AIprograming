import heapq
from math import inf


def min_coins_dp(coins, amount):
	"""주어진 액면으로 amount를 만드는 최소 동전 개수를 반환합니다.

	각 액면의 동전을 제한 없이 사용할 수 있습니다. 만들 수 없는 금액이면
	-1을 반환하며, coins는 변경하지 않습니다.
	"""
	unreachable = amount + 1
	minimum_coins = [unreachable] * (amount + 1)
	minimum_coins[0] = 0

	for coin in coins:
		for current_amount in range(coin, amount + 1):
			minimum_coins[current_amount] = min(
				minimum_coins[current_amount],
				minimum_coins[current_amount - coin] + 1,
			)

	if minimum_coins[amount] == unreachable:
		return -1
	return minimum_coins[amount]


def min_coins_greedy(coins, amount):
	"""큰 액면부터 사용해 amount를 만드는 동전 개수를 반환합니다.

	각 액면의 동전을 제한 없이 사용할 수 있습니다. 만들 수 없는 금액이면
	-1을 반환하며, coins는 변경하지 않습니다.
	"""
	coin_count = 0
	remaining = amount

	for coin in sorted(coins, reverse=True):
		coin_count += remaining // coin
		remaining %= coin

	if remaining != 0:
		return -1
	return coin_count


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
	"""heapq로 시작점에서 모든 정점까지의 거리와 이전 정점을 구합니다."""
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

