import os
import sys

# pyThor (pyTron) page
# Internal are these functions that you can use, the source code to view is in the file  simple_preprocessor_pyThor_features_txt.py
#                                                   the compiled version is in the file  front_compiled.py
#                                                   for review

#  1)     python quick tags  <%  %>
#  2)                              .htmlentities()   on the python quick tags          (to display source code) (note to wrap your format variable in pre tags for newlines work ok)

#  3)     source_code_from_file(file)                # file is the filename of the source code you would like to display

#  4)     use of superglobal variables from PHP in the form of pySERVER,pyGET,pyPOST,pyFILES as accessed in PHP
#         Though recommended for convenience is to use the name of the variable that is global 
#         e.g.,  Recommended use  DOCUMENT_ROOT  this is a global variable, instead of pySERVER['DOCUMENT_ROOT'], and so on (to access other PHP superglobal variables)
#         Please note that the keyword global must be used to access the superglobal variable within any function or method that you intend to use the variable.

#  5)     print_wwwlog(any_text_to_print_to_console_log_string_or_variable_etc)    # prints to brower's console log

# Note:  The variable   ensure  is set to True inititally, this can be set to False for a slight speed increase in the  simple_preprocessor_pyThor_features_txt.py  file ) ( also note: python allows to overwrite functions by simply making a function by the same name in this file as is defined in the simple_preprocessor_pyThor_features_txt.py file, though not recommended)


#  List Of PyThor features
#  -----------------------
#       From the .php file     *.php?pagesource       to display the actual page source code of the webpage (without the source code to the core pyThor features)
#                              *.php?fullsource       to display the full source code of a webpage similar to the view source as feature of web browsers 
#                              *.php?pythorinfo       to display the environment variables of the web server, e.g., pySERVER, pyGET, pyPOST, and pyFILES
#                              *.php?features         to access the feature list
#                                   
#
#       Note that each of these url get parameters are easily configured that can be removed as shown in the example source code page auto created initially (note the .format method of the main function output )


# INCLUDES TO BE PLACED HERE
file_to_include = 'include.py'
execfile(include_quick_tags_file(file_to_include)) # including this way due to execfile does not include file from within a def,function


def source_code():   # note, this is just source code print to display, not the entire page of the function output prints to the web browser, screen
	return <%
<html>
</head>
<script type="text/javascript">
	alert('hello world');
	// when using jquery then the next line
	//$(document).ready(function() {
		//console.log( "ready!" );
		//alert('hello world');
	//});
</script>

</head>
<body>
<h1>hello world</h1>
<br>
page contents here
and more of the website too
<b>have a great day!</b>
<br>
</body>
</html>
	
%>.htmlentities()
	
def top_content():
    
	print_wwwlog( <% This string is at the top content %> ) 
	
	print_wwwlog ( <% another example of new feature using quick tags between parenthesis %> )
	
	return ' pyThor    @    www.pyThor.us '
	
def mid_content():

	var_msg = 'HELLO WORLD! - PyThor for Web Programming'
	
	print_wwwlog( <% This string is at the middle content
<br>
<br>
hello world  (but html tags are raw string literal strings within browser console log window)
%>    )

	return <%
	 
{**{var_msg}**}

%>
	 
def end_content():
	return 'footer'


def domain_name(s):   
	if(s == 'A'):
		return 'us'
	elif(s == 'WIDE'):
		return 'com'

# test example, don't forget to have php.exe and php5ts.dll in PATH
width = 100
height = 100
code = <%

echo ('   {**{width}**}, {**{height}**}  ');

%>


global direct_global_var

def output(name):

	direct_global_var = 'planet earth, (mercury, venus) mars, etc'
	direct_local_var = 'hello world'
	local_var2 = 'hows it going'
	int_var = 1223344
	float_var = 5566778899.0
	<%

<!DOCTYPE html>
<html lang="en">
<head>
<title></title>
<script src="js/jquery-1.11.2.min.js"></script>
<link rel="stylesheet" type="text/css" href="css/page_frame_{**{domain}**}.css" />
<script src="first.js"></script>

<script>
$(document).ready(function() {
	console.log('jquery 1.11.2 initialized');
	console.log('app.js loading...  if capitalized done. statement does not appear next, or as the print line to the console, there is an error occurring');
});

jQuery.getScript("first.js", function() {
	console.log('DONE.');
});
</script>
 
</head>
<body><br>

 {**{direct_local_var}**}  {**{local_var2}**}  {**{direct_global_var}**} {**{int_var}**} {**{float_var}**}
<br>
<a href="{**{pagesourcelink}**}">click to view pyThor page source</a> <br>  
<pre style="display:inline">{**{pagesource}**}</pre>
<!-- similar to view source as feature of web browsers -->  

<a href="{**{fullsourcelink}**}">view full page source</a> <br>
<pre style="display:inline">{**{fullsource}**}</pre>

<a href="{**{pythorinfolink}**}">pyThorInfo</a> {**{pyThorinfo}**}  
<!-- Display pyThor environment by a url get (variable) -->

