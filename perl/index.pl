#!/usr/bin/perl -w

use strict;
use CGI;	#load the CGI module
#use CGI::Carp qw(warningsToBroswer fatalsToBrowser);

my $CGI_o = CGI->new;

print $CGI_o->header();

print <<__CONTENT__	#here document
<html>
<body>
Hello World!
<a href="reinit.html">Re-Initialization</a>
</body>
</html>
__CONTENT__
