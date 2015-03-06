import os
import sys

  
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
#       From the .php file     *.php?fullsource       to display the full source code of a webpage similar to the view source as feature of web browsers 
#                              *.php?pythorinfo       to display the environment variables of the web server, e.g., pySERVER, pyGET, pyPOST, and pyFILES
#                              *.php?features         to access the feature list
#                                   
#
#       Note that each of these url get parameters are easily configured that can be removed as shown in the example source code page auto created initially (note the .format method of the main function output )



# INCLUDES TO BE PLACED HERE
file_to_include = 'include.py'
# including this way due to execfile does not including a file within a def,function as I expected
#execfile(include_quick_tags_file(file_to_include))	# this functin used to include each python file with quick tags		 

# NOTE: include section of source code with two entries due to workaround needed for execfile def,function
execfile(include_quick_tags_file(file_to_include))



		
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
    
	print_wwwlog( '''I am at " the top " content''' ) # NOTE: better to use triple single quotes , best to put a space before and after a triple quoted string (though not necessary for triple SINGLE quotes)
	                                                  # (the open and close quick tags (< % % > with no spaces) to denote a 
                                                      # triple double quoted string ONLY for return and assignment statements at this time) 
                                                      # due to a space needed before closing parenthesis 
                                                      # when using triple DOUBLE quotes (no restriction with triple SINGLE quotes by you, the programmer)
	# at this time, one or no spaces between open parenthesis and open quick tag (no resriction on the close python quick tag as far as spaces around it)
	print_wwwlog ( <% example of new feature using quick tags between parenthesis %> )
	
	return ' pyThor    @    www.pyThor.us '
	
def mid_content():

	print_wwwlog( <% I am  at  '''''''{}{}{}{} {{{{ }}}} the middle content \a\1\2\3\4\5\6\7\8\9\b\f\v\r\n\t\0\x0B
	
	
I have denoted newlines within a raw string , sent to the web browser that also interprets as newlines
And saving the file also is fine.

<br>
<br>
hello world  (but html characters are not interpreted this way)
%>    )  # TWO SMALL CASES TO ESCAPE WITH RAW STRING LITERALS, a backslash before a single quote or double quote 
          # (depending what are the outer quotes) and if the intent is to have a backslash at the end of a string, need two of them

	return <%
	 
{**{var_msg}**}

%>.format( var_msg = 'HELLO WORLD - PyThor for Web Programming' )
	 
def end_content():
	return 'footer'
	
# in the case not transferring data from php using multiple domains, simply revert to a previous version, commit 
def domain_name(s):   
	if(s == 'A'):
		return 'us'
	elif(s == 'WIDE'):
		return 'com'

# test example, don't forget to have php.exe and php5ts.dll in PATH
width = 100
height = 100
code = <%

echo ('   {**{php_width}**}, {**{php_height}**}  ');

%>.format( php_width = str(width) , php_height = str(height) )

# Note, any JavaScript or any other code that contains a curly brace 
# must double the curly brace when using the python format function with the triple double-quoted string, 
# but not in a JavaScript src file (regardless of using the format function or not).

# It further verifies that the compiled python-like RadScript JavaScript will indeed run,
# with the use of jQuery's .ready and .getScript that also verifies the JavaScript is syntactically correct.
# If it is correct to the browser's JavaScript engine, the console.log will successfully print to the browser's console.

global direct_global_var

def output(name):
# With this New Feature: Open and Close Tags for this python file 
# (It allows syntax highlighting within the tags, and eases coding)
# Note that the following opening tag, (less-than sign and percent sign) will be replaced by the simple_preprocessor.
# with this:  PRINT training_wheels_bit_slower_to_remove(""" (lowercase) NOTE: this exact comment line obviously does not run.
	
	direct_global_var = 'planet earth, (mercury, venus) mars, etc'
	direct_local_var = 'hello world'
	local_var2 = 'hows it going'
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
<body><br> {**{direct_local_var}**}  {**{local_var2}**}  {**{direct_global_var}**}
<a href="{**{filename}**}">click to view pyThor page source</a><!-- similar to view source as feature of web browsers -->  <pre style="display:inline">{**{fullsource}**}</pre> <br> <a href="{**{fullsourcelink}**}">view full page source</a> <br>
<a href="index.php?pythorinfo">pyThorInfo</a> {**{pyThorinfo}**}  <!-- Display pyThor environment by a url get (variable) --> <!-- perhaps put this on different page -->
<br>{**{testing_output}**}<br>
<div id="container">

<div id="top">{**{top_content}**}</div>

<div id="mid">{**{mid_content}**}  <br>  <pre>{**{features}**}</pre>   </div>

<div id="end">{**{end_content}**}</div>

</div>

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

