#!/usr/bin/perl -w

use strict;
use CGI;	#load the CGI module
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $CGI_o = CGI->new;

print <<__html_file__;
<html>
   <body>
       <title>LogIn Interface</title>
       <p>LogIn Interface</p>
   </body>
</html>
__html_file__
#when a .cgi file is end with ___html_file__, a new line should be added. Otherwise, error.

#redirect
#print $CGI_o->redirect('./login.cgi');