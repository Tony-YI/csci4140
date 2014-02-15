#!/usr/bin/perl -w

use strict;
use CGI;	#load the CGI module

$CGI_o = CGI->new;

print $CGI_o->header;

print <<__CONTENT__	#here document
<html>
<body>
Hello World!
</body>
</html>
__CONTENT__
