import os
import sys
from subprocess import PIPE, Popen, STDOUT
import time
import ast
import uuid

same_file = False	# is True or False , gets value from PHP (global or make App class due to        # Note, 2015.02.02: same_file set to True not recommended
                        # global variables frowned upon, i.e., not best practices)                   # because of the note comment explained in index.php
                        # began to import from PHP, still a todo, at this time
PRINTOUT = False	# for print statements used by print_test() to review variables, etc. for a form of browser console logging
					# 2015.01.30 added feature to allow python quick tags to triple quoted strings for assignment operators
					# triple quoted string can still be used, but not between <% and %> because they represent triple double quotes, and that would be
					# triple double quotes within triple double quotes (quotes within TDQ need to be escaped with the backslash)

print_literal = False

def findtags(open, close, s):
	t=[] #list,array,vector...
	idx=0
	item =''
	while(idx != -1):
	
		idx = s.find(open, idx)
		if idx == -1:
			#print 'break point #1 (open tag)'
			break;
			
		idx2 = s.find(close, idx+1)
		if idx2 == -1:
			#print 'break point #2 (close tag)'
			break;
			
		item = s[idx+len(open):idx2]
		t.append(item) # potential variable name
		#print 'result(' + item + ')'
		idx += 1
		item ='' # reset item
	return t
	
                  # utags will return the string with unicode type python quick tags ON as its initial value, by default.
                  # for convenience, the utags is a string object that creates a version of the source code when JavaScript is off as a transition until browser native implementation
class utags(str): # or unicode_show  ,  whichever is a more appropriate label

	def unicode_markup(self, bool=True):
		return self if bool else self.replace('<unicode>', '').replace('</unicode>','')

class Str_fv(str): # to allow text that appear as format variables
                   # that are not defined in the parameter list of the format method

	def format(self, *args, **kwargs):
		self  = self.replace('{', '{{').replace( '}', '}}')
		open  = '{{**{{'
		close = '}}**}}'
		var_names = findtags(open, close, self) # potential

		for item in kwargs:
			for it in var_names:	#lookup after this working...
				if  item == it:
					self = self.replace(	open+item+close ,  (open+item+close).replace(open, '{').replace(close, '}'  ) )
					continue
		#print self
		#to_write('str_fv_txt.py', self) # error checking
		
		return     str( self ).format(*args, **kwargs)  # note:  .format method converts  {{ to {
	
	#nice
	def to_write(self, file):
		with open(file, 'w') as fp:
			fp.write(self)

			
class pyQuickTags(str):
	
	str_fv = Str_fv()
	
	def __init__(self, v):        # optional
		#v = v.replace('{', '{{').replace('}', '}}').replace('{{**{{', '{').replace('}}**}}', '}')
		#self = v         
		#print self
		self.str_fv = Str_fv(v)
	
	
	def format(self, *args, **kwargs):
		#print 'hello out there'
	
		return self.str_fv.format(*args, **kwargs) # or init  str_fv()  at this point 
	

		#return     str( s ).format(*args, **kwargs)  # commented out
		#return super(pyQuickTags, self ).lower().format(*args, **kwargs)  # commented out
		# note, can wrap the super(pyQuickTags, self ) in a function e.g., something(super(str_fv, self )).format(*args, **kwargs)
		# or call an additional method as .lower does, etc.
		
	def to_print(self):
		print self
		
	def to_write(self, file):
		with open(file, 'w') as fp:
			fp.write(self)	
			
def rawstringify_outerquote(s):
    for format in ["r'{}'", 'r"{}"', "r'''{}'''", 'r"""{}"""']:
        rawstring = format.format(s)
        try:
            reparsed = ast.literal_eval(rawstring)
            if reparsed == s:
                return rawstring[1]
        except SyntaxError:
            pass
    raise ValueError('rawstringify received an invalid raw string')
	
def mod_dt(file):
	return time.strftime("%Y%m%d%H%M%S",time.localtime(os.path.getmtime(file)));
	
def to_write(file, s):
	with open(file, 'w') as fp:
		fp.write(s)					
					
def print_test(s):
	global PRINTOUT
	if (PRINTOUT):
		print s
		
def exists(path):
	return True if ( os.path.isfile(path) or os.path.isdir(path)) else False

