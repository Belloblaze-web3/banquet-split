# BanquetSplit

The input relationships form a tree. For each query `(X, Y)`, add a relationship between `X` and `Y` and determine whether everyone can still be divided between two banquets so that connected people are separated.

## Key observations

A tree is bipartite, so a two-coloring can be computed with DFS.

- If `X` and `Y` have different colors, their tree path has odd length. The added edge creates an even cycle, so the answer is `Yes`.
- If they have the same color, the added edge creates an odd cycle. It is impossible without removing a relationship. Removing any one edge from that cycle works, so the minimum is `1`, and the number of choices is the cycle length.

The cycle length is `distance(X, Y) + 1`. Binary lifting is used to answer LCA and distance queries efficiently.

## Complexity

- Preprocessing: `O(N log N)`
- Each query: `O(log N)`
- Total: `O((N + Q) log N)`

## Run

```bash
python3 banquet_split.py < input.txt
```

### Sample input

```text
1
5
1 2
1 3
3 4
3 5
2
2 4
1 5
```

### Sample output

```text
Yes
No
1 3
```
