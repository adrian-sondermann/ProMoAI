from collections import deque

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as pn_util


def get_simplified_reachability_graph(net: PetriNet) -> dict[PetriNet.Transition, set[PetriNet.Transition]]:
    graph: dict[PetriNet.Transition, set[PetriNet.Transition]] = {node: set() for node in net.transitions}
    for start_node in graph.keys():
        reachable: set[PetriNet.Transition] = set()
        queue: deque[PetriNet.Transition] = deque()
        queue.append(start_node)
        while queue:
            node = queue.popleft()
            if node not in reachable:
                reachable.add(node)
                successors = pn_util.post_set(node)
                queue.extend(successors)
        graph[start_node].update(reachable)
    return graph


def get_reachable_transitions_from_place_to_another(
    start_place: PetriNet.Place, end_place: PetriNet.Place
) -> set[PetriNet.Transition]:
    visited: set[PetriNet.Place | PetriNet.Transition] = set()
    queue: deque[PetriNet.Place | PetriNet.Transition] = deque()
    queue.append(start_place)
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            if node == end_place:
                continue
            successors = pn_util.post_set(node)
            queue.extend(successors)
    visited = {node for node in visited if isinstance(node, PetriNet.Transition)}
    return visited
