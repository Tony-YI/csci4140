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
	$db_handler->do("CREATE DATABASE $db_name;") or die $DBI::errstr;
    $db_handler->do("SET GLOBAL time_zone = '-5:00';") or die $DBI::errstr; #openshift's time zone
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
    
    $query = "CREATE TABLE session (user_name CHAR(30), session_id CHAR(255), login_time TIMESTAMP(14), PRIMARY KEY(user_name, session_id));";
    db_execute($query);
    
    $query = "CREATE TABLE file (user_name CHAR(30), file_name CHAR(255), file_size INT, upload_time TIMESTAMP(14), img_description CHAR(50), img_path CHAR(255), shortcut_path CHAR(255), PRIMARY KEY(user_name, file_name));";
    db_execute($query);
}

sub db_init #insert seed data
{
    my $query = "INSERT INTO user (user_name, pass_word) VALUES ('admin', 'admin');";
    db_execute($query);
    
    #this is for multi-user, need to do something else
    #my $query = "INSERT INTO user (user_name, pass_word) VALUES ('wyyi', 'haha');";
    #db_execute($query);
}

###################################################
###           Setup LogIn Interface             ###
###################################################

my $expire_time = "+2h";    # +2h means tow hours
my $expire_second = 2 * 3600;

# This function generates random strings of a given length
sub generate_random_string
{
	my $length_of_randomstring=shift @_;# the length of
    # the random string to generate
    
	my @chars=('a'..'z','A'..'Z','0'..'9','_');
	my $random_string;
	foreach (1..$length_of_randomstring)
	{
		# rand @chars will generate a random
		# number between 0 and scalar @chars
		$random_string.=$chars[rand @chars];
	}
	return $random_string;
}

sub cookie_gen  #usage: cookie_gen($CGI_o, $user_name, \$cookie1, \$cookie2)
# $flag = 1 is normal header, $flag = 2 is redirect header
{
    my $CGI_o = shift @_;
    my $user_name = shift @_;
    my $cookie1_ptr = shift @_;
    my $cookie2_ptr = shift @_;
    
    #Generate the random string and store it into database
    my $session_id = &generate_random_string(255);
    my $query = "INSERT INTO session (user_name, session_id, login_time) VALUES ('$user_name', '$session_id', CURRENT_TIMESTAMP);";
    db_execute($query);
    
    $$cookie1_ptr = $CGI_o->cookie(-name=>'user_name', -value=>$user_name, -expire=>$expire_time);
    $$cookie2_ptr = $CGI_o->cookie(-name=>'session_id', -value=>$session_id, -expire=>$expire_time);
}

sub cookie_get_user_name #usage cookie_get($CGI_o ,\$user_name)
{
    my $CGI_o = shift @_;
    my $user_name_ptr = shift @_;
    
    $$user_name_ptr = $CGI_o->cookie('user_name');
}

use Date::Parse;
use POSIX qw/strftime/;

sub cookie_check    #usage: cookie_check($CGI_o)
{
    my $CGI_o = shift @_;
    
    my $user_name = $CGI_o->cookie('user_name');
    my $session_id = $CGI_o->cookie('session_id');
    
    my $query = "SELECT login_time FROM session WHERE user_name='$user_name' AND session_id='$session_id';";
    my @result = ();
    my $row_len = "";
    db_execute($query, \@result, \$row_len);
    if($result[0])  #session exists
    {
        my $local_time = strftime("%Y-%m-%d %H:%M:%S", localtime);
        if(str2time($local_time) - str2time($result[0]) < $expire_second)
        {
            #print $CGI_o->header();
            #print "$local_time<=>$result[0]<br/>";
            return 1;
        }
        else
        {
            #remove record in database
            my $query = "DELETE FROM session WHERE user_name='$user_name' AND session_id='$session_id';";
            db_execute($query);
            return 0;
        }
    }
    else
    {
        #clean all the time out record
        my $local_time = strftime("%Y-%m-%d %H:%M:%S", localtime);
        
        my $query = "SELECT login_time FROM session WHERE 1;";
        my @result = ();
        my $row_len = "";
        db_execute($query, \@result, \$row_len);
        foreach my $i (@result)
        {
            if(str2time($local_time) - str2time($i) >= $expire_second)
            {
                my $query = "DELETE FROM session WHERE login_time='$i';";
                db_execute($query);
            }
        }
        return 0;
    }
}

###################################################
###           Setup LogOut Interface            ###
###################################################
sub log_out #delete session_id indatabase
            #usage: log_out($CGI_o)
{
    my $CGI_o = shift @_;
    
    my $user_name = $CGI_o->cookie('user_name');
    my $session_id = $CGI_o->cookie('session_id');
    
    if($user_name && $session_id)   #not empty
    {
        my $query = "DELETE FROM session WHERE user_name='$user_name' AND session_id='$session_id';";
        db_execute($query);
    }
}


