from pyvis.network import Network
import networkx as nx

def create_import_graph(import_data):
    G = nx.DiGraph()

    for file, imports in import_data.items():
        # Add a node for the file
        G.add_node(file, type='file')

        for imp in imports:
            module_name = imp['name']
            is_local = imp['is_local']

            if is_local:
                # If it's a local import, assume it's another file in the project
                local_module_path = f'./repo/{module_name.replace(".", "/")}.py'
                G.add_node(local_module_path, type='file')
                G.add_edge(file, local_module_path)  # Add directed edge between the files
            else:
                # If it's not local, it's an external library
                G.add_node(module_name, type='external_library')
                G.add_edge(file, module_name)  # Add directed edge to the external library

    return G

def create_pyvis_graph(G):
    net = Network(notebook=True, cdn_resources="in_line")  # Use in_line or remote for better browser compatibility

    # Add nodes and edges from NetworkX graph
    for node in G.nodes:
        net.add_node(node, label=node, size=3 * G.degree(node))
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    # Show the interactive graph in a browser
    net.show("import_graph.html")

