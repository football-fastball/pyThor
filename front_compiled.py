


import os
import sys
from subprocess import PIPE, Popen, STDOUT
import time
import ast
import uuid
import json


global pyGET
global pyPOST
global pySERVER
global pyFILES

global ensure							   # set to True initially, for a slight speed increase set to False, This is a variable name check of PHP to pyThor superglobal variables
ensure = True							   # this is to verify that the variable from the PHP superglobal variable are the variables by their name (string comparison)
										   #
										   # when an update to a new PHP version occurs, 
										   # any new variable (from a PHP upgrade) to pyThor (i.e., not a convenience variable yet) 
										   # then be sure to use the function   exists('' , pySERVER)  when accessing it each time  (this guarentees it is there)

global warn_when_new_php_variables
warn_when_new_php_variables = True         # when an update to a new PHP version occurs, this will warn that a convenience varible does not exist for it, 
                                           # note that this is just a warning and can be turned off (set to False) and that this variable will ALWAYS (in any case) be available from the pySERVER variable (though Note: when it is a new variable be sure to check that it exists in pySERVER with the exists( 'var', pySERVER) function (due to convenience variable not initializing it if its not there (internal: i.e., sent over from php every time) ) 
										   # (if warnings do occur, i.e., a new variable occurs from a PHP upgrade, an upgrade to latest pyThor version is recommended (or if not upgrading pyThor at this time)
										   # then accessing the new variable from pySERVER superglobal variable is fine too)
										   
pyGET={};pyPOST={};pySERVER={};pyFILES={}  # main superglobal variables (accessible similar to how they are from PHP source code)


# Apache Environment ( each variable within pySERVER the "PHP Variables" from PHP $_SERVER ) # available for use
# for the variables, e.g., DOCUMENT_ROOT
# (these are) convenience variables
global HTTP_HOST;global HTTP_USER_AGENT;global HTTP_ACCEPT;global HTTP_ACCEPT_LANGUAGE;global HTTP_ACCEPT_ENCODING;
global HTTP_CONNECTION;global PATH;global SystemRoot;global COMSPEC;global PATHEXT;global WINDIR;global SERVER_SIGNATURE;
global SERVER_SOFTWARE;global SERVER_NAME;
global SERVER_ADDR;global SERVER_PORT;global REMOTE_ADDR;global DOCUMENT_ROOT;global REQUEST_SCHEME;global CONTEXT_PREFIX;
global CONTEXT_DOCUMENT_ROOT;global SERVER_ADMIN;global SCRIPT_FILENAME;global REMOTE_PORT;global GATEWAY_INTERFACE;
global SERVER_PROTOCOL;global REQUEST_METHOD;global QUERY_STRING;global REQUEST_URI;global SCRIPT_NAME;global PHP_SELF;
global REQUEST_TIME_FLOAT;global REQUEST_TIME;

# tempormental variables ( sometimes received,  though ALWAYS initialized )
global HTTP_CACHE_CONTROL;global HTTP_REFERER;


# These variables are automatically populated by the create_superglobals function, please do NOT edit them!
# Note that these variable are available for use throughout your website source code (program), Enjoy!
HTTP_HOST='';HTTP_USER_AGENT='';HTTP_ACCEPT='';HTTP_ACCEPT_LANGUAGE='';HTTP_ACCEPT_ENCODING='';
HTTP_CONNECTION='';PATH='';SystemRoot='';COMSPEC='';PATHEXT='';WINDIR='';SERVER_SIGNATURE='';
SERVER_SOFTWARE='';SERVER_NAME='';
SERVER_ADDR='';SERVER_PORT='';REMOTE_ADDR='';DOCUMENT_ROOT='';REQUEST_SCHEME='';CONTEXT_PREFIX='';
CONTEXT_DOCUMENT_ROOT='';SERVER_ADMIN='';SCRIPT_FILENAME='';REMOTE_PORT='';GATEWAY_INTERFACE='';
SERVER_PROTOCOL='';REQUEST_METHOD='';QUERY_STRING='';REQUEST_URI='';SCRIPT_NAME='';PHP_SELF='';
REQUEST_TIME_FLOAT='';REQUEST_TIME='';
HTTP_CACHE_CONTROL='';HTTP_REFERER='';



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

