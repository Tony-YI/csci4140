#!/usr/bin/perl -w

###	This .pl file is used for storing the lib sub-routine that	###
###	will be used in the assignment.					###

use DBI;	#use DataBase Interface
use CGI;
use CGI::Carp qw(wariningsToBrowser fatalsToBrowser);
use strick;

###################################################
###	Setup connection to MySQL databast	###
###################################################

my $db_host = $ENV{"OPENSHIFT_MYSQL_DB_HOST"};
my $db_username = $ENV{"OPENSHIFT_MYSQL_DB_USERNAME"};
my $db_password = $ENV{"OPENSHIFT_MYSQL_DB_PASSWORD"};
my $db_name = $ENV{"OPENSHIFT_APP_NAME"};	#default database name is same as the application name

sub db_connect()	#pass by reference, parameter is (/$db_handler)
{
	my $ptr = shift @_;
	
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	$$ptr = DBI->connect($db_source, $db_username, $db_password) or die $DBI::errstr;
}

sub db_disconnect()	#pass by reference, parameter is (/db_handler)
{
	my $ptr = shift @_;
	$$ptr->disconnect;
}

###################################################
###
###################################################

return 1;	#for header file, it must return 1, otherwise perl will exit with default value 0
