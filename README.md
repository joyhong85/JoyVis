# JoyVis
RDF Visualization

## For SPARQL Endpoint
~~~python
from JoyVis import Vis

v = Vis('http://localhost:3030/publicdata/query')
nw = v.vis(limit=50)
result = 'html/sample1.html'
nw.show(result)
~~~

## For Local File
~~~python
from JoyVis import Vis

v = Vis(filepath='/Users/joyhong/sample_result.ttl')
nw = v.vis_file(limit=200)
result = 'html/sample8.html'
nw.show(result)
~~~

## Requirements
- pyvis
- RDFLib
- SPARQLWrapper
