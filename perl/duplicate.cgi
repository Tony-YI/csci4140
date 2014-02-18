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
my $new_file_name = $CGI_o->param("new_filename");  ###TODO: check filename validation and no change ext
my $description = $CGI_o->param("description");
my $duplicate_option = $CGI_o->param("duplicate");

#check option
if($duplicate_option eq "overwrite")
{
    duplication_upload_pic($user_name, $description, $old_file_name);
    ###TODO: update existing file record in database, file in img_dir and shortcut_dir
}
elsif($duplicate_option = "rename")
{
    ###TODO: rename the uploading file and upload it if new_file_name file is not exst
    if($new_file_name)  #new_file_name not empty
    {
        ###TODO: check whether $new_file_name is valid or not
        duplication_upload_pic($user_name, $description, $old_file_name, $new_file_name);
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