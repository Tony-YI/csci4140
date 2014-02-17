#!/usr/bin/perl -w

### This .cgi file is for login             ###

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
require "./lib.pl";

my $CGI_o = CGI->new;

print $CGI_o->header();

#print <<__html_file__;
#<html>
#    <body>
#        <title>LogIn Interface</title>
#        <p>LogIn Interface</p>
#    </body>
#</html>
#__html_file__
#when a .cgi file is end with ___html_file__, a new line should be added. Otherwise, error.