###################################################
###          Setup Permanent Storage            ###
###################################################

my $data_dir = $ENV{"OPENSHIFT_DATA_DIR"};
my $img_dir = "_img";  #GLOBAL VARIABLE
my $shortcut_dir = "_shortcut";    #GLOBAL VARIABLE
my $temp_dir = "_temp";  #GLOBAL VARIABLE

sub clean_storage
{
    my $wanted_dir_name = `cd "$data_dir" && ls`;   #do not use `ls -A` since we don't want to delete directory start with .*
    my @wanted_dir_name_array = split(/\n/, $wanted_dir_name);
    
    foreach my $i (@wanted_dir_name_array)
    {
        #delete directory
        `cd "$data_dir" && rm -r "$i"`;
    }
}

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
        #create img dir
        `cd "$upload_dir" && mkdir "$user_name$img_dir"`;
    }
    if(!(-d "$upload_dir$user_name$shortcut_dir"))
    {
        #create shortcut dir
        `cd "$upload_dir"&& mkdir "$user_name$shortcut_dir"`;
    }
    if(!(-d "$upload_dir$user_name$temp_dir"))
    {
        #create temp dir
        `cd "$upload_dir"&& mkdir "$user_name$temp_dir"`;
    }
    
    ###TODO:check file size in an easy way...no can do
    
    #upload picture to $temp_dir
    if(!open(OUTFILE, ">", "$upload_dir$user_name$temp_dir/$file_name"))    #can't open file for writing
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
            if(-e "$upload_dir$user_name$temp_dir/$file_name")
            {
                `rm "$upload_dir$user_name$temp_dir/$file_name"`;
            }
            $$flag_ptr = 3;
            return;
        }
    }
    
    close(OUTFILE); #file uploaded
    
    #indentify the file
    my $identity = `identify -verbose "$upload_dir$user_name$temp_dir/$file_name" | grep Format:`;
    my @temp_array = split(/\n/, $identity);
    
    $_ = $identity;
    if(!/JPEG/ && !/GIF/ && !/PNG/)
    {
        #not match
        if(-e "$upload_dir$user_name$temp_dir/$file_name")
        {
            `rm "$upload_dir$user_name$temp_dir/$file_name"`;
        }
        $$flag_ptr = 5;
        return;
    }
    
    #check file existence
    my @result = ();
    my $row_len = "";
    my $query = "SELECT user_name, file_name FROM file WHERE user_name='$user_name' AND file_name='$file_name';";
    db_execute($query, \@result, \$row_len);
    if(@result || (-e "$upload_dir$user_name$img_dir/$file_name")) #exist
    {
        #Duplication handle interface, after all remove the file in $temp_dir
        $$flag_ptr = 2;
        return;
    }
    
    #move the temp file to $img_dir
    if(-e "$upload_dir$user_name$temp_dir/$file_name")
    {
        `mv "$upload_dir$user_name$temp_dir/$file_name" "$upload_dir$user_name$img_dir/$file_name"`;
    }
    #generate a shortcut, convert it to 100x100
    if(-e "$upload_dir$user_name$img_dir/$file_name")
    {
        `convert "$upload_dir$user_name$img_dir/$file_name" -resize 100x100 "$upload_dir$user_name$shortcut_dir/$file_name"`;
    }
    
    #convert description into viewable
    $_ = $description;
    $description =~ s/&/&amp;/g;
    $description =~ s/</&lt;/g;
    $description =~ s/>/&gt;/g;
    $description =~ s/\"/&quot;/g;
    $description =~ s/\'/&#39;/g;
    
    #upload description and other attributes to the database
    #add time stamp
    my $img_path = "$upload_dir$user_name$img_dir/$file_name";
    my $shortcut_path = "$upload_dir$user_name$shortcut_dir/$file_name";
    $query = "INSERT INTO file (user_name, file_name, file_size, upload_time, img_description, img_path, shortcut_path) VALUES ('$user_name', '$file_name', '$totalBytes', CURRENT_TIMESTAMP, '$description', '$img_path', '$shortcut_path');";  #remember the ' ' of SQL
    db_execute($query);
    
    $$flag_ptr = 1;
}

###################################################
###      Setup Duplication Upload Interface     ###
###################################################
sub get_temp_dir    #get the $upload_dir and $temp_dir
               #usage: get_dir(\$upload_dir, \$temp_dir)
{
    my $upload_dir_ptr = shift @_;
    my $temp_dir_ptr = shift @_;
    
    $$upload_dir_ptr = "$upload_dir";
    $$temp_dir_ptr = "$temp_dir";
}
sub get_img_dir    #get the $upload_dir and $temp_dir
#usage: get_dir(\$upload_dir, \$temp_dir)
{
    my $upload_dir_ptr = shift @_;
    my $img_dir_ptr = shift @_;
    
    $$upload_dir_ptr = "$upload_dir";
    $$img_dir_ptr = "$img_dir";
}

