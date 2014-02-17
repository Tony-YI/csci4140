#!/usr/bin/perl -w

###	This .cgi file is aim to re-initialize the system.	###
###	1.When Button "YES" of reinit.html is clicked, the	###
###	system will be re-initialized.                      ###
###	2.When Button "NO" of reinit.html is clicked, the	###
###	browser will be back to the "Login Interface".		###

###	Re-initialization steps:                            ###
###	1.Drop all the tables of the database(if it exists).###
###	2.Create a seed value of the database(admin).		###
###	3.If a database of the photo album system does not 	###
###	  exist, create it.                                 ###
###	4.Create all the required tables.                   ###
###	5.Clean the permanent file storage on OpenShift.	###
###	6.After re-initialization, go back to the login		###
###	  interface.                                        ###

use CGI;	#use the CGI module
use strict;	#then every variable should have "my"
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
require "./lib.pl";

my $CGI_o = CGI->new;	#create a new CGI module, GLOBAL VARIABLE

sub reinit
{
    ###    Re-Initialize the System    ###
    ###    Print out the html file     ###
    
    print $CGI_o->header(); #print http header
    print <<__html_file__;
<html>
    <body>
        <title>Re-Initialization</title>
        <p>
__html_file__
    
    db_drop();  #drop the MYSQL database
    print "Drop database...Done<br />";
    
    db_create();    #create a database name as APP_NAME
    print "<br />Create database...Done<br />";
    
    db_create_table();  #create all tables we need
    print "<br />Create Table...Done<br />";
    
    db_init();   #initialize the tables
    print "<br />Initialize Table...Done<br />";
    
    clean_storage();
    print "<br />Clean storage...Done<br />";
        
    print <<__html_file__;
        <br />Task Finshed!<br /><br /><br />
        <a href="login.html">Bcak to Login Interface</a>
        </p>
    </body>
</html>
__html_file__
}

my $act = $CGI_o->param("action");	#retrive the value of button, YES/NO

if($act eq "YES")	#YES button is clicked
{
    reinit();
}

elsif($act eq "NO") #NO button is clicked
{
    print $CGI_o->redirect("login.html");
}
