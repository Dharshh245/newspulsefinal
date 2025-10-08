from typing import Iterable, List


def flatten(list_of_lists: Iterable[Iterable]) -> List:
	return [item for sub in list_of_lists for item in sub]


def chunk_list(items: List, chunk_size: int) -> List[List]:
	return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]