def make_tuples(s):		# for direct format variables using python quick tags {**{  }**}

	fv = []

	start = 0
	pos   = 0  # or idx

	while (1):

		pos = s.find( '{**{', pos )

		if (pos == -1):
			break
		else:
			pos += 4
			start = pos
			pos = s.find( '}**}', pos )
			fv.append( s[start:pos]  )  # (start, pos)
			pos += 4
			
	return fv		

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
		#to_write('str_fv_txt.', self) # error checking
		
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

		# perhaps a direct find   ------------- to do next !!!
		#val = ''
		#for name, value in kwargs.items():
		#	if ( '__formatvariable_stop' == name):
		#		val = value
		#		print 'value is:' + val + '<br>'
		#		break ################################## anyway the   direct find     !
		
		opentag=''
		closetag=''
		if '__formatvariable_stop' in kwargs:  # note: opentag not used 
			closetag = kwargs.get('__formatvariable_stop')
		
		if '__formatvariable_range' in kwargs:
			tuple = kwargs.get('__formatvariable_range')		
			opentag  = tuple[0]
			closetag = tuple[1]

		return pyQuickTags( self.str_fv.format(*args, **kwargs) ).fullsource_truncate(startfullsource_substring = opentag, endfullsource_substring = closetag)   # or init  str_fv()  at this point
	

		#return     str( s ).format(*args, **kwargs)  # commented out
		#return super(QuickTags, self ).lower().format(*args, **kwargs)  # commented out
		# note, can wrap the super(QuickTags, self ) in a function e.g., something(super(str_fv, self )).format(*args, **kwargs)
		# or call an additional method as .lower does, etc.
	
	def fullsource_truncate(self, startfullsource_substring, endfullsource_substring):
		
		startpos = self.find(startfullsource_substring)
		
		endpos = self.find(endfullsource_substring) # already found (or to end of string)

		if (startfullsource_substring == ''):	    # NOT the same as     startpos == -1
			startpos = 0
		
		msg=''
		if (endfullsource_substring   == ''):       # NOT the same as       endpos == -1
			endpos = len(self)
		else:
			msg = '<br>Full Source Code Display Done. <br>NOTE: early exit from a truncate of an end of full source substring<br><br>'
		

		return pyQuickTags(self[startpos+len(startfullsource_substring):endpos]   +  msg  )  # update: fix 03-03-2015  parenthesis required outside the string, otherwise htmlentities and additional pyQuickTag methods are not available due to a conversion to a str string from a pyQuickTags string
																			   #.to_file('justtosee.txt')  # I append this to the pyQuickTags at that point, (one line up) to then view what the data is at that point
	
	def initsupers(self, *args):
		
		format_vars = make_tuples(self)

		for item in format_vars:

			data = args[0].get(item)  # locals
			if type(data) is str and data:
				self = self.replace( '{**{'+item+'}**}' , data )
			elif data is None:
				pass
			elif type(data) is int:
				self = self.replace( '{**{'+item+'}**}' , str(data) )
			elif type(data) is float:
				self = self.replace( '{**{'+item+'}**}' , str(data) )
			#else:
			#	print '(' + data + ')<br>'

				
			data = args[1].get(item)  # globals
			if type(data) is str and data:
				self = self.replace( '{**{'+item+'}**}' , data )
			elif data is None:
				pass
			elif type(data) is not int and type(data) is not float:
				self = self.replace( '{**{'+item+'}**}' , str(data) )
			#else:
			#	print '(' + data + ')<br>'

		return pyQuickTags(self)
		
		
	def htmlentities(self):
	
		salt = uuid.uuid4().hex
		s = self.replace('&quot;&quot;&quot;', '*QUOT-*-QUOT-*-QUOT*'+salt)
		s = s.replace("'",  '*apos-*'+salt)
		s = s.replace(r'\\', '*slash-*'+salt)
		
		code_init = pyQuickTags(r""" echo htmlentities('%s'); """).initsupers(locals(),globals())  %  s   # or r"""   """
		var = php(code_init)

		var = var.replace('*QUOT-*-QUOT-*-QUOT*'+salt, '&quot;&quot;&quot;')		
		var = var.replace( '*apos-*'+salt,  "'")
		var = var.replace( '*slash-*'+salt, r'\\')
		
		var = var.replace( '&amp;lt;%' , '&lt;%' ).replace( '%&amp;gt;', '%&gt;' ) # perhaps salt quick tags too
		
		return pyQuickTags(var)		#return var # this ok, perhaps to wrap return with QuickTags() to then allow another method call
		

	def encodehex(self):
		return pyQuickTags( str(self).encode('hex') )

	def encode(self, how): # or  *args, **kwargs
		return pyQuickTags( str(self).encode(how) ) # i,e., 'hex'
		
	def to_file(self, file):
		with open(file, 'w') as fp:
			fp.write(self)
		return pyQuickTags(self)
			
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
	



# compiler functions
def mod_dt(file):
	return time.strftime("%Y%m%d%H%M%S",time.localtime(os.path.getmtime(file)));

							   # dual-purpose naming of a function is not recommended		e.g., (  distinct function names,  kexists (for key exists) or key_exists() , fexists (for file or folder exists) or filefolder_exists(), etc.  )
def exists(arg1, object=''):   # an interesting function   2 argument defines this as a key check to an object (primary) , purpose
							   #
							   #                           1 argument it is a file or folder exists check      (secondary) (distinct based on variable count, therefore no implicit variables in this function)

	if (object == ''): # therefore 1 argument
		return True if ( os.path.isfile(arg1) or os.path.isdir(arg1)) else False   # arg1 is a path (of a file or folder path)
	
	else:              # therefore 2 arguments, this is the key check to an object (e.g., new variable nam contained in pySERVER check)
		if arg1 in object:
			#    when_true                   when_false
			return True if arg1 in object else False
			#
			# if arg1 in object:
			#	return True
			# else:
			#	return False
	
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

	compiled = file[:-3] + '_compiled.py'
	
	if ( is_compiled(file, compiled) ):
		#print '(INCLUDE ALREADY COMPILED)'
		return compiled
	
	print '(INCLUDE NOT compiled yet, therefore COMPILING)'
	
	os.system('"python.exe simple_preprocessor.py -I '+file+' '+compiled+' 2>&1"')
	
	print( 'INCLUDING THIS FILE(' + compiled + ')' )
	return compiled # run pre_processor on it, with file being the source and  it as the dest
		
	# any includes done here to evaluate one file format variable, Q. can I include in a def,function
	
	
def include_quick_tags_file(source):

	print( 'POINT #1 file is:('+ source + ')' )
	f = os.path.abspath(compile_include_quick_tags(source)) # compiled variable
	print( '<br>file to include('+f+')' )
	
	# initially the idea was to compile here with the following statement:
	#execfile(compiled) # require fullpath, includes file   (though having a scope issue here)
				
	return f # hmm, how in -antastic is this, workaround needed by the receiver of this return when same file format is true

	
	

def print_wwwlog(s, literal = True):    # prints to brower's console log
	
	if (literal):
		quote = rawstringify_outerquote(s)   # these 5 statements will occur when we turn on the  print_literal option
		if (quote == '"' ):                  # or    literal = True
			s = s.replace('\\"', '"')        #
                                             # as of at this moment, it converts each print_wwwlog statement to
		if (quote == "'" ):                  # raw string literal with a new and innovative  simple_preprocessor_auto_print_literal.  step
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
		
	code_init = pyQuickTags(r"""
$name1 = '%s';
logConsole('$name1 var', $name1, true);
""").initsupers(locals(),globals()) % s
	wwwout = code_init + "\n" + console_log_function()
	print php(  wwwout  ) # to web


