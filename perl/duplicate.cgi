#!/usr/bin/perl -w

### This .cgi file is used to deal with the situaction  ###
### that the uploading file is already existed in the   ###
### server.                                             ###
### 1.Trigger only when there is a file with the        ###
###   filename exists in the system.                    ###
### 2.Only the filename is considered. No need to check ###
###   the content.                                      ###

###                     Choice:                         ###
### 1.Overwriting the existing file.                    ###
### 2.Renaming the uploading file. Can't change ext     ###
### 3.Canceling upload.                                 ###

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require "./lib.pl";

my $CGI_o = CGI->new();

my $user_name = "admin";    ###TODO: get the $user_name from cookies
my $old_file_name = $CGI_o->param("file_name");
my $new_file_name = $CGI_o->param("new_filename");
my $description = $CGI_o->param("description");
my $duplicate_option = $CGI_o->param("duplicate");

#check option
if($duplicate_option eq "overwrite")
{
    #update existing file record in database, file in img_dir and shortcut_dir
    duplication_upload_pic($user_name, $description, $old_file_name);
}
elsif($duplicate_option = "rename")
{
    ###TODO: check $new_file_name validation and no change ext
    $_ = $old_file_name;
    my ($old_name, $ext) = /([a-z0-9_]+)\.([a-z0-9_]+)/;
    $new_file_name =~ tr/A-Z/a-z/;  #convert uppercase to lowercase
    my @new_name = split('\.', $new_file_name);
    $_ = $new_name[0];
    @new_name = /([a-z0-9_]+)/;
    
    #rename the uploading file and upload it if new_file_name file is not exst
    if($new_name[0])   #$new_file_name is not empty or valid
    {
        $new_file_name = $new_name[0].'.'.$ext;
        
        ###TODO: check $new_file_existence
        if()    #$new_file_name not exists in dir
        {
            duplication_upload_pic($user_name, $description, $old_file_name, $new_file_name);
        }
        else    ##$new_file_name exists in dir
        {
            
        }
    }
    else    #$new_file_name is empty or invalid
    {
        
    }
}
elsif($duplicate_option = "cancel")
{
    ###TODO: cancel upload process and delete the file in temp_dir
}
else    #nothing has been selected
{
    ###TODO: ???
}

print $CGI_o->header();
print <<__html_file__;
<html>
    <body>
    hahahaha
    </body>
</html>
__html_file__
#if end with __html_file__, must add a new line