#!/usr/bin/perl -w

use strict;
use CGI;	#load the CGI module
use CGI::Carp qw(warningsToBroswer fatalsToBrowser);   #the extention is .pl, can't use this

my $CGI_o = CGI->new;

if(cookie_check($CGI_o) eq 0) #cookie is invalid
{
    #redirect
    print $CGI_o->redirect('./login.cgi');
}
else
{
    print $CGI_o->redirect('./display_panel.html');
}