def php(code): # shell execute PHP from python (that is being called from php5_module in Apache), for fun...
	p = Popen(['php'], stdout=PIPE, stdin=PIPE, stderr=STDOUT) # open process
	o = p.communicate('<?php '+ code )[0]      # updated, removing closing tag solution 02-21-201
	try:
		os.kill(p.pid, signal.SIGTERM)	# kill process
	except:
		pass
	return o	

	
def source_code_from_file(file):
	
	source=''   # note: can r' ' string a full path to enter a string as text as string literals due to special characters, i.e., the backslash https://docs.python.org/2/reference/lexical_analysis.html#string-literals
	with open(file, 'r') as fp:   # or .cpp .php  etc.
		source = fp.read()
		source = source.replace('"""', '&quot;&quot;&quot;')            # note: added 02-20-2015
		
	return pyQuickTags(r"""	
	
{**{source_variable}**}

""").initsupers(locals(),globals()).format( source_variable = source ).htmlentities()   # when htmlentities not needed, then either remove the .htmlentities method, different function name with different code, (perhaps an override local function (w/same name) in website source, (though this override technique could cause confusion) ), or a htmlentities with a boolean arg,parameter version, etc.




def geturldecode_php(s):
	
	code_init = r""" echo htmlentities('{geturl}');""".format( geturl = s )   # or r"""   """
	return php(code_init)
	
def exit_program(var):
	print 'early exit, ensure verified, variable name different, at the variable: ' + var + '<br>'
	sys.exit(1)


def read_superglobalvariable_file(file):
	
	with open(file, 'r') as fp:
		arr = fp.read().splitlines()
		#arr[1] = '' if (arr[1]=='[]') else arr[1] #sanitizes, otherwise additional or to a function...
		#arr[2] = '' if (arr[2]=='[]') else arr[2] #...
		#arr[3] = '' if (arr[3]=='[]') else arr[3] #...		
	return ( arr[0], arr[1], arr[2], arr[3] )

	
def to_str(s): # from '' or []
	return '' if ( s == '[]' ) else s
	
