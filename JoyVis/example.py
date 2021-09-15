from JoyVis import Vis, ShowLiteral
import webbrowser, os

def exam1():
    """
    default usage
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query')
    nw = v.vis(limit=50)
    result = 'html/sample1.html'
    nw.show(result)
    webbrowser.open('file://'+os.getcwd()+"/"+result)


def exam2():
    """
    show literals as nodes
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query')
    nw = v.vis(limit=50, show_literal=ShowLiteral.Yes)
    result = 'html/sample2.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam3():
    """
    show literals in node's tool-tip
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query')
    nw = v.vis(limit=50, show_literal=ShowLiteral.InNode)
    result = 'html/sample3.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam4():
    """
    useArrow = False
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query')
    v.useArrow(False)
    nw = v.vis(limit=50, show_literal=ShowLiteral.Yes)
    result = 'html/sample4.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam5():
    """
    use search keyword
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query')
    nw = v.vis(search_keyword='서울',limit=150, show_literal=ShowLiteral.Yes)
    result = 'html/sample5.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam5():
    """
    use search keyword
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query')
    nw = v.vis(search_keyword='서울',limit=150, show_literal=ShowLiteral.Yes)
    result = 'html/sample5.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam6():
    """
    use specific uri
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query')
    nw = v.vis(uri='http://joyhong.tistory.com/resource/h_1111',limit=150, show_literal=ShowLiteral.Yes)
    result = 'html/sample6.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam7():
    """
    set ignore properties to show
    :return:
    """
    from rdflib.namespace import RDF

    v = Vis('http://localhost:3030/publicdata/query')

    ignore = [str(RDF.type)]
    v.setIgnoreProperty(ignore)

    nw = v.vis(uri='http://joyhong.tistory.com/resource/h_1111',limit=150, show_literal=ShowLiteral.Yes)
    result = 'html/sample7.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam8():
    """
    usage for File
    :return:
    """
    v = Vis(filepath='/Users/joyhong/sample_result.ttl')
    nw = v.vis_file(limit=200)
    result = 'html/sample8.html'
    nw.show(result)
    webbrowser.open('file://' + os.getcwd() + "/" + result)


def exam_notebook():
    """
    for jupyter notebook
    :return:
    """
    v = Vis('http://localhost:3030/publicdata/query', notebook=True)
    nw = v.vis(limit=50)
    result = 'html/sample_notebook.html'
    nw.show(result)

exam_notebook()