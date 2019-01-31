#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

class MarkdownLogger(object):

    @staticmethod
    def println(msg, bold=False, italic=False):
        new_msg = msg if not bold else "__%s__" % msg
        new_msg = new_msg if not italic else "_%s_" % new_msg
        print new_msg, "  "

    @staticmethod
    def print_header(header, level=1):
        print "\n", "#"*level, header

    @staticmethod
    def print_header2(header):
        MarkdownLogger.print_header(header, 2)

    @staticmethod
    def print_header3(header):
        MarkdownLogger.print_header(header, 3)

    @staticmethod
    def print_url(label, url):
        print "[%s](%s)" % (label, url)

    @staticmethod
    def print_para(msg):
        print "\n", msg, "\n"

    @staticmethod
    def print_hr():
        print "***"

    @staticmethod
    def print_code(msg):
        print "\n", "```"
        print msg
        print "```\n"

    @staticmethod
    def print_list(items, ordered=False):
        delimiter = "1." if ordered else "*"
        for item in items:
            print delimiter, item
        print "\n"

    @staticmethod
    def print_table(headers, rows):
        print "\n|", "|".join(headers), "|"
        print "|", " ------ |" * len(headers)
        for r in rows:
            print "| ", "  |".join(r), " |"
        print "\n"

    @staticmethod
    def print_error(msg):
        MarkdownLogger.print_hr()
        MarkdownLogger.print_header3("Error")
        if hasattr(msg, '__call__'):
            #function
            msg()
        else:
            MarkdownLogger.print_para(msg)
        MarkdownLogger.print_hr()

    @staticmethod
    def print_link(link_name, url, prefix_msg=""):
        MarkdownLogger.println("%s [%s](%s)" % (prefix_msg, link_name, url))


