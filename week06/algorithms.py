from bisect import bisect_left
import heapq
from unittest import result


def linear_search(scores, target):
	"""점수 목록을 순차 탐색해 target의 첫 인덱스를 반환합니다."""
	for index in range(len(scores)):
		if scores[index] == target:
			return index
	return -1


def binary_search(scores, target):
	"""오름차순 점수 목록을 이진 탐색해 target의 첫 인덱스를 반환합니다."""
	left = 0
	right = len(scores) - 1
	first_index = -1

	while left <= right:
		middle = (left + right) // 2
		if scores[middle] == target:
			first_index = middle
			right = middle - 1
		elif scores[middle] < target:
			left = middle + 1
		else:
			right = middle - 1

	return first_index


def bubble_sort(nums):
	"""인접한 원소를 비교하고 교환해 새 오름차순 리스트를 반환합니다."""
	result = nums[:]
	for end in range(len(result) - 1, 0, -1):
		swapped = False
		for index in range(end):
			if result[index] > result[index + 1]:
				result[index], result[index + 1] = result[index + 1], result[index]
				swapped = True
		if not swapped:
			break
	return result


def cocktail_sort(nums):
	"""양방향으로 인접 원소를 교환하며 새 오름차순 리스트를 반환합니다."""
	result = nums[:]
	left = 0
	right = len(result) - 1
	while left < right:
		swapped = False
		for index in range(left, right):
			if result[index] > result[index + 1]:
				result[index], result[index + 1] = result[index + 1], result[index]
				swapped = True
		right -= 1
		if not swapped:
			break
		swapped = False
		for index in range(right, left, -1):
			if result[index - 1] > result[index]:
				result[index - 1], result[index] = result[index], result[index - 1]
				swapped = True
		left += 1
		if not swapped:
			break
	return result


def insertion_sort(nums):
	"""각 원소를 정렬된 앞부분의 알맞은 위치에 삽입해 반환합니다."""
	result = nums[:]
	for index in range(1, len(result)):
		value = result[index]
		position = index - 1
		while position >= 0 and result[position] > value:
			result[position + 1] = result[position]
			position -= 1
		result[position + 1] = value
	return result


def patience_sort(nums):
	"""카드 더미를 만든 뒤 최소 힙으로 병합해 새 오름차순 리스트를 반환합니다."""
	piles = []
	pile_tops = []
	for value in nums:
		pile_index = bisect_left(pile_tops, value)
		if pile_index == len(piles):
			piles.append([])
			pile_tops.append(value)
		else:
			pile_tops[pile_index] = value
		piles[pile_index].append(value)

	heap = []
	for pile_index in range(len(piles)):
		value = piles[pile_index].pop()
		heapq.heappush(heap, (value, pile_index))

	result = []
	while heap:
		value, pile_index = heapq.heappop(heap)
		result.append(value)
		if piles[pile_index]:
			next_value = piles[pile_index].pop()
			heapq.heappush(heap, (next_value, pile_index))
	return result


def pancake_sort(nums):
	"""접두 구간을 뒤집어 최댓값을 제자리에 옮기며 새 리스트를 반환합니다."""
	result = nums[:]
	for end in range(len(result) - 1, 0, -1):
		max_index = 0
		for index in range(1, end + 1):
			if result[index] > result[max_index]:
				max_index = index
		if max_index != end:
			left = 0
			right = max_index
			while left < right:
				result[left], result[right] = result[right], result[left]
				left += 1
				right -= 1
			left = 0
			right = end
			while left < right:
				result[left], result[right] = result[right], result[left]
				left += 1
				right -= 1
	return result

def find_duplicates(items):
    '''중복해서 나타나는 값들을 찾아 반환합니다.'''
    result = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in result:
                result.append(items[i])
    return result


def find_duplicates_fast(items):
	"""두 번 이상 나타난 값을 처음 등장한 순서대로 한 번씩 반환합니다."""
	seen = set()
	duplicates = set()

	for item in items:
		if item in seen:
			duplicates.add(item)
		else:
			seen.add(item)

	result = []
	added = set()
	for item in items:
		if item in duplicates and item not in added:
			result.append(item)
			added.add(item)

	return result