def create_superglobals(args):
	
	global pySERVER  # only to edit, readonly is accessible
	global pyGET
	global pyPOST
	global pyFILES


	
	if sys.argv[2] == 'file': # i.e., > 8000 in length ( workaround dos prompt limit via passthru )
	
		print 'file mode workaround' + '<br>'    # perhaps virtual in-memory file solution (to this) 
		
		file = sys.argv[3]
		print 'file received is: ' + file + '\n'
		arr = read_superglobalvariable_file(file)

		print 'arr0:'+ arr[0] + '<br>'     # pySERVER
		print 'arr1:'+ arr[1] + '<br>'     # pyGET
		print 'arr2:'+ arr[2] + '<br>'     # pyPOST
		print 'arr3:'+ arr[3] + '<br>'     # pyFILES
		

		data     = json.loads( arr[0] )  # from a file, first line         # could directly load to pySERVER
		pyGET    = json.loads( arr[1] ) if not(to_str(arr[1])=='') else {} # in case its an empty string       (   previous code:  # if arr[1]=='' else {}      )
		pyPOST   = json.loads( arr[2] ) if not(to_str(arr[2])=='') else {}
		pyFILES  = json.loads( arr[3] ) if not(to_str(arr[3])=='') else {}
	
	else:
										 # from dos prompt args sequence (received as string type)
		data     = json.loads( sys.argv[2].decode('hex') ) # could directly load to pySERVER (but going to ensure both pySERVER contents and convenience variables same data (and also verify that at minimum are presumed to exist) )
		pyGET    = json.loads( sys.argv[3].decode('hex') ) if not(to_str(sys.argv[3].decode('hex'))=='') else {} # when received as   5b5d  (its hex version of an empty string)  , empty string '' converted then to a {}
		pyPOST   = json.loads( sys.argv[4].decode('hex') ) if not(to_str(sys.argv[4].decode('hex'))=='') else {} # when received as   5b5d  (its hex version of an empty string)  , empty string '' converted then to a {}
		pyFILES  = json.loads( sys.argv[5].decode('hex') ) if not(to_str(sys.argv[5].decode('hex'))=='') else {} # when received as   5b5d  (its hex version of an empty string)  , empty string '' converted then to a {}
		
		
	
	##### e.g.,   global QUERY_STRING  only to edit, readonly is accessible (works different in PHP)
	
	global warn_when_new_php_variables
	
	#json encoded order
	global REQUEST_TIME;       global CONTEXT_DOCUMENT_ROOT; global SERVER_SOFTWARE;  
	global CONTEXT_PREFIX;     global SERVER_SIGNATURE;      global REQUEST_METHOD;
	global SystemRoot;         global QUERY_STRING;          global PATH;
	global HTTP_USER_AGENT;    global HTTP_CONNECTION;       global PHP_SELF;        global SERVER_NAME;
	global REMOTE_ADDR;        global SERVER_PROTOCOL;       global SERVER_PORT;     global SERVER_ADDR;
	global DOCUMENT_ROOT;      global COMSPEC;               global SCRIPT_FILENAME; global SERVER_ADMIN;
	global HTTP_HOST;          global SCRIPT_NAME;           global PATHEXT;         global REQUEST_URI;
	global HTTP_ACCEPT;        global WINDIR;				 global GATEWAY_INTERFACE;
	global REMOTE_PORT;        global HTTP_ACCEPT_LANGUAGE;  global REQUEST_SCHEME;
	global REQUEST_TIME_FLOAT; global HTTP_ACCEPT_ENCODING;
	global HTTP_CACHE_CONTROL; global HTTP_REFERER;
	
	
	

	for var_name, item in data.items(): # to populate the data structure, dict
		pySERVER[var_name] = item
		

	
	# this is to assign the variable names to indices, to do unable at this time to assign string variable names to the variables directly
	# therefore, this is the purpose for the   ensure   variable
	server_variables = { 	
'REQUEST_TIME':0, 'CONTEXT_DOCUMENT_ROOT':1,'SERVER_SOFTWARE':2, 'CONTEXT_PREFIX':3, 'SERVER_SIGNATURE':4,
'REQUEST_METHOD':5,'SystemRoot':6,'QUERY_STRING':7,'PATH':8,'HTTP_USER_AGENT':9,'HTTP_CONNECTION':10,
'PHP_SELF':11,'SERVER_NAME':12,'REMOTE_ADDR':13,'SERVER_PROTOCOL':14,'SERVER_PORT':15,'SERVER_ADDR':16,
'DOCUMENT_ROOT':17,'COMSPEC':18,'SCRIPT_FILENAME':19,'SERVER_ADMIN':20,'HTTP_HOST':21,'SCRIPT_NAME':22,
'PATHEXT':23,'HTTP_CACHE_CONTROL':24,'REQUEST_URI':25,'HTTP_ACCEPT':26,'WINDIR':27,'GATEWAY_INTERFACE':28,
'REMOTE_PORT':29,'HTTP_ACCEPT_LANGUAGE':30,'REQUEST_SCHEME':31,'REQUEST_TIME_FLOAT':32,'HTTP_ACCEPT_ENCODING':33,
'HTTP_REFERER':34
}


	
	for var_name, item in data.items():

		if var_name in server_variables:
			x = server_variables[var_name]
		else:
			if (warn_when_new_php_variables):
				print '<br>WARNING: Note that this variable is accessible through the pySERVER superglobal variable only at this time('+var_name+')' +'<br>'
			continue
			
		if (ensure): #verifies again
		
			if   (x == 0):
				REQUEST_TIME         = item if (var_name == 'REQUEST_TIME' )         else exit_program('REQUEST_TIME')
			elif (x == 1):
				CONTEXT_DOCUMENT_ROOT = item if (var_name == 'CONTEXT_DOCUMENT_ROOT') else exit_program('CONTEXT_DOCUMENT_ROOT')
			elif (x == 2):
				SERVER_SOFTWARE      = item if (var_name == 'SERVER_SOFTWARE' )      else exit_program('SERVER_SOFTWARE')
			elif (x == 3):
				CONTEXT_PREFIX       = item if (var_name == 'CONTEXT_PREFIX' )       else exit_program('CONTEXT_PREFIX')
			elif (x == 4):
				SERVER_SIGNATURE     = item if (var_name == 'SERVER_SIGNATURE' )     else exit_program('SERVER_SIGNATURE')
			elif (x == 5):
				REQUEST_METHOD       = item if (var_name == 'REQUEST_METHOD' )       else exit_program('REQUEST_METHOD')
			elif (x == 6):
				SystemRoot           = item if (var_name == 'SystemRoot' )           else exit_program('SystemRoot')
			elif (x == 7):
				QUERY_STRING         = item if (var_name == 'QUERY_STRING' )         else exit_program('QUERY_STRING')
			elif (x == 8):
				PATH                 = item if (var_name == 'PATH' )                 else exit_program('PATH')
			elif (x == 9):
				HTTP_USER_AGENT      = item if (var_name == 'HTTP_USER_AGENT' )      else exit_program('HTTP_USER_AGENT')
			elif (x == 10):
				HTTP_CONNECTION      = item if (var_name == 'HTTP_CONNECTION' )      else exit_program('HTTP_CONNECTION')
			elif (x == 11):
				PHP_SELF             = item if (var_name == 'PHP_SELF' )             else exit_program('PHP_SELF')
			elif (x == 12):
				SERVER_NAME          = item if (var_name == 'SERVER_NAME' )          else exit_program('SERVER_NAME')
			elif (x == 13):
				REMOTE_ADDR          = item if (var_name == 'REMOTE_ADDR' )          else exit_program('REMOTE_ADDR')
			elif (x == 14):
				SERVER_PROTOCOL      = item if (var_name == 'SERVER_PROTOCOL' )      else exit_program('SERVER_PROTOCOL')
			elif (x == 15):
				SERVER_PORT          = item if (var_name == 'SERVER_PORT' )          else exit_program('SERVER_PORT')
			elif (x == 16):
				SERVER_ADDR          = item if (var_name == 'SERVER_ADDR' )          else exit_program('SERVER_ADDR')
			elif (x == 17):
				DOCUMENT_ROOT        = item if (var_name == 'DOCUMENT_ROOT' )        else exit_program('DOCUMENT_ROOT')
			elif (x == 18):
				COMSPEC              = item if (var_name == 'COMSPEC' )              else exit_program('COMSPEC')
			elif (x == 19):
				SCRIPT_FILENAME      = item if (var_name == 'SCRIPT_FILENAME' )      else exit_program('SCRIPT_FILENAME')
			elif (x == 20):
				SERVER_ADMIN         = item if (var_name == 'SERVER_ADMIN' )         else exit_program('SERVER_ADMIN')
			elif (x == 21):
				HTTP_HOST            = item if (var_name == 'HTTP_HOST' )            else exit_program('HTTP_HOST')
			elif (x == 22):
				SCRIPT_NAME          = item if (var_name == 'SCRIPT_NAME' )          else exit_program('SCRIPT_NAME')
			elif (x == 23):
				PATHEXT              = item if (var_name == 'PATHEXT' )              else exit_program('PATHEXT')
			elif (x == 24):
				HTTP_CACHE_CONTROL   = item if (var_name == 'HTTP_CACHE_CONTROL' )   else exit_program('HTTP_CACHE_CONTROL')
			elif (x == 25):
				REQUEST_URI          = item if (var_name == 'REQUEST_URI' )          else exit_program('REQUEST_URI')
			elif (x == 26):
				HTTP_ACCEPT          = item if (var_name == 'HTTP_ACCEPT' )          else exit_program('HTTP_ACCEPT')
			elif (x == 27):
				WINDIR               = item if (var_name == 'WINDIR' )               else exit_program('WINDIR')
			elif (x == 28):
				GATEWAY_INTERFACE    = item if (var_name == 'GATEWAY_INTERFACE' )    else exit_program('GATEWAY_INTERFACE')
			elif (x == 29):
				REMOTE_PORT 		 = item if (var_name == 'REMOTE_PORT' ) 		 else exit_program('REMOTE_PORT')
			elif (x == 30):
				HTTP_ACCEPT_LANGUAGE = item if (var_name == 'HTTP_ACCEPT_LANGUAGE' ) else exit_program('HTTP_ACCEPT_LANGUAGE')
			elif (x == 31):
				REQUEST_SCHEME       = item if (var_name == 'REQUEST_SCHEME' )       else exit_program('REQUEST_SCHEME')
			elif (x == 32):
				REQUEST_TIME_FLOAT   = item if (var_name == 'REQUEST_TIME_FLOAT' )   else exit_program('REQUEST_TIME_FLOAT')
			elif (x == 33):
				HTTP_ACCEPT_ENCODING = item if (var_name == 'HTTP_ACCEPT_ENCODING' ) else exit_program('HTTP_ACCEPT_ENCODING')
			elif (x == 34):
				HTTP_REFERER         = item if (var_name == 'HTTP_REFERER' )         else exit_program('HTTP_REFERER')
		else:
			if   (x == 0):
				REQUEST_TIME         = item
			elif (x == 1):
				CONTEXT_DOCUMENT_ROOT = item
			elif (x == 2):
				SERVER_SOFTWARE      = item 
			elif (x == 3):
				CONTEXT_PREFIX       = item 
			elif (x == 4):
				SERVER_SIGNATURE     = item 
			elif (x == 5):
				REQUEST_METHOD       = item 
			elif (x == 6):
				SystemRoot           = item 
			elif (x == 7):
				QUERY_STRING         = item 
			elif (x == 8):
				PATH                 = item 
			elif (x == 9):
				HTTP_USER_AGENT      = item 
			elif (x == 10):
				HTTP_CONNECTION      = item 
			elif (x == 11):
				PHP_SELF             = item 
			elif (x == 12):
				SERVER_NAME          = item 
			elif (x == 13):
				REMOTE_ADDR          = item 
			elif (x == 14):
				SERVER_PROTOCOL      = item 
			elif (x == 15):
				SERVER_PORT          = item 
			elif (x == 16):
				SERVER_ADDR          = item 
			elif (x == 17):
				DOCUMENT_ROOT        = item 
			elif (x == 18):
				COMSPEC              = item 
			elif (x == 19):
				SCRIPT_FILENAME      = item 
			elif (x == 20):
				SERVER_ADMIN         = item 
			elif (x == 21):
				HTTP_HOST            = item 
			elif (x == 22):
				SCRIPT_NAME          = item 
			elif (x == 23):
				PATHEXT              = item 
			elif (x == 24):
				HTTP_CACHE_CONTROL   = item 
			elif (x == 25):
				REQUEST_URI          = item 
			elif (x == 26):
				HTTP_ACCEPT          = item 
			elif (x == 27):
				WINDIR               = item 
			elif (x == 28):
				GATEWAY_INTERFACE    = item 
			elif (x == 29):
				REMOTE_PORT 		 = item 
			elif (x == 30):
				HTTP_ACCEPT_LANGUAGE = item 
			elif (x == 31):
				REQUEST_SCHEME       = item
			elif (x == 32):
				REQUEST_TIME_FLOAT   = item
			elif (x == 33):
				HTTP_ACCEPT_ENCODING = item
			elif (x == 34):
				HTTP_REFERER         = item

	#if (ensure):  # this would perhaps get a performance speedup (not recommended)
			# these are sort of  None  cases

		# mutually distinct therefore if without the elif  are fine  (perhaps a performance boost with the if elif )
		if 'REQUEST_TIME' not in pySERVER.keys():
				REQUEST_TIME                 = ''
				pySERVER['REQUEST_TIME']     = ''
		if 'CONTEXT_DOCUMENT_ROOT' not in pySERVER.keys():
				CONTEXT_DOCUMENT_ROOT             = ''
				pySERVER['CONTEXT_DOCUMENT_ROOT'] = ''
		if 'SERVER_SOFTWARE' not in pySERVER.keys():
				SERVER_SOFTWARE              = ''
				pySERVER['SERVER_SOFTWARE']  = ''
		if 'CONTEXT_PREFIX' not in pySERVER.keys():
				CONTEXT_PREFIX               = ''
				pySERVER['CONTEXT_PREFIX']   = ''
		if 'SERVER_SIGNATURE' not in pySERVER.keys():
				SERVER_SIGNATURE             = ''
				pySERVER['SERVER_SIGNATURE'] = ''
		if 'REQUEST_METHOD' not in pySERVER.keys():
				REQUEST_METHOD               = ''
				pySERVER['REQUEST_METHOD']   = ''
		if 'SystemRoot' not in pySERVER.keys():
				SystemRoot                   = ''
				pySERVER['SystemRoot']       = ''
		if 'QUERY_STRING' not in pySERVER.keys():
				QUERY_STRING                 = ''
				pySERVER['QUERY_STRING']     = ''
		if 'PATH' not in pySERVER.keys():
				PATH                         = ''
				pySERVER['PATH']             = ''
		if 'HTTP_USER_AGENT' not in pySERVER.keys():
				HTTP_USER_AGENT              = ''
				pySERVER['HTTP_USER_AGENT']  = ''
		if 'HTTP_CONNECTION' not in pySERVER.keys():
				HTTP_CONNECTION              = ''
				pySERVER['HTTP_CONNECTION']  = ''
		if 'PHP_SELF' not in pySERVER.keys():
				PHP_SELF                     = ''
				pySERVER['PHP_SELF']         = ''
		if 'SERVER_NAME' not in pySERVER.keys():
				SERVER_NAME                  = ''
				pySERVER['SERVER_NAME']      = ''
		if 'REMOTE_ADDR' not in pySERVER.keys():
				REMOTE_ADDR                  = ''
				pySERVER['REMOTE_ADDR']      = ''
		if 'SERVER_PROTOCOL' not in pySERVER.keys():
				SERVER_PROTOCOL              = ''
				pySERVER['SERVER_PROTOCOL']  = ''
		if 'SERVER_PORT' not in pySERVER.keys():
				SERVER_PORT                  = ''
				pySERVER['SERVER_PORT']      = ''
		if 'SERVER_ADDR' not in pySERVER.keys():
				SERVER_ADDR                  = ''
				pySERVER['SERVER_ADDR']      = ''
		if 'DOCUMENT_ROOT' not in pySERVER.keys():
				DOCUMENT_ROOT                = ''
				pySERVER['DOCUMENT_ROOT']    = ''
		if 'COMSPEC' not in pySERVER.keys():
				COMSPEC                      = ''
				pySERVER['COMSPEC']          = ''
		if 'SCRIPT_FILENAME' not in pySERVER.keys():
				SCRIPT_FILENAME              = ''
				pySERVER['SCRIPT_FILENAME']  = ''
		if 'SERVER_ADMIN' not in pySERVER.keys():
				SERVER_ADMIN                 = ''
				pySERVER['SERVER_ADMIN']     = ''
		if 'HTTP_HOST' not in pySERVER.keys():
				HTTP_HOST                    = ''
				pySERVER['HTTP_HOST']        = ''
		if 'SCRIPT_NAME' not in pySERVER.keys():
				SCRIPT_NAME                  = ''
				pySERVER['SCRIPT_NAME']      = ''
		if 'PATHEXT' not in pySERVER.keys():
				PATHEXT                      = ''
				pySERVER['PATHEXT']          = ''
		if 'HTTP_CACHE_CONTROL' not in pySERVER.keys():
				HTTP_CACHE_CONTROL               = ''
				pySERVER['HTTP_CACHE_CONTROL']   = ''
		if 'REQUEST_URI' not in pySERVER.keys():
				REQUEST_URI                      = ''
				pySERVER['REQUEST_URI']          = ''
		if 'HTTP_ACCEPT' not in pySERVER.keys():
				HTTP_ACCEPT                      = ''
				pySERVER['HTTP_ACCEPT']          = ''
		if 'WINDIR' not in pySERVER.keys():
				WINDIR                           = ''
				pySERVER['WINDIR']               = ''
		if 'GATEWAY_INTERFACE' not in pySERVER.keys():
				GATEWAY_INTERFACE                = ''
				pySERVER['GATEWAY_INTERFACE']    = ''
		if 'REMOTE_PORT' not in pySERVER.keys():
				REMOTE_PORT 		             = ''
				pySERVER['REMOTE_PORT']          = ''
		if 'HTTP_ACCEPT_LANGUAGE' not in pySERVER.keys():
				HTTP_ACCEPT_LANGUAGE             = ''
				pySERVER['HTTP_ACCEPT_LANGUAGE'] = ''
		if 'REQUEST_SCHEME' not in pySERVER.keys():
				REQUEST_SCHEME                   = ''
				pySERVER['REQUEST_SCHEME']       = ''
		if 'REQUEST_TIME_FLOAT' not in pySERVER.keys():
				REQUEST_TIME_FLOAT               = ''
				pySERVER['REQUEST_TIME_FLOAT']   = ''
		if 'HTTP_ACCEPT_ENCODING' not in pySERVER.keys():
				HTTP_ACCEPT_ENCODING             = ''
				pySERVER['HTTP_ACCEPT_ENCODING'] = ''
		if 'HTTP_REFERER' not in pySERVER.keys():
				HTTP_REFERER                     = ''
				pySERVER['HTTP_REFERER']         = ''

	#print 'early exit'
	#sys.exit(1)

	
