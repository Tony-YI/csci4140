#!/usr/bin/perl -w

use strict;
use CGI;	#load the CGI module
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $CGI_o = CGI->new;

#redirect
print $CGI_o->redirect('./login.cgi');