# https://en.wikipedia.org/wiki/Blossom_algorithm
def get_maximum_matching(graph, matching):
    augmenting_path = get_augmenting_path(graph, matching)
    if len(augmenting_path) > 0:
        return get_maximum_matching(graph, matching.augment(augmenting_path))
    else:
        return matching

# https://en.wikipedia.org/wiki/Blossom_algorithm
def get_augmenting_path(graph, matching):
    forest = Forest()
    graph.unmark_all_edges()
    graph.mark_edges(matching.get_edges())
    for exposed_vertice in matching.get_exposed_vertices():
        forest.add_singleton_tree(exposed_vertice)
    v = forest.get_unmarked_even_vertice()
    while v is not None:
        e = graph.get_unmarked_neighboring_edge(v)
        while e is not None:
            _, w = e
            if not forest.does_contain_vertice(w):
                x = matching.get_matched_vertice(w)
                forest.add_edge((v, w))
                forest.add_edge((w, x))
            else:
                if forest.get_distance_to_root(w) % 2 != 0:
                    pass
                else:
                    if forest.get_root(v) != forest.get_root(w):
                        path = forest.get_path_from_root_to(v) + forest.get_path_to_root_from(w)
                        return path
                    else:
                        blossom = forest.get_blossom(v, w)
                        graph_prime = graph.contract(blossom)
                        matching_prime = matching.contract(blossom)
                        path_prime = get_augmenting_path(graph_prime, matching_prime)
                        path = graph.lift_path(path_prime, blossom)
                        return path
            graph.mark_edge(e)
            e = graph.get_unmarked_neighboring_edge(v)
        forest.mark_vertice(v)
        v = forest.get_unmarked_even_vertice()
    return []