#if 'key1' in dict.keys():
#  print "blah"
#else:
#  print "boo"
#	
	

		
def display_pythorinfo(): # pyThor_info()    display_superglobals()

	#global pySERVER      # only when editing...
	#global pyGET		  #...
	#global pyGET		  #...
	#global pyFILES		  #...
	
	out=''
 	
	apache_vars=['HTTP_HOST', 'HTTP_USER_AGENT', 'HTTP_ACCEPT', 'HTTP_ACCEPT_LANGUAGE', 'HTTP_ACCEPT_ENCODING', 
'HTTP_CONNECTION','HTTP_CACHE_CONTROL', 'PATH', 'SystemRoot', 'COMSPEC', 'PATHEXT', 'WINDIR', 'SERVER_SIGNATURE', 
'SERVER_SOFTWARE','SERVER_NAME', 'SERVER_ADDR', 'SERVER_PORT', 'REMOTE_ADDR', 'DOCUMENT_ROOT', 'REQUEST_SCHEME', 
'CONTEXT_PREFIX','CONTEXT_DOCUMENT_ROOT', 'SERVER_ADMIN', 'SCRIPT_FILENAME', 'REMOTE_PORT', 'GATEWAY_INTERFACE', 
'SERVER_PROTOCOL','REQUEST_METHOD', 'QUERY_STRING', 'REQUEST_URI', 'SCRIPT_NAME'  ]	
	
	out += pyQuickTags(r""" 
	<h1>Apache Envionment Variables </h1>
	
	<table border="1">
	""").initsupers(locals(),globals())	
	
	for item in apache_vars:
		out += pyQuickTags(r"""
		
			<tr>	<td> {**{name}**} </td>    <td> {**{value}**} </td>    </tr>
	
	""").initsupers(locals(),globals()).format( name = item , value = pySERVER[item] )                                 
	
	out += pyQuickTags(r"""	</table>	""").initsupers(locals(),globals())
	
	
	out += pyQuickTags(r""" 
		<h1>Printing the pySERVER superglobal variables</h1>
		<table border="1">
	""").initsupers(locals(),globals())
	
	for var_name, item in pySERVER.items():
		out += pyQuickTags(r"""
		
			<tr>	<td> {**{name}**} </td>    <td> {**{value}**} </td>    </tr>
	
	""").initsupers(locals(),globals()).format( name = var_name , value = item )    #   or something like    out += '<tr><td>'+var_name+'</td> <td>'+str( item )+'</td></tr>'
	
	out += pyQuickTags(r"""
		</table>
	""").initsupers(locals(),globals())
	
	
	
	out += pyQuickTags(r""" 
		<h1>Printing the pyGET superglobal variable contents</h1>
		<table border="1">
	""").initsupers(locals(),globals())
	
	for var_name, item in pyGET.items():
		out += pyQuickTags(r"""
		
			<tr>	<td> {**{name}**} </td>    <td> {**{value}**} </td>    </tr>
	
	""").initsupers(locals(),globals()).format( name = var_name , value = item )    #   or something like    out += '<tr><td>'+var_name+'</td> <td>'+str( item )+'</td></tr>'
	
	out += pyQuickTags(r"""	</table>	""").initsupers(locals(),globals())
	
	

	out += pyQuickTags(r""" 
		<h1>Printing the pyPOST superglobal variable contents</h1>
		<table border="1">
	""").initsupers(locals(),globals())

	
	for var_name, item in pyPOST.items():
		out += pyQuickTags(r"""
		
			<tr>	<td> {**{name}**} </td>    <td> {**{value}**} </td>    </tr>
	
	""").initsupers(locals(),globals()).format( name = var_name , value = item )    #   or something like    out += '<tr><td>'+var_name+'</td> <td>'+str( item )+'</td></tr>'
	
	out += pyQuickTags(r"""	</table>	""").initsupers(locals(),globals())
	
	
	out += pyQuickTags(r""" 
	<h1>Printing the pyFILES superglobal variable contents</h1>
	<table border="1">
	""").initsupers(locals(),globals())
	
	for var_name, item in pyFILES.items():
		out += pyQuickTags(r"""
		
			<tr>	<td> {**{name}**} </td>    <td> {**{value}**} </td>    </tr>
	
	""").initsupers(locals(),globals()).format( name = var_name , value = item )    #   or something like    out += '<tr><td>'+var_name+'</td> <td>'+str( item )+'</td></tr>'
	
	out += pyQuickTags(r"""	</table>	""").initsupers(locals(),globals())

	
	
	return out
	
