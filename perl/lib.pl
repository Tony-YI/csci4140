#!/usr/bin/perl -w

###	This .pl file is used for storing the lib sub-routine that	###
###	will be used in the assignment.                             ###

use DBI;	#use DataBase Interface
use CGI;
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;

###################################################
###            Setup MySQL database             ###
###################################################

my $db_host = $ENV{"OPENSHIFT_MYSQL_DB_HOST"};
my $db_username = $ENV{"OPENSHIFT_MYSQL_DB_USERNAME"};
my $db_password = $ENV{"OPENSHIFT_MYSQL_DB_PASSWORD"};
my $db_name = $ENV{"OPENSHIFT_APP_NAME"};	#default database name is same as the application name, csci4140assig1

my $db_handler;	#GLOBAL VARIABLE

sub db_create		#create a database
{
	my $db_source = "DBI:mysql:;host=$db_host"; #note: NO $db_name
	$db_handler = DBI->connect($db_source, $db_username, $db_password) or die $DBI::errstr;
	$db_handler->do("CREATE DATABASE $db_name");
	$db_handler->disconnect() or die $DBI::errstr;
}

sub db_drop		#drop the database
{
	my $db_source = "DBI:mysql:;host=$db_host"; #note: NO $db_name
    $db_handler = DBI->connect($db_source, $db_username, $db_password) or die $DBI::errstr;
    $db_handler->do("DROP DATABASE $db_name");
    $db_handler->disconnect() or die $DBI::errstr;
}

sub db_connect	#void sub-routine
{
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	$db_handler = DBI->connect($db_source, $db_username, $db_password) or die $DBI::errstr;
}

sub db_disconnect
{
	$db_handler->disconnect() or die $DBI::errstr;
}

sub db_execute	#usage: query($query, \@result, \$row_len)
                #parameter ($query) is the SQL query
                #parameter (\@result) is the array used to store the data get from database
                #parameter (\$row_len) records the number of attributes in one row
{
    db_connect();
	my $query_str = shift @_;

	my $query = $db_handler->prepare($query_str);
	$query->execute() or die $query->errstr;
    
    if((my $ptr_result = shift @_) && (my $ptr_row_len = shift @_))
    {
        $$ptr_row_len = $query->{NUM_OF_FIELDS};
        while (my @temp_array = $query->fetchrow_array())
        {
            foreach my $i (@temp_array)
            {
                push(@$ptr_result, $i);
            }
        }
        
    }
    db_disconnect();
}

sub db_create_table   #create all tables we need
{
    my $query = "CREATE TABLE user (user_name CHAR(20) PRIMARY KEY, pass_word CHAR(20));";
    db_execute($query);
    
    $query = "CREATE TABLE session (user_name CHAR(20), session_id CHAR(20), PRIMARY KEY(user_name, session_id));";
    db_execute($query);
    
    $query = "CREATE TABLE file (user_name CHAR(20), file_name CHAR(20), file_size INT, upload_time INT, img_description CHAR(50), img_path CHAR(50), shortcut_path CHAR(50), PRIMARY KEY(user_name, file_name));";
    db_execute($query);
}

sub db_init #insert seed data
{
    my $query = "INSERT INTO user (user_name, pass_word) VALUES ('admin', 'admin');";
    db_execute($query);
    
    my $query = "INSERT INTO user (user_name, pass_word) VALUES ('wyyi', 'haha');";
    db_execute($query);
}

###################################################
###          Setup Permanent Storage            ###
###################################################

my $data_dir = $ENV{"OPENSHIFT_DATA_DIR"};
my $img_dir = "_img";  #GLOBAL VARIABLE
my $shortcut_dir = "_shortcut";    #GLOBAL VARIABLE

sub clean_storage
{
    my $wanted_dir_name = `cd "$data_dir" && ls`;   #do not use `ls -A` since we don't want to delete directory start with .*
    my @wanted_dir_name_array = split(/\n/, $wanted_dir_name);
    #print "@wanted_dir_name_array";
    
    foreach my $i (@wanted_dir_name_array)
    {
        #delete directory
        `cd "$data_dir" && rm -r "$i"`;
    }
    
    #my $out = `cd "$data_dir" && ls -a`;    #remember the "" inside ``
    #print "<h4>$out</h4></br>";
}

#sub init_storage    #used in "sub create_dir"
#{
#    my $user_name = shift @_;
    #my $query = "SELECT $user_name FROM user where 1;";  #select all the username
    #my @result  = ();
    #my $row_len;
    #db_execute($query, \@result, \$row_len);
    #print "@result";
    #print "$row_len";
    
    #foreach my $i (@result)
    #{
    #    `cd "$data_dir" && mkdir "$i$img_dir" && mkdir "$i$shortcut_dir"`;
    #}
    
#    `cd "$data_dir" && mkdir "$user_name$img_dir" && mkdir "$user_name$shortcut_dir"`;

#    my $out3 = `cd "$data_dir" && ls -a`;
#    print "<h4>$out3</h4></br>";
#}

###################################################
###           Setup LogIn Interface             ###
###################################################


###################################################
###           Setup Upload Interface            ###
###################################################

my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};    #equals to $data_dir


sub upload_pic  #if the ./user_name_img and ./user_name_shortcut do not exist, create it
                #usage: upload_pic($user_name, $file_name, $description)
                #run this every time when upload
{
    my $user_name = shift @_;
    my $file_name = shift @_;
    my $description = shift @_;
    
    if(!(-d "$upload_dir$user_name$img_dir")) #dir not found
    {
        #print "create dir and upload pic<br/>";
        #create dir
        `cd "$upload_dir" && mkdir "$user_name$img_dir"`;
        
        #upload pictur
    }
    else
    {
        #print "upload pic<br/>";
        #upload picture
        
    }
    
    if(!(-d "$upload_dir$user_name$shortcut_dir"))    #dir not found
    {
        #print "create dir and upload pic<br/>";
        #create dir
        `cd "$upload_dir" && mkdir "$user_name$shortcut_dir"`;
        
        #upload picture
    }
    else
    {
        #print "upload pic<br/>";
        #upload picture
        
    }
    
    #my $out3 = `cd "$data_dir" && ls -a`;
    #print "<h4>$out3</h4></br>";
}

return 1;	#for header file, it must return 1, otherwise perl will exit with default value 0
