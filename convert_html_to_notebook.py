from bs4 import BeautifulSoup
import json
import urllib.request
import os

def convert_html_to_notebook(file_path_html, file_path_output=None) :
    """
        file_path_html: file path of your html file ( which has been generated from a notebook) 
        file_path_output: default use the same location of the file otherwise use the one specify by the user 
    """
    text=None
    with open(file_path_html,'r',encoding='utf-8') as f :
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')
    # see some of the html
    print(soup.div)
    dictionary = {'nbformat': 4, 'nbformat_minor': 1, 'cells': [], 'metadata': {}}
    for d in soup.findAll("div"):
        if 'class' in d.attrs.keys():
            for clas in d.attrs["class"]:
                if clas in ["jp-RenderedMarkdown", "jp-InputArea-editor"]:
                    # code cell
                    if clas == "jp-InputArea-editor":
                        cell = {}
                        cell['metadata'] = {}
                        #cell['outputs'] = []
                        cell['source'] = [d.get_text()]
                        cell['execution_count'] = None
                        cell['cell_type'] = 'code'
                        dictionary['cells'].append(cell)
    
                    else:
                        cell = {}
                        cell['metadata'] = {}
    
                        cell['source'] = [d.decode_contents()]
                        cell['cell_type'] = 'markdown'
                        dictionary['cells'].append(cell)#
    if file_path_output is None :
        folder_output = os.path.dirname(file_path_html) 
        file_name = os.path.basename(file_path_html).replace(" ","_").replace(".html",".ipynb")
        file_path_output = os.path.join(folder_output,file_name)
    with open(file_path_output, 'w') as fw :
        fw.write(json.dumps(dictionary))
        
# example 
# convert_html_to_notebook(file_path_html=r'C:\tmp\my_file.html')
# --> it will create the file : C:\tmp\my_file.ipynb