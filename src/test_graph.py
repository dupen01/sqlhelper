from graph import DagGraph


dg = DagGraph()

# dg.add_node('a')
# dg.add_node('b')
# dg.add_node('c')
# dg.add_node('d')
# dg.add_node('e')
# dg.add_node('f')
# dg.add_node('x')
# dg.add_node('y')

dg.add_edge('a', 'b')
dg.add_edge('a', 'c')
dg.add_edge('a', 'd')
dg.add_edge('d', 'e')
dg.add_edge('e', 'd')
dg.add_edge('b', 'e')
dg.add_edge('x', 'y')

dg.print_related_edges_backward('b')