def file_exists(path):
	return os.path.isfile(path)
	
def is_compiled(source, dest):

	if ( not file_exists(dest) ): # exists def nice, file_exists works fine too
		return False

	if ( mod_dt(source) >= mod_dt(dest) ):
		return False
	else:
		return True
		
def compile_include_quick_tags(file):
	global same_file
	
	if(not same_file):
		compiled = file[:-3] + '_compiled.py'
	else:
		compiled = file
	
	if ( is_compiled(file, compiled) ):
		#print '(INCLUDE ALREADY COMPILED)'
		return compiled
	
	print '(INCLUDE NOT compiled yet, therefore COMPILING)'
	
	os.system('"python.exe simple_preprocessor.py -TW '+file+' '+compiled+' whateverDNMfilterByoutputfunction 2>&1"')
	
	print_test( 'INCLUDING THIS FILE(' + compiled + ')' )
	return compiled # run pre_processor on it, with file being the source and  it as the dest
		
	# any includes done here to evaluate one file format variable, Q. can I include in a def,function
	
	
def include_quick_tags_file(source):
	global same_file
	
	print_test( 'POINT #1 file is:('+ source + ')' )
	f = os.path.abspath(compile_include_quick_tags(source)) # compiled variable
	print_test( '<br>file to include('+f+')' )
	
		# initially the idea was to compile here with the following statement:
		#execfile(compiled) # require fullpath, includes file   (though having a scope issue here)
				
	#if (same_file):
		# need to postprocessor.py the file after compiling
		# due to the way execfile currently works, cannot call from a def,function as I intend it to work (simply include)
	
	return f # hmm, how in -antastic is this, workaround needed by the receiver of this return when same file format is true


def execfile_fix(file): # workaround, due to execfile not working (as i'd like it to work (as expected)) from within a def,function
	global same_file
	
	if(same_file):
		os.system('"python.exe simple_postprocessor.py -TW '+file+' 2>&1"');


		
# INCLUDES TO BE PLACED HERE

file_to_include = 'include.py'
# including this way due to execfile does not including a file within a def,function as I expected
#execfile(include_quick_tags_file(file_to_include))	# this functin used to include each python file with quick tags		 


# NOTE: include section of source code with two entries due to workaround needed for execfile def,function
execfile(include_quick_tags_file(file_to_include))
execfile_fix(file_to_include) # when same file format is used, post_procesor.py (not used when using different file format)
                              # NOTE: fix does not need to be removed if using different file format (due to boolean check)
                              # otherwise, workaround is to convert after output() def called from main, with list of include files to convert back


def print_wwwlog(s, literal = True):    # prints to brower's console log
	
	if (literal):
		quote = rawstringify_outerquote(s)   # these 5 statements will occur when we turn on the  print_literal option
		if (quote == '"' ):                  # or    literal = True     
			s = s.replace('\\"', '"')        #
                                             # as of at this moment, it converts each print_wwwlog statement to
		if (quote == "'" ):                  # raw string literal with a new and innovative  simple_preprocessor_auto_print_literal.py  step
			s = s.replace("\\'", "'")        # the reason is to output messages to the brower console without escaping (actually its the most minimal escaping required)
                                             # see the comment about "TWO SMALL CASES TO ESCAPE WITH RAW STRING LITERALS" down below
											 
	# not to encode to ascii, better to use raw strings 
	#if (not esc_sequences_already):     # to get close to wysiwyg --   and perhaps innovative, Unicode tags proposed
	#	s = 'Lee: ' + s.encode('ascii')  # just to write lines, used during programming, statement can be removed
                                         # the way print_wwwlog() works is that it will either print ascii messages to the console or, you can escape characters, 
                                         # that will give you the same result, that will have to be interpreted anyway at the web browser as unicode,
                                         # perhaps put <unicode></unicode> and or <utf8></utf8> tags (and their uppercase forms) that I have arbitrarily innovated around utf8 strings to identify that.
		s = s.encode('hex')              # though perhaps browser's would identify that, or not, otherwise comment tags could be put around the unicode tags just mentioned <-- --> and javscript would convert to the required unicode text characters
		s = '<hex>'+s+'</hex>'           # if newlines actually needed, then there's use of html tags, e.g., <br> and so on... (perhaps even arbitrary tags for things like tabs <tabs> defined by css and so on...)
		
	code_init = <%