# (exactly) from simple_preprocesor.py 
def get_string_tag_to_tag_read_source(file, start_tag, end_tag):  # same function to get_string_tag_to_tag the PHP version I wrote
	
	s=''
	with open( file, 'r' ) as fp:  #file pointer (of features file 
		s = fp.read()
	
	start = s.find(start_tag)
	
	if (start == -1):
		print 'early exit, could not find start_tag ' + start_tag + ' in file: ' + features_file + '<br>' 
		sys.exit(1)
		
	end = s.find(end_tag)
	
	if (end == -1):
		print 'early exit, could not find end_tag' + end_tag + ' in file: ' + features_file + '<br>'
	
	return s[start+len(start_tag):end]
	

def replace_when_yes(value, salted_opentag, salted_closetag,  bool_when,  salt_flavor):  # yes  as  true
	
	if (bool_when):
		return value.replace( salted_opentag, '<pre>' ).replace( salted_closetag, '</pre>' )
	else:
		return value
		
def get_fullsource(comments = True, pretags=False): # True initially
	
	salt = uuid.uuid4().hex
	
	#print '<br>'+ 'GET_FULLSOURCE' + '<br>'
	
	source = __file__ # compiled version _compiled.py  (note: not the current file, e.g.,  *_pyThor_features_txt.py )
	
	features_file = 'simple_preprocessor_pyThor_features_txt.py'	# test if feature file exists (should)
	
	opentag   = '# PYTHON QUICK TAGS FEATURES OPEN TAG #'.replace(' ','_')
	closetag  = '# PYTHON QUICK TAGS FEATURES CLOSE TAG #'.replace(' ','_')
	features  = get_string_tag_to_tag_read_source( features_file, opentag, closetag )
	
	opentag   = '# MAIN PROGRAM OPEN TAG #'.replace(' ','_')
	closetag  = '# MAIN PROGRAM CLOSE TAG #'.replace(' ','_')
	mainintro = get_string_tag_to_tag_read_source( features_file, opentag, closetag )
	
	source = source.replace('_compiled.py', '.py')
	

	with open(source, 'r') as rp:
		s = rp.read()
	
	out = '*--START OF FULL SOURCE--*'.replace(' ', '_')
	
	#        when_true                     when_false
	out += '*openpre-*'+salt  if (pretags) else   ''
	
	
	out += features + s + mainintro
	

	out += '*closepre-*'+salt if (pretags) else   ''
	
	out += '*--END OF FULL SOURCE--*'.replace(' ', '_')
	
	
	return replace_when_yes( pyQuickTags(out).htmlentities(), salted_opentag='*openpre-*'+salt, salted_closetag='*closepre-*'+salt, bool_when=pretags, salt_flavor = salt )


