#!/usr/bin/perl -w

use strict;
use CGI;	#load the CGI module
#use CGI::Carp qw(warningsToBroswer fatalsToBrowser);

my $CGI_o = CGI->new;

my $user_name = $CGI_o->cookie("user");
my $session_id = $CGI->cookie("session");

print $CGI_o->header();
print <<__html_file__ #here document
<html>
    <body>
        <a href="reinit.html">Re-Initialization</a></br>
        <h2>$user_name</h2></br>
        <h2>$session_id</h2>
    </body>
</html>
__html_file__
