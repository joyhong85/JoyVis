from JoyVis import Vis, ShowLiteral
import webbrowser, os

v = Vis('http://localhost:3030/publicdata/query', notebook=True)
v.useArrow(False)

nw = v.vis(limit=50, show_literal=ShowLiteral.Yes)

result = 'html/sample.html'
nw.show(result)
webbrowser.open('file://'+os.getcwd()+"/"+result)