$name1 = '%s';
logConsole('$name1 var', $name1, true);
%> % s
	wwwout = code_init + "\n" + console_log_function()
	print php(  wwwout  ) # to web
					  					  
def print_args(s, intro=''):
	print_test( intro )
	for item in s:
		print_test( 'ARG:(' + item + ')' )
		
def create_superglobals(args):
	global same_file
	# idea to transfer superglobals from PHP here
	
               # experimental, just testing PHP called within Python
def php(code): # shell execute PHP from Python (that is being called from php5_module in Apache), for fun...
	p = Popen(['php'], stdout=PIPE, stdin=PIPE, stderr=STDOUT) # open process
	o = p.communicate('<?php '+ code +'\n ?>')[0]
	try:
		os.kill(p.pid, signal.SIGTERM)	# kill process
	except:
		pass
	return o

def top_content():
    
	print_wwwlog( '''I am at " the top " content''' ) # NOTE: better to use triple single quotes , best to put a space before and after a triple quoted string (though not necessary for triple SINGLE quotes)
	                                                  # (the open and close quick tags (< % % > with no spaces) to denote a 
                                                      # triple double quoted string ONLY for return and assignment statements at this time) 
                                                      # due to a space needed before closing parenthesis 
                                                      # when using triple DOUBLE quotes (no restriction with triple SINGLE quotes by you, the programmer)
	# at this time, one or no spaces between open parenthesis and open quick tag (no resriction on the close python quick tag as far as spaces around it)
	print_wwwlog ( <% example of new feature using quick tags between parenthesis %> )
	
	return ' pyThor    @    www.pythor.us '
	
def mid_content():

	print_wwwlog( r'''I am " at """" \'\'\'\'\'\'\'{}{}{}{} {{{{ }}}} the middle content \a\1\2\3\4\5\6\7\8\9\b\f\v\r\n\t\0\x0B
	
	
I have denoted newlines within a raw string , sent to the web browser that also interprets as newlines
And saving the file also is fine.

<br>
<br>
hello world  (but html characters are not interpreted this way)
'''    )  # TWO SMALL CASES TO ESCAPE WITH RAW STRING LITERALS, a backslash before a single quote or double quote 
          # (depending what are the outer quotes) and if the intent is to have a backslash at the end of a string, need two of them

	return <%
	
This is a test, <br>it is actually within a triple double quoted string
{**{testing}**}
%>.format( testing = 'HELLO WORLD(testing)' )
	
def end_content():
	return 'footer'
	
# in the case not transferring data from php using multiple domains, simply revert to a previous version, commit 
def domain_name(s):   
	if(s == 'A'):
		return 'us'
	elif(s == 'WIDE'):
		return 'com'

# no longer using due to pyQuickTags class,object replaces this function
def training_wheels_bit_slower_to_remove(s): # recommend: to remove this function for production code and edit code as required
                                             # just chose an arbitrary tag to represent the python format variables, works nicely, for now
	return s.replace('{', '{{').replace('}', '}}').replace('{{**{{', '{').replace('}}**}}', '}')

# test example, don't forget to have php.exe and php5ts.dll in PATH
width = 100
height = 100
code = <%

echo ('   {**{php_width}**}, {**{php_height}**}  ');

%>.format( php_width = str(width) , php_height = str(height) )

# Note, any JavaScript or any other code that contains a curly brace 
# must double the curly brace when using the python format function with the triple double-quoted string, 
# but not in a JavaScript src file (regardless of using the format function or not).

# It further verifies that the compiled Python-like RapydScript JavaScript will indeed run,
# with the use of jQuery's .ready and .getScript that also verifies the JavaScript is syntactically correct.
# If it is correct to the browser's JavaScript engine, the console.log will successfully print to the browser's console.


def output(name):
# With this New Feature: Open and Close Tags for this Python file 
# (It allows syntax highlighting within the tags, and eases coding)
# Note that the following opening tag, (less-than sign and percent sign) will be replaced by the simple_preprocessor.py
# with this:  PRINT training_wheels_bit_slower_to_remove(""" (lowercase) NOTE: this exact comment line obviously does not run.
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
<body>
<br>{**{testing_output}**}<br>
<div id="container">

