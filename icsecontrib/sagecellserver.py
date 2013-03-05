#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive



class sagecellserver(nodes.General, nodes.Element): 
    pass


def visit_sagecellserver_node(self, node):
    self.body.append("<div class='sage'>")
    self.body.append("<script type='text/x-sage'>")	    
    self.body.append(node['python_code'])    
    self.body.append("</script>")    
    self.body.append("</div>")	


def depart_sagecellserver_node(self, node):
    pass	


class SageCellServer(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        "prompt_tag": directives.unchanged,
    }
	
    def run(self):               
        if "prompt_tag" in self.options:
            annotation = self.options.get("prompt_tag")
        else:
            annotation = "False"

        content_list = self.content

        if annotation == "False":
            content_list = map(lambda x: x.replace("sage: ", "").replace("...   ", ""), content_list)
        
        node = sagecellserver()    
        node['python_code'] = '\n'.join(content_list)        
    
        return [node]		


def setup(app):
    app.add_node(sagecellserver, html=(visit_sagecellserver_node, depart_sagecellserver_node))
    app.add_directive("sagecellserver", SageCellServer)


