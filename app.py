"""
Workflow
Download Repo
go through repo + create import graph

"""

import repo_parser
import grapher
import getGithub
import sys


args = sys.argv[1:]
link = args[0]
name = args[1]
if not link or not name:
    exit()
print(link, name)
getGithub.download_repo(link, name)
# get repo
data = repo_parser.parse_repo('./repo/' + name + '/')
print(data)

# Build the graph
G = grapher.create_import_graph(data)

# Visualize the graph interactively
grapher.create_pyvis_graph(G)