%>.format (   #  %:)>    # UNCOMMENT POINT *A* (uncomment the FIRST comment hash tag for the remove unicode operation   # the arbitrary find string is exactly this 20 characters long, quick workaround to subtract a parenthesis keyword operator # hap face keyword to rid a frown ( removes a close parenthesis ) (an arbitrary keyword created to remove one text character)
	# variables used
	top_content = top_content(),
	mid_content = mid_content(),
	end_content = end_content(),
	php_test    = php(code),  # just testing, remove if coding anything serious
	
	domain      = domain_name(name), # or something like whether a mobile device,
                                    # resolution information, etc. to select which css that fits	

testing_output = '', #this_is_a_test(),    # test of include file using quick tags python syntax


source_variable = source_code(),

example_htmlentities_string = <%  <p><hello world note p tags output><p>  %>.htmlentities(), # note, python quick tags stings have .htmlentities method

filename = os.path.basename(__file__).replace('_compiled.py', '.py'), # php filename witout extension

fullsource = get_fullsource(comments = True, pretags=True) if (QUERY_STRING == 'fullsource') else '' , 

# __formatvariable_stop = (  '*--END OF FULL SOURCE--*'.replace(' ', '_' ) ) if (QUERY_STRING == 'fullsource') else '',  #   or perhaps to name it   __sysexit()  to truncate at the substring (note use of __ variables NOT recommended)

 __formatvariable_range = ('*--START OF FULL SOURCE--*'.replace(' ', '_' ) , '*--END OF FULL SOURCE--*'.replace(' ', '_' )) if (QUERY_STRING == 'fullsource') else ('',''),

fullsourcelink = './index.php?fullsource',


# for demonstration purpose only, please remove the next line for production code (it is however a feature that is available at any time should you code it)
pyThorinfo = display_pythorinfo()  if (QUERY_STRING == 'pythorinfo') else '',   #remove this line to remove the url feature

features = display_features() if (QUERY_STRING == 'features') else ''

)


# display_superglobals()


# QUERY_STRING == 'fullsource&no_comments'  without comments


#  NOTE:  that within 


#.replace( '&amp;lt;%' , '&lt;%' ).replace( '%&amp;gt;', '%&gt;' )





 # %%>    # UNCOMMENT POINT *B* (uncomment the FIRST comment hash tag for the remove unicode operation)                                           

# html entities form of <% %> are to be used within python quick tags of <% %>     that     are       &lt;% %&gt;  at this time,  Note: this may be a concern, and htmlentities any string containing that will convert it to &amp;lt;% %&amp;gt;
# Therefore a feature to be implemented is to address that automatically for convenience

# statements marked by UNCOMMENT POINT *A* and *B* uncomment to remove unicode type quick python tags i.e., <unicode> </unicode>  though the contents in between the tags remain intact
#.unicode_markup()	# this is the method to remove the unicode type python quick tags, and give it a False argument
					# the utags wrapper already is automatically created
					# Usage:
					# place the keyword False in between .unicode_markup() parenthesis to remove the unicode type python quick tags,
					# i.e., to drop the <unicode> and </unicode> tags but not the contents,text between the tags
					# by giving the method unicode_markup() the argument of False it will remove the unicode tags
					# (by removing the argument or by setting it to True that is the same thing) the unicode tags remain intact.
					# (See front_compiled. in github commit #47 of this project that I specially modified to show a working usage example)
					# Otherwise, modify this latest version according to usage description
					
	# testing writing print statement to the web browser 
	# the intent is to create a python function to wrap the writing with print statements to the web browser's console
	code_init = <%
$name = 'Stan Switaj';
 
$fruits = array("banana", "apple", "strawberry", "pineaple");
 
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

	# Including an external python file that uses quick tags, (both open and close tags), and a format string variable syntax of {**{variable_name}**}
	
	s = (code_init + "\n" + console_log_function()  )
	
	# Escaping quotes seem to be the only small hassle from converting php source code to php source code within a python triple quoted string 
	# (due to the slightly obtuse (yet it works) situation of... running PHP then system calling python and within it, running PHP within a python triple quoted string)
	# therefore, NOTE: the extra backslash compared with the php version
	# this will convert it to the exact php, but I've no need of it at this time, though note the following variable name in the comments (the immediate next line)
	# string_to_write__NOT_DISPLAY_for_exact_PHP_equivalent_source_code = s.replace("#\\'#", "#'#").replace('#\\"\\"#', '#""#').replace("#\\'\\'#", "#''#")   # works, tested
	# The previous statement string (in the comments) can be used to write if desired to get the exact PHP equivalent that is different than the string used to output to the web page 
	# (due to an extra backslash required by python for quotes)

	
	# For convenience I've included it in the following write statement anyway (to get the exact equivalent to the PHP source code string)
	# The next line is optional to the OUTPUT to Web (i.e., it will not affect the display OUTPUT to web 
	# (only for the previously stated purpose. So it's just to inspect and review the string by writing it to a file)
	s = s.replace("#\\'#", "#'#").replace('#\\"\\"#', '#""#').replace("#\\'\\'#", "#''#") # comment this line out to view the exact string that gets OUTPUT to the web
	
	#to_write('testit.txt', s ) # uses to determine problematic characters only, can be removed, and to verify the contents of a php string by outputing to a file
	
	# TO OUTPUT to web
	print php(  s   )

	

#   notes:
#   https://sarfraznawaz.wordpress.com/2012/01/05/outputting-php-to-browser-console/
#   http://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists-in-python same as
#   to test variable existence http://stackoverflow.com/a/843293  otherwise .ini for initial options
#   nice unicode description: https://greeennotebook.wordpress.com/2014/05/24/character-sets-and-unicode-in-python/
#   perhaps something like this for pyQuickTags http://stackoverflow.com/a/3542763 then perhaps a <% %>.formatdirect() method for direct interpolation, a neat idea
