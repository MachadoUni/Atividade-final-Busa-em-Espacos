import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0

        for index, tile in enumerate(state.tiles):

            if tile == 0:
                continue

            current_row = index // 3
            current_col = index % 3

            goal_index = tile - 1

            goal_row = goal_index // 3
            goal_col = goal_index % 3

            distance += abs(current_row - goal_row)
            distance += abs(current_col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        tie_breaker = count()

        frontier = []

        best_cost = {initial: initial.cost}

        # Adiciona o estado inicial
        initial_f = initial.cost + self.heuristic(initial)

        heapq.heappush(
            frontier,
            (initial_f, next(tie_breaker), initial)
        )

        # Estatísticas
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:

            _, _, current = heapq.heappop(frontier)

            if current.cost > best_cost[current]:
                continue

            # Verifica se encontramos a solução
            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost
                )

            nodes_expanded += 1

            for neighbor in current.neighbors():

                new_cost = neighbor.cost

                if neighbor not in best_cost or new_cost < best_cost[neighbor]:

                    best_cost[neighbor] = new_cost

                    priority = new_cost + self.heuristic(neighbor)

                    heapq.heappush(
                        frontier,
                        (priority, next(tie_breaker), neighbor)
                    )

                    nodes_generated += 1

            max_frontier_size = max(
                max_frontier_size,
                len(frontier)
            )

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