class Graph:

    def __init__(self):
        self.adjacency = {}
        self.unmarked_adjacency = {}
        self.__assert_representation()

    def __assert_representation(self):
        for t in self.adjacency:
            assert len(self.adjacency[t]) > 0, 'If vertice exists in adjacency matrix, it must have at least one neighbor'
            for u in self.adjacency[t]:
                self.__assert_edge_exists((t, u))
        for t in self.unmarked_adjacency:
            assert len(self.unmarked_adjacency[t]) > 0, 'If vertice exists in unmarked adjacency matrix, it must have at least one neighbor'
            for u in self.unmarked_adjacency[t]:
                self.__assert_edge_exists((t, u))
                self.__assert_unmarked_edge_exists((t, u))

    def __assert_edge_exists(self, edge):
        v, w = edge
        assert (v in self.adjacency) and (w in self.adjacency[v]), 'Edge must exist in adjacency matrix'
        assert (w in self.adjacency) and (v in self.adjacency[w]), 'Reciprocal edge must exist in adjacency matrix'

    def __assert_edge_does_not_exist(self, edge):
        v, w = edge
        assert (v not in self.adjacency) or (w not in self.adjacency[v]), 'Edge must not exist in adjacency matrix'
        assert (w not in self.adjacency) or (v not in self.adjacency[w]), 'Reciprocal edge must not exist in adjacency matrix'

    def __assert_unmarked_edge_exists(self, edge):
        v, w = edge
        assert (v in self.unmarked_adjacency) and (w in self.unmarked_adjacency[v]), 'Edge must exist in unmarked adjacency matrix'
        assert (w in self.unmarked_adjacency) and (v in self.unmarked_adjacency[w]), 'Reciprocal edge must exist in unmarked adjacency matrix'

    def __assert_unmarked_edge_does_not_exist(self, edge):
        v, w = edge
        assert (v not in self.unmarked_adjacency) or (w not in self.unmarked_adjacency[v]), 'Edge must not exist in unmarked adjacency matrix'
        assert (w not in self.unmarked_adjacency) or (v not in self.unmarked_adjacency[w]), 'Reciprocal edge must not exist in unmarked adjacency matrix'

    def __assert_vertice_exists(self, vertice):
        assert vertice in self.adjacency, 'Vertice must exist in adjacency matrix'

    def __assert_vertice_does_not_exist(self, vertice):
        assert vertice not in self.adjacency, 'Vertice must not exist in adjacency matrix'
        assert vertice not in self.unmarked_adjacency, 'Vertice must not exist in unmarked adjacency matrix'

    def copy(self):
        self.__assert_representation()
        graph = Graph()
        for t in self.adjacency:
            graph.adjacency[t] = set()
            for u in self.adjacency[t]:
                graph.adjacency[t].add(u)
        for t in self.unmarked_adjacency:
            graph.unmarked_adjacency[t] = set()
            for u in self.unmarked_adjacency[t]:
                graph.unmarked_adjacency[t].add(u)
        graph.__assert_representation()
        return graph

    def add_edge(self, edge):
        self.__assert_edge_does_not_exist(edge)
        self.__assert_unmarked_edge_does_not_exist(edge)
        v, w = edge
        if v not in self.adjacency:
            self.adjacency[v] = set()
        self.adjacency[v].add(w)
        if w not in self.adjacency:
            self.adjacency[w] = set()
        self.adjacency[w].add(v)
        if v not in self.unmarked_adjacency:
            self.unmarked_adjacency[v] = set()
        self.unmarked_adjacency[v].add(w)
        if w not in self.unmarked_adjacency:
            self.unmarked_adjacency[w] = set()
        self.unmarked_adjacency[w].add(v)
        self.__assert_representation()

    def unmark_all_edges(self):
        self.unmarked_adjacency = {}
        for t in self.adjacency:
            self.unmarked_adjacency[t] = set()
            for u in self.adjacency[t]:
                self.unmarked_adjacency[t].add(u)
        self.__assert_representation()

    def mark_edges(self, edges):
        for edge in edges:
            self.mark_edge(edge)
        self.__assert_representation()

    def mark_edge(self, edge):
        self.__assert_edge_exists(edge)
        self.__assert_unmarked_edge_exists(edge)
        v, w = edge
        self.unmarked_adjacency[v].remove(w)
        if len(self.unmarked_adjacency[v]) == 0:
            del self.unmarked_adjacency[v]
        self.unmarked_adjacency[w].remove(v)
        if len(self.unmarked_adjacency[w]) == 0:
            del self.unmarked_adjacency[w]
        self.__assert_representation()

    def get_unmarked_neighboring_edge(self, vertice):
        self.__assert_representation()
        if vertice in self.unmarked_adjacency:
            return vertice, next(iter(self.unmarked_adjacency[vertice]))
        else:
            return None
    
    def get_vertices(self):
        self.__assert_representation()
        return self.adjacency.keys()

    def contract(self, blossom):
        graph = self.copy()
        graph.__assert_vertice_does_not_exist(blossom.get_id())
        graph.adjacency[blossom.get_id()] = set()
        for t in blossom.get_vertices():
            graph.__assert_vertice_exists(t)
            for u in graph.adjacency[t]:
                graph.__assert_edge_exists((t, u))
                graph.adjacency[u].remove(t)
                if u != blossom.get_id():
                    graph.adjacency[blossom.get_id()].add(u)
                    graph.adjacency[u].add(blossom.get_id())
            del graph.adjacency[t]
        if len(graph.adjacency[blossom.get_id()]) == 0:
            # Required to maintain invariant
            del graph.adjacency[blossom.get_id()]
        graph.unmark_all_edges()
        graph.__assert_representation()
        return graph

    def lift_path(self, path, blossom):
        self.__assert_representation()
        if len(path) == 0:
            return path
        if len(path) == 1:
            assert False, 'A path cannot contain exactly one vertice'
        if path[0] == blossom.get_id():

            ############################################################################################################
            # LEFT ENDPOINT
            ############################################################################################################

            #  ,-o                    #    b                    #    o--,                
            # |      b  o--o  o--o  o #        o  o--o  o--o  o #        o  o--o  o--o  o
            # o                       # o      |                # b                      
            #        o                # |      o                #        o               
            #    o--'                 #  `-o                    #    o--'                

            #  ,-o                    #    o--,                
            # |      o  o--o  o--o  o #        o  o--o  o--o  o
            # o      |                # o                      
            #        o                # |      b               
            #    b                    #  `-o                   

            w = path[1]
            blossom_path = []
            for v in blossom.traverse_left():
                blossom_path.append(v)
                if (w in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                    return blossom_path + path[1:]
            blossom_path = []
            for v in blossom.traverse_right():
                blossom_path.append(v)
                if (w in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                    return blossom_path + path[1:]
            assert False, 'At least one path with even edges must exist through the blossom'
        if path[-1] == blossom.get_id():

            ############################################################################################################
            # RIGHT ENDPOINT
            ############################################################################################################

            #                    o-.  #                    b    #                 ,--o   
            # o  o--o  o--o  b      | # o  o--o  o--o  o        # o  o--o  o--o  o       
            #                       o #                |      o #                       b
            #                o        #                o      | #                o       
            #                 `--o    #                    o-'  #                 `--o   

            #                    o-.  #                 ,--o   
            # o  o--o  o--o  o      | # o  o--o  o--o  o       
            #                |      o #                       o
            #                o        #                b      |
            #                    b    #                    o-' 

            u = path[-2]
            blossom_path = []
            for v in blossom.traverse_left():
                blossom_path.append(v)
                if (u in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                    return path[:-1] + list(reversed(blossom_path))
            blossom_path = []
            for v in blossom.traverse_right():
                blossom_path.append(v)
                if (u in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                    return path[:-1] + list(reversed(blossom_path))
            assert False, 'At least one path with even edges must exist through the blossom'
        for i, v in enumerate(path):
            if v == blossom.get_id():
                u, w = path[i-1], path[i+1]
                if u in self.adjacency[blossom.get_base()]:

                    ####################################################################################################
                    # INTERIOR LEFT-ORIENTED BLOSSOM
                    ####################################################################################################

                    #            o     #                         #                         #          o--,  
                    #                  #                         #                         #              o
                    #            o     #                         #                         # o  o--b        
                    #            |     #          o--,           #          o--,           #              o 
                    #            o     #              o  o--o  o #              o          #          o--'  
                    #                  # o  o--b                 # o  o--b                 #                
                    #            o--,  #              o          #              o  o--o  o #          o     
                    #                o #          o--'           #          o--'           #          |     
                    #   o  o--b        #                         #                         #          o    
                    #                o #                         #                         #               
                    #            o--'  #                         #                         #          o    

                    blossom_path = []
                    for v in blossom.traverse_left():
                        blossom_path.append(v)
                        if (w in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                            return path[:i] + blossom_path + path[i+1:]
                    blossom_path = []
                    for v in blossom.traverse_right():
                        blossom_path.append(v)
                        if (w in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                            return path[:i] + blossom_path + path[i+1:]
                    assert False, 'At least one path with even edges must exist through the blossom'
                elif w in self.adjacency[blossom.get_base()]:

                    ####################################################################################################
                    # INTERIOR RIGHT-ORIENTED BLOSSOM
                    ####################################################################################################

                    #       o          #                         #                         #  ,--o         
                    #                  #                         #                         # o             
                    #       o          #                         #                         #        b--o  o
                    #       |          #           ,--o          #           ,--o          # o             
                    #       o          # o  o--o  o              #          o              #  `--o         
                    #                  #                 b--o  o #                 b--o  o #               
                    #    ,--o          #          o              # o  o--o  o              #     o         
                    #   o              #           `--o          #           `--o          #     |         
                    #          b--o  o #                         #                         #     o         
                    #   o              #                         #                         #               
                    #    `--o          #                         #                         #     o         

                    blossom_path = []
                    for v in blossom.traverse_left():
                        blossom_path.append(v)
                        if (u in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                            return path[:i] + list(reversed(blossom_path)) + path[i+1:]
                    blossom_path = []
                    for v in blossom.traverse_right():
                        blossom_path.append(v)
                        if (u in self.adjacency[v]) and (len(blossom_path) % 2 != 0):
                            return path[:i] + list(reversed(blossom_path)) + path[i+1:]
                    assert False, 'At least one path with even edges must exist through the blossom'
                else:
                    assert False, 'Exactly one side of the path must be incident to the base of the blossom'
        return path

class Matching:

    def __init__(self):
        self.adjacency = {}
        self.edges = set()
        self.exposed_vertices = set()
        self.__assert_representation()

    def __assert_representation(self):
        for t in self.adjacency:
            self.__assert_vertice_exists(t)
            if len(self.adjacency[t]) == 0:
                self.__assert_vertice_is_exposed(t)
            else:
                self.__assert_vertice_is_not_exposed(t)
                u = next(iter(self.adjacency[t]))
                self.__assert_edge_exists(tuple(sorted((t, u))))
                self.__assert_vertice_is_not_exposed(u)

    def __assert_edge_exists(self, edge):
        v, w = edge
        assert (v in self.adjacency) and (w in self.adjacency[v]), 'Edge must exist in adjacency matrix'
        assert (w in self.adjacency) and (v in self.adjacency[w]), 'Reciprocal edge must exist in adjacency matrix'
        assert edge in self.edges, 'Edge must exist in edges set'

    def __assert_edge_does_not_exist(self, edge):
        v, w = edge
        assert (v not in self.adjacency) or (w not in self.adjacency[v]), 'Edge must not exist in adjacency matrix'
        assert (w not in self.adjacency) or (v not in self.adjacency[w]), 'Reciprocal edge must not exist in adjacency matrix'
        assert edge not in self.edges, 'Edge must not exist in edges set'

    def __assert_vertice_is_exposed(self, vertice):
        assert vertice in self.adjacency, 'Vertice must exist in adjacency matrix'
        assert vertice in self.exposed_vertices, 'Vertice must exist in exposed vertices set'
        assert len(self.adjacency[vertice]) == 0, 'Vertice must have no neighbors'

    def __assert_vertice_is_not_exposed(self, vertice):
        assert vertice in self.adjacency, 'Vertice must exist in adjacency matrix'
        assert vertice not in self.exposed_vertices, 'Vertice must not exist in exposed vertices set'
        assert len(self.adjacency[vertice]) == 1, 'Vertice must have exactly one neighbor'

    def __assert_vertice_exists(self, vertice):
        assert vertice in self.adjacency, 'Vertice must exist in adjacency matrix'
        if vertice in self.exposed_vertices:
            assert len(self.adjacency[vertice]) == 0, 'If vertice is exposed, it must have no neighbors'
        else:
            assert len(self.adjacency[vertice]) == 1, 'If vertice is not exposed, it must have exactly one neighbor'

    def __assert_vertice_does_not_exist(self, vertice):
        assert vertice not in self.adjacency, 'Vertice must not exist in adjacency matrix'
        assert vertice not in self.exposed_vertices, 'Vertice must not be exposed'

    def copy(self):
        self.__assert_representation()
        matching = Matching()
        for t in self.adjacency.keys():
            matching.adjacency[t] = set()
            for u in self.adjacency[t]:
                matching.adjacency[t].add(u)
        for e in self.edges:
            matching.edges.add(e)
        for u in self.exposed_vertices:
            matching.exposed_vertices.add(u)
        matching.__assert_representation()
        return matching

    def augment(self, path):
        matching = self.copy()
        matching.__assert_vertice_is_exposed(path[0])
        matching.__assert_vertice_is_exposed(path[-1])
        matching.exposed_vertices.remove(path[0])
        matching.exposed_vertices.remove(path[-1])
        for i in range(len(path)-1):
            v, w = path[i], path[i+1]
            edge = tuple(sorted((v, w)))
            if edge in matching.edges:
                matching.__assert_edge_exists(edge)
                matching.edges.remove(edge)
                matching.adjacency[v].remove(w)
                matching.adjacency[w].remove(v)
            else:
                matching.__assert_edge_does_not_exist(edge)
                matching.edges.add(edge)
                matching.adjacency[v].add(w)
                matching.adjacency[w].add(v)
        matching.__assert_representation()
        return matching

    def get_edges(self):
        self.__assert_representation()
        return self.edges

    def get_exposed_vertices(self):
        self.__assert_representation()
        return self.exposed_vertices

    def get_matched_vertice(self, vertice):
        self.__assert_representation()
        self.__assert_vertice_is_not_exposed(vertice)
        return next(iter(self.adjacency[vertice]))

    def add_vertices(self, vertices):
        for vertice in vertices:
            self.add_vertice(vertice)
        self.__assert_representation()

    def add_vertice(self, vertice):
        self.__assert_vertice_does_not_exist(vertice)
        self.adjacency[vertice] = set()
        self.exposed_vertices.add(vertice)
        self.__assert_representation()

    def contract(self, blossom):
        matching = self.copy()
        matching.__assert_vertice_does_not_exist(blossom.get_id())
        matching.adjacency[blossom.get_id()] = set()
        if blossom.get_base() in matching.exposed_vertices:
            matching.exposed_vertices.add(blossom.get_id())
        for t in blossom.get_vertices():
            matching.__assert_vertice_exists(t)
            for u in matching.adjacency[t]:
                e = tuple(sorted((t, u)))
                matching.__assert_edge_exists(e)
                matching.edges.remove(e)
                matching.adjacency[u].remove(t)
                if u != blossom.get_id():
                    matching.edges.add(tuple(sorted((blossom.get_id(), u))))
                    matching.adjacency[blossom.get_id()].add(u)
                    matching.adjacency[u].add(blossom.get_id())
            del matching.adjacency[t]
            matching.exposed_vertices.discard(t)
        matching.__assert_representation()
        return matching

class Forest:

    def __init__(self):
        self.roots = {}
        self.distances_to_root = {}
        self.unmarked_even_vertices = set()
        self.parents = {}
        self.__assert_representation()

    def __assert_representation(self):
        for vertice in self.roots:
            self.__assert_vertice_exists(vertice)
        assert self.roots.keys() == self.distances_to_root.keys(), 'Roots and distances to root must have same keys'
        assert self.roots.keys() == self.parents.keys(), 'Roots and parents mut have same keys'
        for vertice in self.unmarked_even_vertices:
            self.__assert_vertice_exists(vertice)
            assert self.distances_to_root[vertice] % 2 == 0, 'Unmarked even vertice must have even distance to root'

    def __assert_vertice_exists(self, vertice):
        assert vertice in self.roots, 'Vertice must have a root'
        assert vertice in self.distances_to_root, 'Vertice must have a distance to root'
        assert vertice in self.parents, 'Vertice must have a parent'

    def __assert_vertice_does_not_exist(self, vertice):
        assert vertice not in self.roots, 'Vertice must not have a root'
        assert vertice not in self.distances_to_root, 'Vertice must not have a distance to root'
        assert vertice not in self.unmarked_even_vertices, 'Vertice must not exist in unmarked even vertices set'
        assert vertice not in self.parents, 'Vertice must not have a parent'

    def add_singleton_tree(self, vertice):
        self.__assert_vertice_does_not_exist(vertice)
        self.roots[vertice] = vertice
        self.distances_to_root[vertice] = 0
        self.unmarked_even_vertices.add(vertice)
        self.parents[vertice] = vertice
        self.__assert_representation()

    def get_unmarked_even_vertice(self):
        self.__assert_representation()
        if len(self.unmarked_even_vertices) > 0:
            return next(iter(self.unmarked_even_vertices))
        else:
            return None

    def mark_vertice(self, vertice):
        self.__assert_vertice_exists(vertice)
        if self.distances_to_root[vertice] % 2 == 0:
            assert vertice in self.unmarked_even_vertices, 'If vertice has an even distance to root, it must exist in unmarked even vertices set'
            self.unmarked_even_vertices.remove(vertice)
        self.__assert_representation()

    def does_contain_vertice(self, vertice):
        self.__assert_representation()
        return vertice in self.roots

    def add_edge(self, edge):
        v, w = edge
        if v not in self.roots:
            self.__assert_vertice_does_not_exist(v)
            self.__assert_vertice_exists(w)
            self.roots[v] = self.roots[w]
            self.distances_to_root[v] = 1 + self.distances_to_root[w]
            if self.distances_to_root[v] % 2 == 0:
                self.unmarked_even_vertices.add(v)
            self.parents[v] = w
        elif w not in self.roots:
            self.__assert_vertice_does_not_exist(w)
            self.__assert_vertice_exists(v)
            self.roots[w] = self.roots[v]
            self.distances_to_root[w] = 1 + self.distances_to_root[v]
            if self.distances_to_root[w] % 2 == 0:
                self.unmarked_even_vertices.add(w)
            self.parents[w] = v
        else:
            assert False, 'At least one incident vertice must not already exist'
        self.__assert_representation()

    def get_distance_to_root(self, vertice):
        self.__assert_representation()
        self.__assert_vertice_exists(vertice)
        return self.distances_to_root[vertice]

    def get_root(self, vertice):
        self.__assert_representation()
        self.__assert_vertice_exists(vertice)
        return self.roots[vertice]

    def get_path_from_root_to(self, vertice):
        self.__assert_representation()
        return list(reversed(self.get_path_to_root_from(vertice)))

    def get_path_to_root_from(self, vertice):
        self.__assert_representation()
        self.__assert_vertice_exists(vertice)
        root = self.roots[vertice]
        path = []
        parent = vertice
        while parent != root:
            path.append(parent)
            parent = self.parents[parent]
        path.append(root)
        assert len(set(path)) == len(path), 'Path to root must not contain any duplicate vertices'
        return path

    def get_blossom(self, v, w):
        self.__assert_representation()
        v_path = self.get_path_to_root_from(v)
        w_path = self.get_path_to_root_from(w)
        w_ancestors = set(w_path)
        v_blossom_vertices = []
        common_ancestor = None
        for u in v_path:
            if u in w_ancestors:
                common_ancestor = u
                break
            else:
                v_blossom_vertices.append(u)
        assert common_ancestor is not None, 'Common ancestor must exist'
        w_blossom_vertices = []
        for u in w_path:
            if u == common_ancestor:
                break
            else:
                w_blossom_vertices.append(u)
        blossom_vertices = [common_ancestor] + list(reversed(v_blossom_vertices)) + w_blossom_vertices
        assert len(set(blossom_vertices)) == len(blossom_vertices), 'Blossom must not contain any duplicate vertices'
        assert len(blossom_vertices) % 2 != 0, 'Blossom must contain an odd number of vertices'
        blossom = Blossom(blossom_vertices, common_ancestor)
        return blossom

class Blossom:

    count = 0

    def __init__(self, vertices, base):
        Blossom.count += 1
        self.id = -Blossom.count
        self.vertices = vertices
        self.base = base
        self.__assert_representation()

    def __assert_representation(self):
        assert self.vertices[0] == self.base, 'Blossom must begin with base vertice'
        assert len(self.vertices) % 2 != 0, 'Blossom must have an odd number of vertices'
        assert len(self.vertices) >= 3, 'Blossom must have at least three vertices'

    def get_id(self):
        self.__assert_representation()
        return self.id

    def get_vertices(self):
        self.__assert_representation()
        return self.vertices

    def get_base(self):
        self.__assert_representation()
        return self.base

    def traverse_right(self):
        self.__assert_representation()
        for vertice in self.vertices:
            yield vertice

    def traverse_left(self):
        self.__assert_representation()
        for vertice in reversed(self.vertices[1:] + self.vertices[:1]):
            yield vertice

