#!/usr/bin/perl -w

###	This .cgi file is to log the user out.	###
###	The logout action should remove the     ###
###	corresponding login session information	###
###	from both the client and the system of	###
###	the corresponding browser instance.     ###

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require './lib.pl';

my $CGI_o = CGI->new();

log_out($CGI_o);

print $CGI_o->redirect('./login.cgi'); #notice: can't add ""
#in perl, after __html_file__, there must be a new line a somthing