sub duplication_upload_pic  #usage: duplication_upload_pic($user_name, $description, $old_file_name, $new_file_name)  RENAME
                            #   or: duplication_upload_pic($user_name, $description, $old_file_name)  OVERWRITE
{
    my $user_name = shift @_;
    my $description = shift @_;
    my $old_file_name = shift @_;
    my $new_file_name = shift @_;
    
    #convert description into viewable
    
    $_ = $description;
    $description =~ s/&/&amp;/g;
    $description =~ s/</&lt;/g;
    $description =~ s/>/&gt;/g;
    $description =~ s/\"/&quot;/g;
    $description =~ s/\'/&#39;/g;
    
    my $totalBytes = -s "$upload_dir$user_name$temp_dir/$old_file_name";    #get filesize of $old_file_name
                                                                            #if it still in temp_dir
    
    if($old_file_name && $new_file_name)    #RENAME and upload
    {
        my $img_path = "$upload_dir$user_name$img_dir/$new_file_name";
        my $shortcut_path = "$upload_dir$user_name$shortcut_dir/$new_file_name";
        my $query;
        
        #fornow, the new_file_name file must not exist
        #rename the uploading file and upload it
        
        if(-e "$upload_dir$user_name$temp_dir/$old_file_name")
        {
            #move the temp file to $img_dir
            `mv "$upload_dir$user_name$temp_dir/$old_file_name" "$upload_dir$user_name$img_dir/$new_file_name"`;
            #generate a shortcut, convert it to 100x100
            `convert "$upload_dir$user_name$img_dir/$new_file_name" -resize 100x100 "$upload_dir$user_name$shortcut_dir/$new_file_name"`;
            
            #upload description and other attributes to the database
            #add time stamp
            $query = "INSERT INTO file (user_name, file_name, file_size, upload_time, img_description, img_path, shortcut_path) VALUES ('$user_name', '$new_file_name', '$totalBytes', CURRENT_TIMESTAMP, '$description', '$img_path', '$shortcut_path');";  #remember the ' ' of SQL
            db_execute($query);
        }
        else    #file not exists in temp_dir
        {
            #do nothing
            $query = "UPDATE file SET upload_time=CURRENT_TIMESTAMP, file_name='$new_file_name' WHERE user_name='$user_name' AND file_name='$old_file_name';";  #remember the ' ' of SQL
            db_execute($query);
        }
    }
    elsif($old_file_name && !$new_file_name) #OVERWRITE
    {
        my $img_path = "$upload_dir$user_name$img_dir/$old_file_name";
        my $shortcut_path = "$upload_dir$user_name$shortcut_dir/$old_file_name";
        my $query;
        
        #update existing file record in database, file in img_dir and shortcut_dir
        
        if(-e "$upload_dir$user_name$temp_dir/$old_file_name")
        {
            #move the temp file to $img_dir
            `mv "$upload_dir$user_name$temp_dir/$old_file_name" "$upload_dir$user_name$img_dir/$old_file_name"`;
            #generate a shortcut, convert it to 100x100
            `convert "$upload_dir$user_name$img_dir/$old_file_name" -resize 100x100 "$upload_dir$user_name$shortcut_dir/$old_file_name"`;
            
            #upload description and other attributes to the database
            #add time stamp
            
            ###I don't use update because there are sometime the file is in the dir but not insert into database
            $query = "DELETE FROM file WHERE user_name='$user_name' AND file_name='$old_file_name';";
            db_execute($query);
            #$query = "INSERT INTO file (user_name, file_name, file_size, upload_time, img_description, img_path, shortcut_path) VALUES ('$user_name', '$old_file_name', '$totalBytes', CURRENT_TIMESTAMP, '$description', '$img_path', '$shortcut_path');";
            #db_execute($query);
            
            #$query = "UPDATE file SET file_size='$totalBytes', upload_time=CURRENT_TIMESTAMP, img_description='$description' WHERE user_name='$user_name' AND file_name='$old_file_name';";
            db_execute($query);
        }
        else    #file not exists in temp_dir
        {
            #do nothing
            $query = "UPDATE file SET upload_time=CURRENT_TIMESTAMP WHERE user_name='$user_name' AND file_name='$old_file_name';";  #remember the ' ' of SQL
            db_execute($query);
        }
    }
}

###################################################
###        Setup Album Display Interface        ###
###################################################
#since the photos are store in the presistent storage
#are not accessable by the browser.
#we must create a symbolic link of the presisten dir
#so that we can get back the photo using browser

