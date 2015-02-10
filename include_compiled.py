
def this_is_a_test():

	return utags(training_wheels_bit_slower_to_remove(r"""

This is intended to be included as text, and returned as a string
\\a\\1\\2\\3\\4\\5\\6\\7\\8\\9\\b\\f\\v\\r\\n\\t\\0\\x0B   testing3, expected
<!-- escape characters within include files -->

"""))

def python_using_php_htmlentities(s):

	salt = uuid.uuid4().hex
	
	s = s + r'\a\1\2\3\4\5\6\7\8\9\b\f\v\r\n\t\0\x0B'
	
	s = s.replace('&quot;&quot;&quot;', '*QUOT-*-QUOT-*-QUOT*'+salt);
	
	code_init = utags(training_wheels_bit_slower_to_remove(r""" echo htmlentities('%s'); """))  %  s.replace("'", "\\'")  # quotes cause problem to format string variables, give it a raw string literal
															
	width = 200
	height = 200
	
	code_here = utags(training_wheels_bit_slower_to_remove(r"""
	echo ('   {**{php_width}**}, {**{php_height}**}  ');
	""")).format( php_width = str(width) , php_height = str(height) )

	var = php(code_init)
	
	
	var = var.replace('*QUOT-*-QUOT-*-QUOT*'+salt, '&quot;&quot;&quot;')
	return var

	
def source_code():

	#simple_preprocessor.py to address """ """ between quick tags and other small things of a raw string literal
	
	return utags(training_wheels_bit_slower_to_remove(r"""

	'how about this nice person you'
 
&quot;&quot;&quot; hello world, within triple double quotes within python quick tags &quot;&quot;&quot;

	<br>
	hello world, this is the source code included file
	<unicode></unicode>
	
	<p> </p>

"""))


def source_code_output():
	return utags(training_wheels_bit_slower_to_remove(r"""
	

{**{source_code_htmlentities_form}**}
	

""")).format( source_code_htmlentities_form = python_using_php_htmlentities( source_code() ) )
	
def console_log_function():
	return utags(training_wheels_bit_slower_to_remove(r"""
	
     /**
     * Logs messages/variables/data to browser console from within php
     *
     * @param $name: message to be shown for optional data/vars
     * @param $data: variable (scalar/mixed) arrays/objects, etc to be logged
     * @param $jsEval: whether to apply JS eval() to arrays/objects
     *
     * @return none
     * @author Sarfraz
     */
     function logConsole($name, $data = NULL, $jsEval = FALSE)
     {
          if (! $name) return false;
 
          $isevaled = false;
          $type = ($data || gettype($data)) ? 'Type: ' . gettype($data) : '';
 
          if ($jsEval && (is_array($data) || is_object($data)))
          {
               $data = 'eval(' . preg_replace( '#[\\a\\1\\2\\3\\4\\5\\6\\7\\8\\9\\b\\f\\v\\r\\n\\t\\0\\x0B]+#', '', json_encode($data)) . ')';
               $isevaled = true;
          }
          else
          {
               $data = json_encode($data);
          }
 
          # sanitalize
		  $data = $data ? $data : '';
          $search_array = array("#\\'#", '#\\"\\"#', "#\\'\\'#", "#\\n#", "#\\r\\n#");
          $replace_array = array('"', '', '', '\\\\n', '\\\\n');
          $data = preg_replace($search_array,  $replace_array, $data);
          $data = ltrim(rtrim($data, '"'), '"');
          $data = $isevaled ? $data : ($data[0] === "'") ? $data : "'" . $data . "'";
 
$js = <<<JSCODE
\n<script>
     // fallback - to deal with IE (or browsers that don't have console)
     if (! window.console) console = {};
     console.log = console.log || function(name, data){};
     // end of fallback
 
	// I innovated a start and end tag for hexadecimal content (the tag is of course arbitrary, though seems to fit the purpose (apropos))
    
	function not(s){return !s;}
	
	function hex2asc(pStr) {
	
		if (not( typeof pStr === 'string') )			// alert(typeof pStr);
		return pStr;

		// todo: to check for minimum lengths at this point 

		var startHexTag = pStr.substr(0, 5);			// start tag to indicate hexadecimal content is <hex>

		var endHexTag = pStr.substr(pStr.length - 6); 	// end tag to indicate hexadecimal content is </hex>

		if ( not ( startHexTag === "<hex>" && endHexTag === "</hex>" ) )
		return pStr;

		var data = pStr.substring(5, pStr.length - 6 )

        tempstr = '';
        for (b = 0; b < data.length; b = b + 2) {
            tempstr = tempstr + String.fromCharCode(parseInt(data.substr(b, 2), 16));
        }
        return tempstr;
    }
 
     console.log('$name');
     console.log('------------------------------------------');
     console.log('$type');
     console.log(hex2asc($data));
     console.log('\\\\n');
</script>
JSCODE;
 
          echo $js;
     } # end logConsole
	 
	 
//echo( ' <br> {**{hello}**} <br>');	 

//echo( '{**{howdy}**}');

""")).format (  hello='hello world', howdy='very well thanks' )