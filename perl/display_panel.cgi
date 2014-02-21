#!/usr/bin/perl -w

### This .html file is for display panel    ###

#The display panel should contain a list of links to direct the user to
#different components of this system.

#1. The link "View Album" takes the user to "Album display interface".
#2. The link "Upload Photos" takes the user to "File picking interface".
#3. The link "Logout" logs the user out.

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
require './lib.pl';

my $CGI_o = CGI->new();

if(cookie_check($CGI_o) eq 0) #cookie is invalid
{
    #redirect
    print $CGI_o->redirect('./login.cgi');
}

print $CGI_o->header();

print <<__html_file__;
<html>
	<body>
		<title>Display Panel</title>
		<a href="album_display.cgi">View Album</a><br />
		<br /><a href="file_picking.cgi">Upload Photos</a><br />
		<br /><a href="logout.cgi">Logout</a><br />
	</body>
</html>
__html_file__
#if __html_file is the last line, must add a new line