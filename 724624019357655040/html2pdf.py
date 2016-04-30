# -*- coding: utf-8 -*-

"""
    Convert html to PDF
"""

from functools import wraps
from xhtml2pdf import pisa

import sys


def tags(tag_name):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(content):
            if tag_name == "head":
                head_content = """
                    <style>
                    @page {
                        size: A4 portrait;
                        @frame header_frame {           /* Static frame */
                            -pdf-frame-content: header_content;
                            left: 50pt; width: 512pt; top: 50pt; height: 40pt;
                        }
                        @frame footer_frame {           /* Static frame */
                            -pdf-frame-content: footer_content;
                            left: 50pt; width: 512pt; top: 772pt; height: 20pt;
                        }
                        @frame content_frame {          /* Content Frame */
                            left: 50pt; width: 512pt; top: 90pt; height: 632pt;
                        }
                    }
                    </style>
                """
                return "<{0}>{1}</{0}>{2}".format(tag_name,
                                                  head_content,
                                                  func(content))    
            return "<{0}>{1}</{0}>".format(tag_name, func(content))
        return func_wrapper
    return tags_decorator


def insert_header(header_template, header_content):
    if not header_template:
        header_template = "<div id='header_content'>{}</div>"

    def _header(func):
        @wraps(func)
        def wrap_header(body):
            header = header_template.format(header_content) 
            return header + func(body)

        return wrap_header
    return _header


def insert_footer(footer_template, footer_content):
    if not footer_template:
        footer_template = "<div id='footer_content'>{}</div>"

    def _footer(func):
        @wraps(func)
        def wrap_footer(body):
            footer = footer_template.format(footer_content) 
            return func(body) + footer

        return wrap_footer
    return _footer



@tags("html")
@tags("head")
@tags("body")
@insert_footer(footer_content="(c) - page <pdf:pagenumber> of <pdf:pagecount>",
               footer_template="")
@insert_header(header_content="HEADER CONTENT",header_template="")
def make_content(body):
    return body

def main():
    pisa.showLogging()

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    inputContent = ""
    with open(inputFile, 'r') as iF:
        inputContent = make_content(iF.read())

    with open(outputFile, 'wb') as oF:
        pisaStatus = pisa.CreatePDF(inputContent, dest=oF)
        print ("Printed at {}".format(outputFile))


if __name__ == "__main__":
    main()
