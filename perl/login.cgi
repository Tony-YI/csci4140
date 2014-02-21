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

my $expire_time = "+2h";
my $cookie1;
my $cookie2;

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
    if(!($user_name) || !($pass_word))  #user_name of pass_word is empty
    {
        print $CGI_o->header();
        print_html_head();
        print "Log In Failed. User Name and PassWord can't be EMPTY.<br/><br/>";
        print_form();
        print_html_tail();
    }
    
    else    #input are valid
    {
        my $query = "SELECT * FROM user WHERE user_name='$user_name';";
        my @result = ();
        my $row_len = "";
        db_execute($query, \@result, \$row_len);
        if($result[0] eq $user_name && $result[1] eq $pass_word)
        {
            #valid user
            ###TODO:generate session id and store it in database
            cookie_gen($CGI_o, $user_name, $expire_time, \$cookie1, \$cookie2);
            print $CGI_o->redirect(-cookie=>[$cookie1, $cookie2], -url=>'./display_panel.html');
        }
        else
        {
            print $CGI_o->header();
            print_html_head();
            print "Log In Failed. Please check your User Name and PassWord.<br/><br/>";
            print_form();
            print_html_tail();
        }
    }
}

else
{
    print $CGI_o->header();
    print_html_head();
    print_form();
    print_html_tail();
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