import sys
from array import array


def integers(data):
    """Yield integers without creating a large list of Python int objects."""
    number = 0
    sign = 1
    in_number = False

    for byte in data:
        if 48 <= byte <= 57:
            number = number * 10 + byte - 48
            in_number = True
        elif byte == 45:
            sign = -1
        elif in_number:
            yield sign * number
            number = 0
            sign = 1
            in_number = False

    if in_number:
        yield sign * number


def solve():
    data = sys.stdin.buffer.read()
    it = integers(data)
    t = next(it)
    output = []

    for _ in range(t):
        n = next(it)

        # Compact forward-star adjacency representation.
        head = array('i', [-1]) * n
        to = array('i')
        next_edge = array('i')

        def add_edge(u, v):
            to.append(v)
            next_edge.append(head[u])
            head[u] = len(to) - 1

        for _ in range(n - 1):
            u = next(it) - 1
            v = next(it) - 1
            add_edge(u, v)
            add_edge(v, u)

        # Root the tree, compute depths and the bipartite color.
        parent = array('i', [-1]) * n
        depth = array('i', [0]) * n
        color = bytearray(n)
        parent[0] = 0
        stack = [0]

        while stack:
            u = stack.pop()
            edge = head[u]
            while edge != -1:
                v = to[edge]
                if parent[v] == -1:
                    parent[v] = u
                    depth[v] = depth[u] + 1
                    color[v] = color[u] ^ 1
                    stack.append(v)
                edge = next_edge[edge]

        # Binary-lifting table for LCA queries.
        max_log = n.bit_length()
        jumps = [parent]
        for _ in range(1, max_log):
            previous = jumps[-1]
            current = array('i', [0]) * n
            for v in range(n):
                current[v] = previous[previous[v]]
            jumps.append(current)

        q = next(it)
        for _ in range(q):
            x = next(it) - 1
            y = next(it) - 1

            if color[x] != color[y]:
                output.append("Yes")
                continue

            original_x, original_y = x, y
            distance = depth[x] + depth[y]

            if depth[x] < depth[y]:
                x, y = y, x

            difference = depth[x] - depth[y]
            bit = 0
            while difference:
                if difference & 1:
                    x = jumps[bit][x]
                difference >>= 1
                bit += 1

            if x != y:
                for bit in range(max_log - 1, -1, -1):
                    if jumps[bit][x] != jumps[bit][y]:
                        x = jumps[bit][x]
                        y = jumps[bit][y]
                lca = jumps[0][x]
            else:
                lca = x

            distance -= 2 * depth[lca]
            cycle_length = distance + 1
            output.append(f"No\n1 {cycle_length}")

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    solve()
