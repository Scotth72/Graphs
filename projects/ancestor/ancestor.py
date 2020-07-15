
from collections import deque


def earliest_ancestor(ancestors, starting_node):
    child_parent_rel = dict()

    for relation in ancestors:
        child = relation[1]
        parent = relation[0]

        if child not in child_parent_rel:
            child_parent_rel[child] = [parent]

        else:
            child_parent_rel[child] = [*child_parent_rel[child], parent]

    node = starting_node
    dq = deque()
    dq.append(node)

   # sort the array in reverse
   # pops the parent first
   # leaves the smaller node

    while len(dq) > 0:
        node = dq.popleft()
        if node in child_parent_rel:
            child_parent_rel[node].sort(reverse=True)

            for next_node in child_parent_rel[node]:
                dq.append(next_node)

    # check if has parent
    if node == starting_node:
        return -1
    else:
        return node
