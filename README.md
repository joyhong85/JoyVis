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
![sample1 result](https://github.com/joyhong85/JoyVis/blob/main/JoyVis/img/sample1.png)

## For Local File
~~~python
from JoyVis import Vis

v = Vis(filepath='/Users/joyhong/sample_result.ttl')
nw = v.vis_file(limit=200)
result = 'html/sample8.html'
nw.show(result)
~~~
![sample1 result](https://github.com/joyhong85/JoyVis/blob/main/JoyVis/img/sample8.png)

## For Jupyter Notebook
~~~python
v = Vis('http://localhost:3030/publicdata/query', notebook = True)
nw = v.vis(limit=50)
result = 'html/sample_notebook.html'
nw.show(result)
~~~
## Requirements
- pyvis
- RDFLib
- SPARQLWrapper
