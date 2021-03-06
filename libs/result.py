from sys import version_info
import os
from . import addon


if version_info.major == 3:
    from .printf.py3 import printf
else:
    from .printf.py2 import printf


def export_html(export_file, web, web_text):  # export result file
    try:  # open file
        export_f = open(export_file, "a+")  # use add to open file
        export_f.seek(274, 0)  # turn after to</center>
    except:
        printf("Cann't export the result!!!", "error")
        # set format to html
    export_web = "<li><a href=\"{0}\" target=\"_blank\">{1}</a></li>".format(web, web_text)
    export_web_len = len(export_web)
    export_f.write(export_web)
    export_f.seek(0, 0)  # goto file's head
    export_f.close()


def init_html(filename):  # init the web form
    if os.path.exists("output"):
        pass
    else:
        try:
            os.mkdir("ouput")
        except:
            pass
    web_frame = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>WMIN result</title>
    <style type="text/css">
    <!--
    a:link {
        text-decoration: none;
    }
    a:visited {
        text-decoration: none;
    }
    a:hover {
        text-decoration: none;
    }
    a:active {
        text-decoration: none;
    }
    -->
    </style>
    </head>
    <body>

    <left>
    <h3>
    <b>
    WMIN v1.0 scan report
    </b>
    </h3>
    </left>

    </body>
</html>"""

    export_filename = "ouput/" + filename + ".html"  # set output filename
    try:
        export_file = open(export_filename, "w")  # use write to open file
    except:
        printf("result file can't be created!", "error")
    export_file.write(web_frame)  # write to web form
    export_file.close()
    return export_filename  # return filename
