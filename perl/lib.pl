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

sub db_execute	#usage: db_execute($query, \@result, \$row_len) or db_execute($query)
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
    my $query = "CREATE TABLE user (user_name CHAR(30) PRIMARY KEY, pass_word CHAR(50));";
    db_execute($query);
    
    $query = "CREATE TABLE session (user_name CHAR(30), session_id CHAR(255), PRIMARY KEY(user_name, session_id));";
    db_execute($query);
    
    $query = "CREATE TABLE file (user_name CHAR(30), file_name CHAR(255), file_size INT, upload_time INT, img_description CHAR(50), img_path CHAR(255), shortcut_path CHAR(255), PRIMARY KEY(user_name, file_name));";
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
                #usage: upload_pic(\$CGI_o, $user_name, $file_name, $description, \$flag)
                #run this every time when upload
                #$flag = 1 if sucessful, 2 if file exited, 3 if file too large, 4 if can't open dir, 5 if invalid extension
{
    my $CGI_o_ptr = shift @_;
    my $user_name = shift @_;
    my $file_name = shift @_;
    my $description = shift @_;
    my $flag_ptr = shift @_;
    
    if(!(-d "$upload_dir$user_name$img_dir")) #dir not found
    {
        #create dir
        `cd "$upload_dir" && mkdir "$user_name$img_dir"`;
    }
    if(!(-d "$upload_dir$user_name$shortcut_dir"))
    {
        #create dir
        `cd "$upload_dir"&& mkdir "$user_name$shortcut_dir"`;
    }
    
    ###TODO:check file size in an easy way...no can do
    
    #check file existence
    my @result = ();
    my $row_len = "";
    my $query = "SELECT user_name, file_name FROM file WHERE user_name='$user_name' AND file_name='$file_name';";
    db_execute($query, \@result, \$row_len);
    if(@result) #exist
    {
        ###TODO: Duplication handle interface
        $$flag_ptr = 2;
        return;
    }
    
    #file not exist, upload picture
    if(!open(OUTFILE, ">", "$upload_dir$user_name$img_dir/$file_name"))    #can't open file for writing
    {
        $$flag_ptr = 4;
        return;
    }
    
    #open file sucessfully, file size is allowed and upload file
    my $ret = 0;
    my $totalBytes = 0;
    my $buffer = "";
    
    binmode(OUTFILE);    #???
    
    while($ret = read($$CGI_o_ptr->upload("photo"), $buffer, 1024))
    {
        print OUTFILE $buffer;
        $totalBytes += $ret;
        if($totalBytes > 1024*1024) #1 MB, check file size
        {
            close(OUTFILE);
            `rm "$upload_dir$user_name$img_dir/$file_name"`;
            $$flag_ptr = 3;
            return;
        }
    }
    
    close(OUTFILE); #file uploaded
    
    #indentify the file
    my $identity = `identify -verbose "$upload_dir$user_name$img_dir/$file_name" | grep Format:`;
    my @temp_array = split(/\n/, $identity);
    
    $_ = $identity;
    if(!/JPEG/ && !/GIF/ && !/PNG/)
    {
        #not match
        `rm "$upload_dir$user_name$img_dir/$file_name"`;
        $$flag_ptr = 5;
        return;
    }
    
    #generate a shortcut, convert only when larger than 100x100
    `convert "$upload_dir$user_name$img_dir/$file_name" -resize 100x100\> "$upload_dir$user_name$shortcut_dir/$file_name"`;
    
    #convert description into viewable
    $_ = $description;
    $description =~ s/&/&amp;/g;
    $description =~ s/</&lt;/g;
    $description =~ s/>/&gt;/g;
    $description =~ s/\"/&quot;/g;
    $description =~ s/\'/&#39;/g;
    
    #upload description and other attributes to the database
    ###TODO: add time stamp
    my $img_path = "$upload_dir$user_name$img_dir/$file_name";
    my $shortcut_path = "$upload_dir$user_name$shortcut_dir/$file_name";
    $query = "INSERT INTO file (user_name, file_name, file_size, upload_time, img_description, img_path, shortcut_path) VALUES ('$user_name', '$file_name', '$totalBytes', 0, '$description', '$img_path', '$shortcut_path');";  #remember the ' ' of SQL
    db_execute($query);
    
    $$flag_ptr = 1;
}

return 1;	#for header file, it must return 1, otherwise perl will exit with default value 0
