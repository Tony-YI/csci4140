#!/usr/bin/perl -w

### This .cgi file is for login             ###

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require "./lib.pl";

my $CGI_o = CGI->new();
my $user_name = $CGI_o->param('user_name');
my $pass_word = $CGI_o->param('pass_word');
my $login = $CGI_o->param('login');

sub print_form
{
    print <<__html_file__;
        <form method="POST" action="login.cgi">
        User Name:
        <input type="text" maxlength="30" name="user_name"/><br/><br/>
        PassWord:&nbsp;&nbsp;
        <input type="password" maxlength="50" name="pass_word"/><br/><br/>
        <input type="submit" name="login" value="LogIn"/>
    </form>
    <br/>
    <a href="album_display.cgi">View Album (Read Only)</a>
__html_file__
}

sub print_html_head
{
    print <<__html_file__;
<html>
    <body>
        <title>LogIn Interface</title>
__html_file__
}

sub print_html_tail
{
    print <<__html_file__;
    </body>
</html>
    __html_file__
}

if($login eq "LogIn")   #subbmit buttom is pressed
{
    print $CGI_o->header();
    
    if(!($user_name) || !($pass_word))  #user_name of pass_word is empty
    {
        print_html_head();
        print "Log In Failed. User Name and PassWord can't be EMPTY.<br/><br/>"
        print_form();
        print_html_tail();
    }
}


#print <<__html_file__;
#<html>
#    <body>
#        <title>LogIn Interface</title>
#        <p>LogIn Interface</p>
#    </body>
#</html>
#__html_file__
#when a .cgi file is end with ___html_file__, a new line should be added. Otherwise, error.