<br>{**{testing_output}**}<br>
<div id="container">

<div id="top">{**{top_content_var}**}</div>

<div id="mid">{**{mid_content_var}**} <br>  <pre>{**{features}**}</pre>   </div>

<div id="end">{**{end_content_var}**}</div>

</div>

String Tests:
NOTE: Just Testing OUTPUT HERE (note: the following escape characters need double backslash (octals not tested at this time)<br>
\\\r\\n\\t\\0\\x0B  testing1, expected
<br>

\\a\\1\\2\\3\\4\\5\\6\\7\\8\\9\\b\\f\\v\\r\\n\\t\\0\\x0B   testing2, expected
Result: Easy dealing with escape characters here. Though a python def, function like PHP's htmlentities still perhaps required (to be written,created)
<br>
PHP test: {**{php_test}**}
</body>
</html>


<unicode>hello world</unicode>


<pre style="white-space: pre-wrap;"> (note that this wrap use of pre tags will wrap its text)

<b>Any Characters permissible within python quick tags &lt;% %&gt; (strings), neat</b>

Though this to note:<br>
&lt;% %&gt; , allows quick tags between quick tags though must be in html entities form


''' triple single quotes allowed also '''

""" triple double quotes now allowed within python quick tags, feature added 2015.02.08 """

</pre>

<h1>Example Of Displaying Source Code</h1>
<pre>{**{source_variable}**}</pre>    (Note that to display source code with the same newlines as in the source code, it should be wrapped in pre tags without the css style wrapping of text as in the examples before and after the display of this source code)


<pre style="white-space: pre-wrap;">
This format variable (see your_page.) is processed, it's converted to htmlentities
feature added to QuickTags to htmlentities any python quick tags &lt;% %&gt; (string) (Note: only python quick tag &lt;% %&gt; strings MUST be converted, the rest optional for display purposes), feature added 2015.02.17


(Note: To not .htmlentities the contents of the page itself within the &lt;head&gt;&lt;/head&gt; section of html tags, javascript between python quick tags &lt;% %&gt; , etc. ) 

(htmlentities can be used for many purposes, such as to display source code blocks of code)

quick way to html entities a string {**{example_htmlentities_string}**}

While still compatible with being able to use python format variables,

{**{ python quick tags format variable now as wysiwyg text when undefined in format method parameters, feature added 2015.02.16 }**}


{**{     var    }**}
</pre>

</pre>

%>.format (   # variables used
	
	top_content_var = top_content(),
	mid_content_var = mid_content(),
	end_content_var = end_content(),
	php_test    = php(code),  # just testing, remove if coding anything serious

	domain = 'us' if (name == 'A') else  'com',                  # else (name == 'WIDE')  # or something like whether a mobile device, resolution information, etc. to select which css that fits

	testing_output = '', #this_is_a_test(),    # test of include file using quick tags python syntax

	source_variable = source_code(),

	example_htmlentities_string = <%  <p><hello world note p tags output><p>  %>.htmlentities(), # note, python quick tags stings have .htmlentities method

	pagesourcelink = 'index.php?pagesource',

	pagesource = source_code_from_file( r'front.py' ) if (QUERY_STRING == 'pagesource') else '' , 								 			 

	fullsourcelink = './index.php?fullsource',
	
	fullsource = get_fullsource(pretags=True) if (QUERY_STRING == 'fullsource') else '' , 

	 __formatvariable_range = ('*--START OF FULL SOURCE--*'.replace(' ', '_' ) , '*--END OF FULL SOURCE--*'.replace(' ', '_' )) if (QUERY_STRING == 'fullsource') else ('',''),

	pythorinfolink = './index.php?pythorinfo',

	pyThorinfo = display_pythorinfo() if (QUERY_STRING == 'pythorinfo') else '',   #remove this line to remove the url feature  # for demonstration purpose only, please remove the next line for production code (it is however a feature that is available at any time should you code it)

	features = display_features() if (QUERY_STRING == 'features') else ''
)

	# testing writing print statement to the web browser 
	# the intent is to create a python function to wrap the writing with print statements to the web browser's console
	code_init = <%
$name = 'Stan Switaj';
 
$fruits = array("oranges", "apples", "strawberry", "pineapple", "kiwi");

$user = new stdClass;
$user->name = 'Hello 123.00 \\a\\1\\2\\3\\4\\5\\6\\7\\8\\9\\b\\f\\v\\r\\n\\t\\0\\x0B ';
$user->desig = "CEO";
$user->lang = "PHP Running Through subprocess (python)";
$user->purpose = "To print log messages to the browser console messages to the browser";
// var_dump($fruits);        // Remove php comment to output data structure to web browser 
logConsole('$name var', $name, true);
logConsole('An array of fruits', $fruits, true);
logConsole('$user object', $user, true);
%>

	# Written to print to the console log of a web browser
	s = (code_init + "\n" + console_log_function()  )

	# TO OUTPUT to web
	print php(  s   )
	