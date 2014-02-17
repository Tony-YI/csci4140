#!/usr/bin/perl -w

use strict;
use CGI;	#load the CGI module
#use CGI::Carp qw(warningsToBroswer fatalsToBrowser);   #the extention is .pl, can't use this

my $CGI_o = CGI->new;

my $user_name = $CGI_o->cookie("user");
my $session_id = $CGI_o->cookie("session");

print $CGI_o->header();
print <<__html_file__; #here document
<html>
    <body>
        <a href="reinit.html">Re-Initialization</a></br>
        <br /><a href="login.html">LogIn</a>
        <h2>$user_name</h2></br>
        <h2>$session_id</h2>
    </body>
</html>
__html_file__
