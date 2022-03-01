Depth first search:
visited={}
depth={s:0}
parent={s:None}
def dfs(s,adj){
     for v in adj[s]
          if not visited [v]
               visited[v] = true; parent[v]=s;depth[v]=depth[s]+1
                    dfs(v,adj)
}

find shortest path. Breadth first search:
each vertex represents a configuration(permutation) of the cube
the edges represent a move from a particular permutation.
