
def this_is_a_test():

	return <%
This is intended to be included as text, and returned as a string
\\a\\1\\2\\3\\4\\5\\6\\7\\8\\9\\b\\f\\v\\r\\n\\t\\0\\x0B   testing3, expected
<!-- escape characters within include files -->

%>


	
def python_php_htmlentities(s):

	salt = uuid.uuid4().hex
	
	s = s + r'\a\1\2\3\4\5\6\7\8\9\b\f\v\r\n\t\0\x0B'
	
	s = s.replace('&quot;&quot;&quot;', '*QUOT-*-QUOT-*-QUOT*'+salt);
	
	code_init = <% echo htmlentities('%s'); %>  %  s.replace("'", "\\'")  # quotes cause problem to format string variables, give it a raw string literal
															
	width = 200
	height = 200
	
	code_here = <%
	echo ('   {**{php_width}**}, {**{php_height}**}  ');
	%>.format( php_width = str(width) , php_height = str(height) )

	var = php(code_init)
	
	
	var = var.replace('*QUOT-*-QUOT-*-QUOT*'+salt, '&quot;&quot;&quot;')
	
	var = var.replace( '&amp;lt;%' , '&lt;%' ).replace( '%&amp;gt;', '%&gt;' ) # due to quick tags must be in htmlentities form between quick tags <% %>

	
	return var

	
def source_code_incl():

	#simple_preprocessor.py to address """ """ between quick tags and other small things of a raw string literal
	
	return <%

	'how about this nice person you'
 
""" hello world, within triple double quotes within python quick tags """

	<br>
	hello world, this is the source code included file
	<unicode></unicode>
	
	<p> </p>

&lt;% %&gt;   and feature added 2015.02.17 to convert back (when double htmlentities to quick tags strings)	
	
%>.htmlentities() 

# now method instead of the function, bit easier
# python_php_htmlentities( source_code() )

def source_code_output():
	return <%
	
{**{source_code_htmlentities_form}**}
	
%>.format( source_code_htmlentities_form = python_php_htmlentities( source_code_incl() ) ) # note: at this time not to double htmlentities process
