import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

st.title('Graph Data Vis - V2')

num_datasets = st.slider('Number of datasets', 1, 10, 1)

relationships = []

tables = []

edges = []

for i in range(num_datasets):
    st.subheader(f'Dataset {i+1}')
    table = st.file_uploader(f'Upload dataset {i+1}', type=['csv', 'xlsx'])
    if table is not None:
        table = pd.read_csv(table)
        tables.append(table)
        st.write(table)

num_relationships = st.slider('Number of relationships', 1, 10, 1)

if num_relationships > 0 and num_datasets > 1:
    for i in range(num_relationships):
        st.subheader(f'Relationship {i+1}')
        from_dataset = st.selectbox('From', range(1, num_datasets+1), key=(i+1)*10)
        to_dataset = st.selectbox('To', range(1, num_datasets+1), key=(i+1)*100)
        foreign_key = st.selectbox('Foreign Key', tables[to_dataset-1].columns, key=(i+1)*1000)
        relationships.append((from_dataset, to_dataset, foreign_key))

for rel in relationships:
    from_dataset, to_dataset, foreign_key = rel
    from_table = tables[from_dataset-1]
    to_table = tables[to_dataset-1]

    st.subheader(f'Relationship {from_dataset} to {to_dataset}')
    st.write(from_table)
    st.write(to_table)
    
    # read row wise, split column containing foreign key by comma and add the first column and the values in the split columns to edges

    for i in range(len(to_table)):
        to_row = to_table.iloc[i]
        from_value = to_row[foreign_key]
        from_values = str(from_value).split(',')
        for from_value in from_values:
            edges.append((from_value, to_row[0]))

def create_graph(net):

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        net.show('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

    # Read the HTML file
    source_code = HtmlFile.read()

    return components.html(source_code, height=400)





if st.button('Visualize'):

    G = Network(
                height='400px',
                width='100%',
                bgcolor='white',
                font_color='black',
                directed=True,
                neighborhood_highlight=True,
            )

    if len(tables)>0:
        for i in range(num_datasets):
            for index, row in tables[i].iterrows():
                G.add_node(str(row[0]), label=str(row[0]), title=str(row[0]), group=i)

        # check if the nodes are present and form edges as given in edge list
        node_names = [node['id'] for node in G.nodes]
        st.write('Node Names:', node_names)
        st.write('Edges:', edges)
        for edge in edges:
            if str(edge[0]) in node_names and str(edge[1]) in node_names:
                G.add_edge(str(edge[0]), str(edge[1]))

    st.header('Graph Visualization')
    create_graph(G)