class NodeNotFoundException(Exception):
    pass


class NodeExitsException(Exception):
    pass


class DagGraph:
    def __init__(self, nodes: list=[]) -> None:
        self.__nodes = []
        self.__edges = []
        if nodes:
            for node in nodes:
                self.__nodes.append(node)


    def add_node(self, node: str) -> None:
        if node in self.__nodes:
            raise NodeExitsException(f"节点已存在:{node}")
        self.__nodes.append(node)

    
    def remove_node(self, node: str) -> None:
        if node not in self.__nodes:
            raise NodeNotFoundException(f"节点不存在:{node}")
        self.__nodes.remove(node)


    def add_edge(self, _from, _to) -> None:
        # if _from not in self.__nodes:
        #     raise NodeNotFoundException(f"节点不存在:{_from}")
        # if _to not in self.__nodes:
        #     raise NodeNotFoundException(f"节点不存在:{_to}")
        self.__edges.append((_from, _to))
    

    def remove_edge(self, _from, _to):
        if _from not in self.__nodes:
            raise NodeNotFoundException(f"节点不存在:{_from}")
        if _to not in self.__nodes:
            raise NodeNotFoundException(f"节点不存在:{_to}")
        self.__edges.remove((_from, _to))


    def get_nodes(self) -> list:
        return sorted(list(set(self.__nodes)))
    

    def get_edges(self) -> list:
        return list(set(self.__edges))


    def __print_mermaid(self, edges: list) -> None:
        edges = list(set(edges))
        print('graph LR')
        for _from, _to in edges:
            print(f"{_from} --> {_to}")


    def print_all_edges(self):
        self.__print_mermaid(self.__edges)


    def find_related_edges_backward(self, node):
        # 创建一个队列和一个集合来记录已访问过的关系
        from collections import deque
        queue = deque([node])
        visited = set()
        all_relations = []
        while queue:
            current = queue.popleft()
            # 找到当前元素相关的所有直接关系
            direct_relations = [rel for rel in self.__edges if current in rel]
            all_relations.extend(direct_relations)
            # 将未访问过的直接关系中的元素加入队列
            for rel in direct_relations:
                neighbor = rel[0] if rel[1] == current else rel[1]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return list(set(all_relations))
    

    def print_related_edges_backward(self, node):
        related_edges = self.find_related_edges_backward(node=node)
        self.__print_mermaid(related_edges)