<div id="top">{**{top_content}**}</div>

<div id="mid">{**{mid_content}**}</div>

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

<pre>

{**{source_variable}**}
''' triple single quotes allowed also '''
""" triple double quotes now allowed within python quick tags, feature added 2015.02.08 """

While still compatible with being able to use python format variables,
{**{ python quick tags format variable now as wysiwyg text when undefined in format method parameters, feature added 2015.02.16 }**}



</pre>

%>.format (   #  %:)>    # UNCOMMENT POINT *A* (uncomment the FIRST comment hash tag for the remove unicode operation   # the arbitrary find string is exactly this 20 characters long, quick workaround to subtract a parenthesis keyword operator # happy face keyword to rid a frown ( removes a close parenthesis ) (an arbitrary keyword created to remove one text character)
	# variables used
	top_content = top_content(),
	mid_content = mid_content(),
	end_content = end_content(),
	php_test    = php(code),  # just testing, remove if coding anything serious
	
	domain      = domain_name(name), # or something like whether a mobile device,
                                     # resolution information, etc. to select which css that fits	

testing_output = this_is_a_test(),    # test of include file using quick tags python syntax


source_variable = source_code_output()

) # %%>    # UNCOMMENT POINT *B* (uncomment the FIRST comment hash tag for the remove unicode operation)                                           

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
					# (See front_compiled.py in github commit #47 of this project that I specially modified to show a working usage example)
					# Otherwise, modify this latest version according to usage description
					
	# testing writing print statement to the web browser 
	# the intent is to create a python function to wrap the writing with print statements to the web browser's console
	code_init = <%
$name = 'Stan Switaj';
 
$fruits = array("banana", "apple", "strawberry", "pineaple");
 
$user = new stdClass;
$user->name = 'Hello 123.00 \\a\\1\\2\\3\\4\\5\\6\\7\\8\\9\\b\\f\\v\\r\\n\\t\\0\\x0B ';
$user->desig = "CEO";
$user->lang = "PHP Running Through subprocess (Python)";
$user->purpose = "To print log messages to the browser console messages to the browser";
 var_dump($fruits);
logConsole('$name var', $name, true);
logConsole('An array of fruits', $fruits, true);
logConsole('$user object', $user, true);
%>


	# Written to print to the console log of a web browser

	# Including an external python file that uses quick tags, (both open and close tags), and a format string variable syntax of {**{variable_name}**}
	
	s = (code_init + "\n" + console_log_function()  )
	
	# Escaping quotes seem to be the only small hassle from converting php source code to php source code within a python triple quoted string 
	# (due to the slightly obtuse (yet it works) situation of... running PHP then system calling Python and within it, running PHP within a python triple quoted string)
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
	
	# Sidenote: I did update the original regex and removed the \s to allow spaces and its noteworthy that it only needs one backslash to escape the string
	# as well as extended the regex just for demonstration to cover the escape characters commonly used
	# this is how the original regex should be escaped:     '#[\s\\r\\n\\t\\0\\x0B]+#'       and works (note remove the \s to allow spaces) 

	# TO OUTPUT to web
	print php(  s   )


	# ALSO NOTE: On the line immediately starting with the (percent sign and greater-than sign), this is the closing tag
	# gets replaced back to (triple double quotes and open parenthesis, in the situation when the same_format is set to true)

if __name__ == "__main__":  # in the case not transferring data from php, then simply revert to a previous version, commit
	create_superglobals(sys.argv)
	print_args(sys.argv, '<br>HERE front.py '+'<br>')
	
	if( not len(sys.argv) >= 2 ):
		print "argument is required, which domain name from the initial, starting PHP"
		sys.exit(1)
		
	output(name=sys.argv[1])


	
	
#   https://sarfraznawaz.wordpress.com/2012/01/05/outputting-php-to-browser-console/
#   http://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists-in-python same as
#   to test variable existence http://stackoverflow.com/a/843293  otherwise .ini for initial options
#   nice unicode description: https://greeennotebook.wordpress.com/2014/05/24/character-sets-and-unicode-in-python/
