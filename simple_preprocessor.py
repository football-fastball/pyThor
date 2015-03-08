import sys
import re
import os

option_auto_trailing_backslash_doubleit = True  # when True,  resolves by converting trailing \ to \\     (alternative method is setting to False)
                                                # when False, resolves by adding a space to end of python quick tag string to auto resolve python not allowing trailing backslash in triple quoted string
                                                # either is ok, works
def print_args(s):
	for item in s:
		print 'ARG:(' + item + ')'
		
def print_tuple(u):
	for item in u:	
		#print item                              # this will print  the raw string literal version of it (newlines shown as \n literally text displayed in command line text)
		print str( item[0] ) + ' ' + item[1] + '<br>'    # this      prints the escaped version of it (e.g., newlines wrap)

def print_tuple_4i(u):
	for item in u:	
		#print item                              # this will print  the raw string literal version of it (newlines shown as \n literally text displayed in command line text)
		print str( item[0] ) + ' ' + item[1] + ' ' + item[2] + ' ' + str( item[3] )
	
	
def makes_tuple_find(s, item, previous_text_character_length=0):
	idx=0
	t=[]
	while(1):
		i = s.find(item,idx)
		
		if (i== -1):
			break
		
		if (i == 0): # in the case of /%>    i then is 0
			t.append( ( i, 'FALSE_START' + s[0:i+len(item)] ) )
		else:
			t.append( ( i , s[i-previous_text_character_length:i+len(item)] ) )
		idx = i+1
	return t

def reverse_tuple_list(t):
	v=[]
	l = len(t)
	idx = l
	for x in range(l):
		v.append( ( t[idx-1][0] , t[idx-1][1] ) )
		idx = idx - 1
	return v

def make_quad_tuple_find_between_tags_reverse_order(s, opentag = '<%', closetag = '%>'):
	
	arr = makes_tuple_find(s, opentag)
	
	arr2 = reverse_tuple_list(arr)

	tup = []
	for item in arr2:
		
		tmp = item[1]
		idx = item[0]
		res = s.find(closetag, idx) # can do idx+2 to be exact

		if res == -1:
			print 'early exit, cannot find closing python quick tag'
			sys.exit(1)
			
		tup.append( ( item[0], item[1], '%>', res ) )
	return tup		

def auto_backslash_escape_adjacent_to_python_quicktag(s, array_of_tuples_in_reverse_order , thing): # adjacent to the closing python quicktag   %>
	t = s+' '  # just an exercise to not modify the original,  otherwise  s works too
	t = t[:-1] # to create a new string , otherwise perhaps     t = s[:]  e.g., http://www.python-course.eu/deep_copy.php
	for i in array_of_tuples_in_reverse_order:

		if i[1] == thing: #ok, that the required result
			print 'yes'                                     # then an edit to the source code will only occur when a count > 0
		else:
			t = t[: i[0]+1  ] + '\\' + t[  i[0]+1  :]
	
	return t

def findindices_of_nonwhitespace(s): # string  , returns tuple  (index and item) , this function not used for now
                                     # split function  enhanced to also return the indices of each item 
	arr = s.split()
	t=[]
	for item in arr:
		i=0
		i = s.find(item, i)
		t.append((i,item))
	return t		

def adjacent(itemA, itemB, new, s): # skips whitespace  # regrettably had to resort to this regex, required, therefore this function
	
	# something like this should be possible (using itemA and itemB)
	restr = itemA + r'\s{0,}' + itemB  # not using this string because,
	# due to the operation of regex and its variability it's due to escaping of characters and other reasons
	
	# therefore:
	return re.sub(r'\(\s{0,}<%', new, s)  # 0 to many spaces in between the ( and <%     #note: i had to escape the open parenthesis in this regex search


def concat2( itemA, itemB, new, s):
	
	return re.sub( itemB + r'\s{0,}\+\s{0,}<%', new, s )

	
def algorithm(s, uni_val=str(True) ):
	
	global option_auto_trailing_backslash_doubleit # when set to False adds space to resolve trailing backslash issue
	
	uni_str = '.unicode_markup('+uni_val+')'
	
	
	s = s.replace('return <%', 'return pyQuickTags(r"""')
	s = s.replace('= <%', '= pyQuickTags(r"""')
	
	# note adjacent function for any number of spaces between ( and <%
	s = adjacent('(', '<%', '( pyQuickTags(r"""', s)
	
	s = concat2( '+', '%>', '%> + pyQuickTags(r"""', s)
	
	s = concat2( '+', "\)",  ') + pyQuickTags(r"""', s)
	
	s = concat2( '+', "\'", '\' + pyQuickTags(r"""', s)  # when text in form  ' + %> or " + %> required
	s = concat2( '+', '\"', '\" + pyQuickTags(r"""', s)  # can comment these two lines out then
	
	s = s.replace('<%', 'print pyQuickTags(r"""')
#		s = s.replace('%%>', ')'+uni_str )    # UNCOMMENT POINT *C* (uncomment the FIRST comment hash tag for the remove unicode operation)      # to remove quick workaround, remove this line
	
	if(option_auto_trailing_backslash_doubleit): # an alternative to the algorithm2 solution that (resolves it by adding a trailing backslash) is 
		s = s.replace('%>','""").initsupers(locals(),globals())')              # to simply add a space to the end of the string at this exact point of the code (that modifies the compiled code only) that somewhat resolves the trailing backslash issue in python triple double quotes 2015.02.08
	else:
		s = s.replace('%>',' """).initsupers(locals(),globals())')     # adds a space 