#add file "deploy" in [project_name]/.openshift/action_hooks/
#the file name must be "deploy"
#add line into "deploy"
#ln -s {OPENSHIFT_DATA_DIR} {OPENSHIFT_REPO_DIR}/perl/data

sub get_photo   #usage: get_photo($user_name, $amount, $option_sort, $option_order, \@result, \$row_len, \$count)
                #then we will get $amount number of photos of $user_name and sotre the result in \@result and \$row_len
{
    my $user_name = shift @_;
    my $amount = shift @_;
    my $option_sort = shift @_;
    my $option_order = shift @_;
    my $result_ptr = shift @_;
    my $row_len_ptr = shift @_;
    my $count_ptr = shift @_;
    
    my $query = "SELECT COUNT(*) FROM file WHERE user_name='$user_name';";
    db_execute($query, $result_ptr, $row_len_ptr);
    $$count_ptr = $$result_ptr[0];
    
    @$result_ptr = ();  #make it back to blank otherwise it will add to the back
    #$$row_len_ptr = "";
    
    if($option_order eq 1)  #Ascending
    {
        if($option_sort eq 1)   #sort by file size
        {
            $query = "SELECT file_name, file_size, img_description, img_path, shortcut_path FROM file WHERE user_name='$user_name' ORDER BY file_size;";
        }
        elsif($option_sort eq 2)    #sort by name
        {
            $query = "SELECT file_name, file_size, img_description, img_path, shortcut_path FROM file WHERE user_name='$user_name' ORDER BY BINARY file_name;";
        }
        elsif($option_sort eq 3)    #sort by Upload Time
        {
            $query = "SELECT file_name, file_size, img_description, img_path, shortcut_path FROM file WHERE user_name='$user_name' ORDER BY upload_time;";
        }
    }
    elsif($option_order eq 2)   #Decending
    {
        if($option_sort eq 1)   #sort by file size
        {
            $query = "SELECT file_name, file_size, img_description, img_path, shortcut_path FROM file WHERE user_name='$user_name' ORDER BY file_size DESC;";
        }
        elsif($option_sort eq 2)    #sort by name
        {
            $query = "SELECT file_name, file_size, img_description, img_path, shortcut_path FROM file WHERE user_name='$user_name' ORDER BY BINARY file_name DESC;";
        }
        elsif($option_sort eq 3)    #sort by Upload Time
        {
            $query = "SELECT file_name, file_size, img_description, img_path, shortcut_path FROM file WHERE user_name='$user_name' ORDER BY upload_time DESC;";
        }
    }
    
    db_execute($query, $result_ptr, $row_len_ptr);
    
    
    for(my $i = 0; $i < ($$row_len_ptr * $$count_ptr); $i++)  #($$row_len_ptr * $amount)
    {
        #$img_dir = '_img';
        #$shortcut_dir = '_shortcut';
        
        if(($i % $$row_len_ptr) eq 3)
        {
            my $img_path_for_show = "./data/$user_name$img_dir/$$result_ptr[$i - 3]";
            $$result_ptr[$i] = $img_path_for_show;
        }
        if(($i % $$row_len_ptr) eq 4)
        {
            my $shortcut_path_for_show = "./data/$user_name$shortcut_dir/$$result_ptr[$i - 4]";
            $$result_ptr[$i] = $shortcut_path_for_show;
        }
    }
}

sub remove_photo    #usage: remove_photo($user_name, @array_of_file_name)
{
    my $user_name = shift @_;
    my @array_file_name = @_;
    
    #print "<br/>user_name = $user_name<br/>array_file_name = @array_file_name<br/>";
    
    ###TODO: delete file in dir
    ###TODO: delete record in database
    
    #my $data_dir = $ENV{"OPENSHIFT_DATA_DIR"};
    #my $img_dir = "_img";  #GLOBAL VARIABLE
    #my $shortcut_dir = "_shortcut";    #GLOBAL VARIABLE
    #my $temp_dir = "_temp";  #GLOBAL VARIABLE
    foreach my $i (@array_file_name)
    {
        if(-e "$upload_dir$user_name$img_dir/$i")
        {
            `rm "$upload_dir$user_name$img_dir/$i"`;
            #my $out = `cd "$upload_dir$user_name$img_dir" && ls`;
            #print "<br/>out = $out<br/>";
            
            my $query = "DELETE FROM file WHERE user_name='$user_name' AND file_name='$i';";
            db_execute($query);
        }
        else{}
        if(-e "$upload_dir$user_name$shortcut_dir/$i")
        {
            `rm "$upload_dir$user_name$shortcut_dir/$i"`;
            #my $out = `cd "$upload_dir$user_name$shortcut_dir" && ls`;
            #print "<br/>out = $out<br/>"
        }
        else{}
    }
}

return 1;	#for header file, it must return 1, otherwise perl will exit with default value 0