def display_features():

	features_file = 'simple_preprocessor_pyThor_features_txt.py'	# test if feature file exists (should)

	opentag   = '# FEATURES LIST OPEN TAG #'.replace(' ','_')
	closetag  = '# FEATURES LIST CLOSE TAG #'.replace(' ','_')
	features  = get_string_tag_to_tag_read_source( features_file, opentag, closetag )

	return pyQuickTags(features).htmlentities()
	
	
def print_args(s, intro=''):
	print( intro )
	for x, item in enumerate(s):
		print( 'ARG:'+str(x)+'(' + item + ')' ) + '<br>'
	
	
import os
import sys

  
# Internal are these functions that you can use, the source code to view is in the file  simple_preprocessor_pyThor_features_txt.py
#                                                   the compiled version is in the file  front_compiled.py
#                                                   for review

#  1)     python quick tags  print pyQuickTags(r"""  """).initsupers(locals(),globals())
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
	return pyQuickTags(r"""
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
	
""").initsupers(locals(),globals()).htmlentities()
	
def top_content():
    
	print_wwwlog( '''I am at " the top " content''' ) # NOTE: better to use triple single quotes , best to put a space before and after a triple quoted string (though not necessary for triple SINGLE quotes)
	                                                  # (the open and close quick tags (< % % > with no spaces) to denote a 
                                                      # triple double quoted string ONLY for return and assignment statements at this time) 
                                                      # due to a space needed before closing parenthesis 
                                                      # when using triple DOUBLE quotes (no restriction with triple SINGLE quotes by you, the programmer)
	# at this time, one or no spaces between open parenthesis and open quick tag (no resriction on the close python quick tag as far as spaces around it)
	print_wwwlog ( pyQuickTags(r""" example of new feature using quick tags between parenthesis """).initsupers(locals(),globals()) )
	
	return ' pyThor    @    www.pyThor.us '
	
