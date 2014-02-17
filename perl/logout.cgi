#!/usr/bin/perl -w

###	This .cgi file is to log the user out.	###
###	The logout action should remove the     ###
###	corresponding login session information	###
###	from both the client and the system of	###
###	the corresponding browser instance.     ###

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $CGI_o = CGI->new();

print $CGI_o->header(); #notice: can't add ""
print <<__html_file__;
<html>
	<body>
		<title>LogOut</title>
		<p>LogOut</p>
        <a href="login.html">LogIn</a>
	</body>
</html>
__html_file__
#in perl, after __html_file__, there must be a new line a somthing