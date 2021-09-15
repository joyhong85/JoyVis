from pyvis.network import Network
import networkx as nx
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
import json

from enum import Enum


class ShowLiteral(Enum):
    Yes = 0
    No = 1
    InNode = 2


class Vis(object):
    """
    SPARQL Endpoint 과 연동하여 특정 트리플들을 시각화하는 도구,
    파일을 읽어 파일의 내용을 시각화할 수도 있다.
    """

    def __init__(self, endpoint=None, filepath=None, ignore_property=[], notebook=False):
        self.__endpoint = endpoint
        self.__filepath = filepath
        self.__ignore_property = ignore_property if ignore_property != None else []
        self.__sparql = SPARQLWrapper(endpoint)
        self.__useArrow = True
        self.__notebook = notebook


    def __getLocalName(self, node):
        if node.find('/') > 0 and node.find('#') > 0:
            return node[node.rindex('/') + 1:] if node.rindex('/') > node.rindex('#') else node[node.rindex('#') + 1:]
        elif node.find('/') > 0:
            return node[node.rindex('/') + 1:]
        elif node.find('#') > 0:
            return node[node.rindex('#') + 1:]
        else:
            return node

    def useArrow(self, flag=True):
        self.__useArrow = flag

    def __make_short_name(self, name):
        if len(name) > 20:
            name = name[0:20]
        return name

    def setIgnoreProperty(self, ignore_property):
        self.__ignore_property = ignore_property

    def __show_graph(self, results, show_literal):
        nw = Network(height='800px', width='70%', notebook=self.__notebook)

        node = {}
        groups = {}
        node_num = 0;
        group_num = 0;
        edge_list = []

        if show_literal:
            groups['literal'] = group_num
            group_num += 1

        for result in results["results"]["bindings"]:
            #             print(result["s"]["value"], "\t", result["p"]["value"], "\t", result["o"]["value"])
            #             print(result)
            if not result["p"]["value"] in self.__ignore_property:
                if 'slabel' not in result:
                    result['slabel'] = {'type': 'literal', 'value': self.__getLocalName(result['s']['value'])}
                if 'olabel' not in result:
                    result['olabel'] = {'type': 'literal', 'value': self.__getLocalName(result['o']['value'])}
                if 'stype' not in result:
                    result['stype'] = {'type': 'literal', 'value': ''}
                if 'otype' not in result:
                    result['otype'] = {'type': 'literal', 'value': ''}

                # Node
                if result['s']['type'] == 'uri' and not result['s']['value'] in node:
                    node[result['s']['value']] = {'id': node_num}
                    node_num += 1

                if result['o']['type'] == 'uri' and not result['o']['value'] in node:
                    node[result['o']['value']] = {'id': node_num}
                    node_num += 1

                if 'stype' in result and not result['stype']['value'] in groups:
                    groups[result['stype']['value']] = group_num
                    group_num += 1
                if 'otype' in result and not result['otype']['value'] in groups:
                    groups[result['otype']['value']] = group_num
                    group_num += 1

                node[result['s']['value']].update(
                    {'label': result['slabel']['value'], 'type': result['stype']['value']})
                if result['o']['type'] == 'uri':
                    node[result['o']['value']].update(
                        {'label': result['olabel']['value'], 'type': result['otype']['value']})
                    edge_list.append((result['s']['value'], result['o']['value'], result['p']['value']))

                # show literal
                if show_literal == ShowLiteral.Yes:
                    if result['o']['type'] == 'literal':
                        node[result['o']['value'] + str(node_num)] = {'id': node_num}
                        node[result['o']['value'] + str(node_num)].update(
                            {'label': result['o']['value'], 'type': 'literal'})
                        edge_list.append((result['s']['value'], result['o']['value'], result['p']['value'],
                                          result['o']['value'] + str(node_num)))
                        node_num += 1

                # show literal in node tooltip
                if show_literal == ShowLiteral.InNode:
                    if result['o']['type'] == 'literal':
                        if 'datatype' in node[result['s']['value']]:
                            dt = node[result['s']['value']]['datatype'] + '<br>' + self.__getLocalName(
                                result['p']['value']) + ":" + result['o']['value']
                            node[result['s']['value']].update({'datatype': dt})
                        else:
                            node[result['s']['value']]['datatype'] = self.__getLocalName(result['p']['value']) + ":" + \
                                                                     result['o']['value']
                            node[result['s']['value']].update({'datatype': node[result['s']['value']]['datatype']})

        for n in node:
            if node[n]['type'] == 'literal':
                nw.add_node(n, shape='box', label=self.__make_short_name(node[n]['label']), title=node[n]['label'],
                            group=groups[node[n]['type']])
            else:
                if 'datatype' in node[n]:
                    nw.add_node(n, label=self.__make_short_name(node[n]['label']),
                                title=n + "<br>" + node[n]['datatype'], group=groups[node[n]['type']])
                else:
                    nw.add_node(n, label=self.__make_short_name(node[n]['label']), title=n,
                                group=groups[node[n]['type']])
        for e in edge_list:
            if len(e) == 4:
                if self.__useArrow:
                    nw.add_edge(e[0], e[3], arrows='to', label=self.__getLocalName(e[2]), title=e[2])
                else:
                    nw.add_edge(e[0], e[3], label=self.__getLocalName(e[2]), title=e[2])
            else:
                if e[2] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                    if self.__useArrow:
                        nw.add_edge(e[0], e[1], width=4, color='black', arrows='to', label=self.__getLocalName(e[2]),
                                    title=e[2])
                    else:
                        nw.add_edge(e[0], e[1], width=4, color='black', label=self.__getLocalName(e[2]), title=e[2])
                else:
                    if self.__useArrow:
                        nw.add_edge(e[0], e[1], arrows='to', label=self.__getLocalName(e[2]), title=e[2])
                    else:
                        nw.add_edge(e[0], e[1], label=self.__getLocalName(e[2]), title=e[2])

        nw.set_edge_smooth('dynamic')
        nw.show_buttons(filter_=['physics'])

        return nw

    def __run_query(self, query_string, show_literal):
        self.__sparql.setQuery(query_string)
        self.__sparql.setReturnFormat(JSON)
        results = self.__sparql.query().convert()
        nw = self.__show_graph(results, show_literal)
        return nw

    def vis(self, search_keyword: str = '', uri: str = '', limit: int = 500,
            show_literal: ShowLiteral = ShowLiteral.No):
        if limit > 1000:
            limit = 1000

        if uri != '':
            query_string = """
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?s ?p ?o ?slabel ?olabel ?stype ?totype
                WHERE {
                    {
                        filter(?s=<%s>)
                        ?s ?p ?o.
                        optional{?s rdfs:label ?slabel .}
                        optional{?s a ?stype}
                        optional{?o rdfs:label ?olabel .}
                        optional{?o a ?otype}
                      } UNION {
                        filter(?o=<%s>)
                        ?s ?p ?o.
                        optional{?s rdfs:label ?slabel .}
                        optional{?s a ?stype}
                        optional{?o rdfs:label ?olabel .}
                        optional{?o a ?otype}
                      }
                } LIMIT %i
            """ % (uri, uri, limit)
        elif search_keyword != '':
            query_string = """
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?s ?p ?o ?slabel ?olabel ?stype ?totype
                WHERE {
                    ?s ?pp ?oo.
                    filter(regex(?oo, '%s'))
                    ?s ?p ?o.
                    optional{?s rdfs:label ?slabel .}
                    optional{?s a ?stype}
                    optional{?o rdfs:label ?olabel .}
                    optional{?o a ?otype}
                } LIMIT %i
            """ % (search_keyword, limit)
        else:
            query_string = """
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    SELECT *
                    WHERE {
                        ?s ?p ?o.
                        optional{?s rdfs:label ?slabel .}
                        optional{?s a ?stype}
                        optional{?o rdfs:label ?olabel .}
                        optional{?o a ?otype}
                    } LIMIT %i
                """ % limit

        return self.__run_query(query_string, show_literal)

    def vis_file(self, uri: str = '', show_literal: ShowLiteral = ShowLiteral.Yes,  limit: int = 500):
        g = Graph()
        g.parse(self.__filepath, format='turtle')

        if uri != '':
            qres = g.query("""
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?s ?p ?o ?slabel ?olabel ?stype ?totype
                WHERE {
                    {
                        filter(?s=<%s>)
                        ?s ?p ?o.
                        optional{?s rdfs:label ?slabel .}
                        optional{?s a ?stype}
                        optional{?o rdfs:label ?olabel .}
                        optional{?o a ?otype}
                      } UNION {
                        filter(?o=<%s>)
                        ?s ?p ?o.
                        optional{?s rdfs:label ?slabel .}
                        optional{?s a ?stype}
                        optional{?o rdfs:label ?olabel .}
                        optional{?o a ?otype}
                      }
                } LIMIT %i
            """ % (uri, uri, limit))
        else:
            qres = g.query("""
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT *
                WHERE {
                    ?s ?p ?o.
                    optional{?s rdfs:label ?slabel .}
                    optional{?s a ?stype}
                    optional{?o rdfs:label ?olabel .}
                    optional{?o a ?otype}
                }  LIMIT %i
            """ % limit )
        f = open('json_result', 'w')
        JSONResultSerializer(qres).serialize(f)
        with open('json_result') as f:
            read_data = json.load(f)

        nw = self.__show_graph(read_data, show_literal)
        return nw