def mid_content():

	print_wwwlog( pyQuickTags(r""" I am  at  '''''''{}{}{}{} {{{{ }}}} the middle content \a\1\2\3\4\5\6\7\8\9\b\f\v\r\n\t\0\x0B
	
	
I have denoted newlines within a raw string , sent to the web browser that also interprets as newlines
And saving the file also is fine.

<br>
<br>
hello world  (but html characters are not interpreted this way)
""").initsupers(locals(),globals())    )  # TWO SMALL CASES TO ESCAPE WITH RAW STRING LITERALS, a backslash before a single quote or double quote 
          # (depending what are the outer quotes) and if the intent is to have a backslash at the end of a string, need two of them

	return pyQuickTags(r"""
	 
{**{var_msg}**}

""").initsupers(locals(),globals()).format( var_msg = 'HELLO WORLD - PyThor for Web Programming' )
	 
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
code = pyQuickTags(r"""

echo ('   {**{php_width}**}, {**{php_height}**}  ');

""").initsupers(locals(),globals()).format( php_width = str(width) , php_height = str(height) )

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
	int_var = 1223344
	float_var = 5566778899.0
	print pyQuickTags(r"""

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
<body><br> {**{direct_local_var}**}  {**{local_var2}**}  {**{direct_global_var}**} {**{int_var}**} {**{float_var}**}
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

&quot;&quot;&quot; triple double quotes now allowed within python quick tags, feature added 2015.02.08 &quot;&quot;&quot;

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

""").initsupers(locals(),globals()).format (   #  %:)>    # UNCOMMENT POINT *A* (uncomment the FIRST comment hash tag for the remove unicode operation   # the arbitrary find string is exactly this 20 characters long, quick workaround to subtract a parenthesis keyword operator # hap face keyword to rid a frown ( removes a close parenthesis ) (an arbitrary keyword created to remove one text character)
	# variables used
	top_content = top_content(),
	mid_content = mid_content(),
	end_content = end_content(),
	php_test    = php(code),  # just testing, remove if coding anything serious
	
	domain      = domain_name(name), # or something like whether a mobile device,
                                    # resolution information, etc. to select which css that fits	

testing_output = '', #this_is_a_test(),    # test of include file using quick tags python syntax


source_variable = source_code(),

example_htmlentities_string = pyQuickTags(r"""  <p><hello world note p tags output><p>  """).initsupers(locals(),globals()).htmlentities(), # note, python quick tags stings have .htmlentities method

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





 # %""").initsupers(locals(),globals())    # UNCOMMENT POINT *B* (uncomment the FIRST comment hash tag for the remove unicode operation)                                           

# html entities form of print pyQuickTags(r""" """).initsupers(locals(),globals()) are to be used within python quick tags of print pyQuickTags(r""" """).initsupers(locals(),globals())     that     are       &lt;% %&gt;  at this time,  Note: this may be a concern, and htmlentities any string containing that will convert it to &amp;lt;% %&amp;gt;
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
	code_init = pyQuickTags(r"""
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
""").initsupers(locals(),globals())

 
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
#   perhaps something like this for pyQuickTags http://stackoverflow.com/a/3542763 then perhaps a print pyQuickTags(r""" """).initsupers(locals(),globals()).formatdirect() method for direct interpolation, a neat idea



if __name__ == "__main__":  # in the case not transferring data from php, then simply revert to a previous version, commit
	
	print 'pyThor (pyThor,server-side) (rapydscript, python client-side javascript)'
	#print_args(sys.argv, '<br>HERE front.py '+'<br>')		# to view the arguments that are sent to PyThor (from PHP)
		
	create_superglobals(sys.argv)
	
	if( not len(sys.argv) >= 2 ):
		print "argument is required, which domain name from the initial, starting PHP"
		sys.exit(1)
		
	output(name=sys.argv[1])
	
	  

