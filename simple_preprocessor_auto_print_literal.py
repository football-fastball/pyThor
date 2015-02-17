# this is after the initial simple_preprocessor.py
# 
# therefore, front_compiled.py (or whatever its name is given
# by php ( or perhaps for include files also by python)
# flimsy at this time
import sys

def print_array(s):
	print 'Array items: '
	for x, item in enumerate(s):
		print str(x)+':('+item+')'
	print '<br>'

def is_found(s):	
	return False if s == -1 else True
   #return WHEN_TRUE_THIS  if EVALUATES_TO_TRUE  else  WHEN_FALSE_THIS

def repeat(s,times):
	return s * times if times > 0 else ''
	
def process(lines):
	#   example, (spaces ok)
	#   print_wwwlog('   is replaced with   print_wwwlog(r'
	#   print_wwwlog("   is replaced with   print_wwwlog(r"
	
	out = ''
	for line in lines:
		#s = line.split()      # or line.lstrip()  same thing    then  s[0]
		func = 'print_wwwlog'
		
		# the idea is     if ( '<%' in line and '%>' in line  )   # due to it already being converted to triple double quoted a raw string literal string
		# but because pre_processor.py runs first, therefore its the following:
		if ( '( pyQuickTags(r"""' in line and '""")' in line ):		# therefore, presuming that quick tags are being used
			out += line                             # therefore, not automatically adding r, already done
			continue
		
		if ( line.lstrip().startswith(func) ):  	#  .startswith(func)     same as      [:len(func)] == func    works 
			s   = line.find("'")
			d   = line.find('"')
			
			print '<br>LINE: (' + line + ')'		# print_array(s)
			
			val = -1
			if ( is_found(s) and is_found(d) ): 	# situation of both (all) exist in string
			
				if s < d:
					val = s
					print 'point #1 - IS FOUND (single quote) '
				else:
					val = d
					print 'point #2 - IS FOUND (double quote) '
			elif ( is_found(s) or is_found(d)  ): 	# one or other exist in string (not both)
			
				if is_found(s):
					val = s
					print 'point #3 - IS FOUND (single quote) '
				else:
					val = d
					print 'point #4 - IS FOUND (double quote) '
			else: # therefore neither exist in string i.e.,  not is_found(s) and not is_found(d)
					# exit somehow
					out += line   #  its an early go to next item in the loop,  can r literal strings within quotes  not variables or returned strings from function returns
					print '<br><br> Nothing found <br><br>'
					continue
			
			print 'VAL IS: ('+ str(val) + ')'
			print 'VAL VALUE IS: ('+ line[val] + ')'
			
			if ( is_found(val) ):					# determine if triple quoted string or not
				if line[val:val+3] == '"""':
					print '<br>its a triple double quote<br>'
					print 'TDQ=(' + line[val:val+3] +')'
					
				elif line[val:val+3] == "'''":
					print '<br>its a triple single quote<br>'
					print 'TSQ=(' + line[val:val+3] +')'
				else:
					print 'SITUATION IS: (' + line[val:val+3] + ')'
					
			paren = line.find("(")					# openparenthesis
			count = len(line[paren+1:val])
			print '<br>SPACE BETWEEN IS : COUNT : ' + str(count) + '<br>'
			
			result = line[:paren+1] + repeat(' ',count-1) + 'r' + line[val:]  # this is the line added with r
			print '<br>FINAL STRING IS  : ' + result + '<br>'
			
			
			out += result
		else:
			out += line
	
	return out
	# initially for every print_wwwlog(  then read its argument
	
# until exact, just going to use a 3rd file to review
def modify_it(file):   # received _compiled.py

	#with open(file, 'r+') as fp:
	#	lines = rp.readlines()
	#	data = process(  lines  )
	#	fp.seek(0)
	#	fp.write(   data   )
	#	fp.truncate()

	
	with open(file, 'r') as rp:
		lines = rp.readlines()  # includes newlines, otherwise  .read().splitlines()  removes newlines
		data = process(lines)
		
	with open(file , 'w') as wp:
		data = wp.write(  data  )
		

if __name__ == "__main__":

	if( not len(sys.argv) >= 3 ):
		print "argument is required"
		sys.exit(1)                  # import sys
		
	# sys.argv[1]      #argument received
	print '<br>'
	print 'SIMPLE_PREPROCESSOR_AUTO_PRINT_LITERAL file(' + sys.argv[1] + ')';
	print 'SIMPLE_PREPROCESSOR_AUTO_PRINT_LITERAL use, convert to auto literals, i.e., r the strings (' + sys.argv[2] + ')';
	# perhaps argument when you know not to forget the raw string escape keyword  r'  '
	if (sys.argv[2] == 'False'):
		print 'EXITING SIMPLE_PREPROCESSOR_AUTO_PRINT_LITERAL.'
	
	else:
		print '<br>'
		modify_it(sys.argv[1])