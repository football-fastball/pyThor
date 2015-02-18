<?php
    /*    pyThor   */

									// Note: when False, the file front_compiled.py is created
$auto_print_wwwlog_literal = True;

$str_bool_uni_value = 'False';

// Now, auto compiling a RapydScript to JavaScript if needed before running the web page

// Note:
// The compiling can just as easily be done in the python code,
// but the php code just as accommodating to the 
// maintenance tasks, e.g., compiling rapydscript to js


// Just revert to previous version, commit 
// if not using a same domain name with different domain suffixes, e.g., domain.com, domain.net
// Though the idea if needed is to eventually transfer data to the python code, if only a few arguments
// simply through a list of parameter/arguments, with more, then to use json via a php array encode and send that

//echo domain_name_endswith() . '<br>'; // goes to py code

function domain_name_endswith() {	  // or contains, domain_suffix, etc.    // or just argument to py code

$ret1 = 'A';    // plan
$ret2 = 'WIDE'; // B
	if(isset($_SERVER['SERVER_NAME']) ) {
		$s = $_SERVER['SERVER_NAME'];
	//  :D  Lee
		$s = right(raise($s), 2);
		if ($s == 'US')
			return $ret1;  // or boolean type
		else
			return $ret2;  // world, earth, whatever, the language thing issue...
	}
return $ret1;
}


$source   = 'first.pyj';
//$compiled = 'first.js';	// optional, not used in this version

if ( not( file_exists ($source) ) ) {
	echo "$source does not exist, exiting."; 
	exit (1); 
}

compile( 'first' ); // or first.pyj

/* Note: New Feature   --   Open and Close Tags for ONLY the  .py  file  ( not the RapydScript code file )
  
   In this version I add the php feature to python of  open and close  tags that define 
   the beginning of python code and when the end of the python code occurs that are the tags   <%   and   %>
   very similar to the way   <?php   and   ?>   work in PHP.

   ( The difference being the tags technically represent an echo (print) and a triple commented string,
    (so the html output goes between the tags , not python keyword operations at this time) )

   In PHP, html code written (without the echo function) goes outside of its open and close tags.
   With this feature, it's different.
   
   This happens in the simple preprocessor step, it also gives an optional switch to enable a bit simpler python coding,
   and then the statement after the double ampersand.
   After running the actual Python web page, front.py, the statement after the next double ampersands changes the 
   text replacement back in the simple postprocessor step to the Python open and close tags,    <%   and   %>  
*/
// note: the double ampersand executes only if the first command is successful (the preprocessor step)
// NOTE: changed from system to passthru due to PHP5.6.4 strangely running python simple_postprocessor.py statement twice 2015.01.13
// perhaps its the console @echo on,off situation when system is used (inconsequentially uncertain, i.e., not relevant at this point)

// Update: Added a feature to compile the source code only when a edit occurs, therefore the compiled file runs to display the webpage
//         this is done by adding a one file format check, compiling only when the source code is modified, otherwise it simply outputs 
//         the compiled file (slight update to simple_preprocessor.py also)
//         With this feature there is an added benefit that there is no need for a post_processor.py due 
//         to being different files and the source is not modified         this feature added: 2015.01.26 and the entire project up to this day by Stan "Lee" Switaj and my email is: BehemothIncCEO@gmail.com
//         ( Sidenote: Though if this code were adapted to create a   mod_quick_tags_python  Apache module, perhaps the simple_postprocessor.py would still be required)          (comments,suggestions welcome)

	
$source = 'front.py';
$compiled = 'front_compiled.py';

if ( not( is_compiled($source, $compiled) ) ) {
	echo '(PYTHON COMPILING)';
	echo passthru(	'python simple_preprocessor.py -TW "'.$source.'" "'.$compiled.'" "'.$str_bool_uni_value.'" 2>&1  && '.
			'python "'.$compiled .'" "' .domain_name_endswith().'"  2>&1 ');
}
else {
	//echo '(ALREADY COMPILED)';
	echo passthru('python "'.$compiled. '" "' .domain_name_endswith().'"  2>&1 ');
}


function mod_dt($file) {
	return date ("YmdHis", filemtime($file));
}

function is_compiled($source, $compiled) {
	
	if ( not( file_exists ($source) ) ) {
		echo "$source file does not exist, exiting";
		return false;
	}
	
	if ( not( file_exists ($compiled) ) ) {
		echo "$compiled file does not exist" . '<br>';
		return false;
	}
	
	if ( mod_dt($source) >= mod_dt($compiled) )
		return false;
	else
		return true;
}


function compile($source, $compiled = 'default_same_name_as_source') {

	if ( not( contains('.pyj' , lower($source) ) ) )
		$source = $source . '.pyj';

	if ( $compiled == 'default_same_name_as_source' )
		$compiled = without_file_extension($source) . '.js';
	else if ( not( contains('.js' , lower($compiled) ) ) )
		$compiled = $compiled . '.js';
	
	if ( is_compiled ($source, $compiled) ) {
		//echo 'compiled, yes, already done.';
		return;
	}
	
	if ( file_exists($compiled) )
		unlink ( $compiled );

	$cc  = '"C:\Program Files\nodejs\node.exe" ';                                  // note trailing space
	$cc .= '"C:\Program Files\nodejs\node_modules\rapydscript\bin\rapydscript" ';  // note trailing space
	$cc .= "$source -o $compiled";
	system($cc);                                                                   // compiling here

	if ( not( file_exists($compiled) ) ) {
		echo "$source has a syntax error due to a failure to compile, exiting";
		exit(1);
	}

	echo 'just auto compiled python rapydscript to javascript';
}

function str_bool($s){ return ( ($s) ? 'True' : 'False'); };
function not($s){return !$s;}
function contains ($needle, $haystack) { return strpos($haystack, $needle) !== false; }
function lower($s) { return strtolower ($s); }
function raise($s) { return strtoupper ($s); }
function without_file_extension($s) { return substr($s, 0, strrpos($s, ".")); } // without . and file extension
function left($str, $length)  {return substr($str, 0, $length);}
function right($str, $length) {return substr($str, -$length);  }
#function str($s){	   // should just return 'true' or 'false' and name it str_bool() but perhaps str() can be extended
#	if (is_bool($s) == true) return ( ($s) ? 'true' : 'false'); else return 'Different type'; }

?>