#		s = s.replace('""")).format (     %:)>', '""").format (   #  %:)> ')    # UNCOMMENT POINT *D* (uncomment the FIRST comment hash tag for the remove unicode operation)     
	# about the previous line,  to remove quick workaround, remove this line, way to rid one close parenthesis, with the happy face keyword created for this purpose , it comments out the keyword %:)> 

	# statements marked by UNCOMMENT POINT *C* and *D* uncomment to remove unicode type quick python tags
	# uncomment to remove unicode type quick python tags i.e., <unicode> </unicode>  though the contents in between the tags remain intact
	return s

def algorithm2(s):
										 # added: 2015.02.08 (feature to auto escape backslash for trailing raw literal triple double quotes to make it a valid python string)
	item1 = r'\\%>'                      # must be raw string literal
	arr1  = makes_tuple_find(s, item1 )
	item2 = '\%>'
	arr2  = makes_tuple_find(s, item2, 1)
	arr3  = reverse_tuple_list(arr2)     # to add a slash, from end to front so indices consistent
	s     = auto_backslash_escape_adjacent_to_python_quicktag(s, arr3, item1)
	return s 

def algorithm_to_allow_tdq_within_quick_tags(s, old='"""', new='&quot;&quot;&quot;'): # to allow triple double quotes within quick tags <% %>

	tup = make_quad_tuple_find_between_tags_reverse_order(s)

	for i in tup:
	
		s = s[:i[0]] + s[i[0]:i[3]].replace(old, new) + s[i[3]:]
		
		#s = s[:i[0]] + s[i[0]:i[3]].replace('"""', '&quot;&quot;&quot;') + s[i[3]:]

	return s

# the algorithm created by Stan "Lee" Switaj
def algorithm_to_allow_tdq_within_quick_tags_final_done(s, opentag, closetag, old, new ): # instead of regex, perhaps not going to be used

	tup = make_quad_tuple_find_between_tags_reverse_order(s, opentag, closetag)

	for i in tup:
		s = s[:i[0]] + s[i[0]:i[3]].replace(old, new) + s[i[3]:]
		
	return s

	
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
	
	return s[start+len(start_tag):end]	#  +1 perhaps
	
def modify_diff(type_val, source, destination, uni_val=''):

	global option_auto_trailing_backslash_doubleit
	
	# assemble point the source file (within same file)
	
	# tag to tag read of main features, then read of source, then read of tag to tag of main,argument part
	
	# test if feature file exists
	features_file = 'simple_preprocessor_pyThor_features_txt.py'
	
	opentag   = '#_PYTHON_QUICK_TAGS_FEATURES_OPEN_TAG_#'
	closetag  = '#_PYTHON_QUICK_TAGS_FEATURES_CLOSE_TAG_#'
	features  = get_string_tag_to_tag_read_source( features_file, opentag, closetag )
	
	
	opentag   = '#_MAIN_PROGRAM_OPEN_TAG_#'
	closetag  = '#_MAIN_PROGRAM_CLOSE_TAG_#'
	mainintro = get_string_tag_to_tag_read_source( features_file, opentag, closetag )
	

	with open(source, 'r') as rp:
		s = rp.read()
	
	if (type_val == '-M'):	#otherwise its -I
		s = features + s + mainintro

	#print 'Length:' + str(len(s)) + '<br>'
	#print s	
	#print 'early exit'
	#sys.exit(1)

	if (option_auto_trailing_backslash_doubleit): # by converting trailing \ to \\   Otherwise alternative method to add space, i.e., set this variable to False at the top
		s = algorithm2(s)
	
	
	s = algorithm_to_allow_tdq_within_quick_tags(s) # python quick tags are already the initial tags
		
	#s = algorithm_to_allow_tdq_within_quick_tags_final_done(s, '<%', '%>', '"""', '&quot;&quot;&quot;') # instead of regex

	with open(destination, 'w') as wp:
			wp.write( algorithm(s, uni_val) )


def exists(path):	# file_exists
	if (os.path.isfile(path)):
		return path
	else:
		print 'file does not exist, early exit' + path + '<br>'
		sys.exit(1)

def type_check(type):
	if ( type == '-I' or type == '-M' ):
		return type
	else:
		print 'first argument required is -M or -I ,early exit'+'<br>'
		sys.exit(1)

if __name__ == "__main__":  # in the case not transferring data from php, then simply revert to a previous version, commit
	# simply remove or comment out the print statements at your convenience, used just for debugging and testing purposes
	if( not len(sys.argv) >= 2 ):
		print "argument is required, which domain name from the initial, starting PHP"
		sys.exit(1)
	
	print (' Preprocessor ')
	print_args(sys.argv)
	
	type   =''
	unicode=''
	count  = len(sys.argv)

	if( count == 3):
		src  = exists(sys.argv[1])
		dst  = sys.argv[2]
	if( count == 4):
		type = type_check(sys.argv[1])
		src  = exists(sys.argv[2])
		dst  = sys.argv[3]
	if( count  == 5):
		type    = type_check(sys.argv[1])
		src     = exists(sys.argv[2])
		dst     = sys.argv[3]
		unicode = sys.argv[4]
		
	modify_diff( type_val=type, source=src, destination=dst, uni_val=unicode )