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

sub print_form
{
    print <<__html_file__;
    <form enctype="multipart/form-data" action="duplicate.cgi" method="POST">
    <input type="radio" name="duplicate" value="overwrite"/>Overwrite the existing file "$old_file_name".<br/><br/>
    <input type="radio" name="duplicate" value="rename"/>Rename the uploading file. New filename
    <input type="text" name="new_filename" maxlength="255" size="35"/><br/><br/>
    <input type="radio" name="duplicate" value="cancel"/>Cancle the current upload.<br/><br/>
    <input type="hidden" name="file_name" value="$old_file_name"/>
    <input type="hidden" name="description" value="$description"/>
    <input type="submit" value="Proceed"/>
    </form>
__html_file__
}

print $CGI_o->header();
print <<__html_file__;
<html>
    <body>
__html_file__

#check option
if($duplicate_option eq "overwrite")
{
    #update existing file record in database, file in img_dir and shortcut_dir
    duplication_upload_pic($user_name, $description, $old_file_name);
    print <<__html_file__;
    <title>Upload Successed</title>
    <p>File '"$old_file_name"' Overwriting Successed.</p><br/>
    <br/><a href="file_picking.html">Back to File Picking Interface</a>
    <br/><br/><a href="display_panel.html">Back to Display Panel</a>
__html_file__
}
elsif($duplicate_option = "rename")
{
    #check $new_file_name validation and no change ext
    $_ = $old_file_name;
    my ($old_name, $ext) = /([-a-z0-9_ ]+)\.([-a-z0-9_ ]+)/;
    $new_file_name =~ tr/A-Z/a-z/;  #convert uppercase to lowercase
    my @new_name = split('\.', $new_file_name);
    $_ = $new_name[0];
    @new_name = /([-a-z0-9_ ]+)/;
    
    #rename the uploading file and upload it if new_file_name file is not existed
    if($new_name[0])   #$new_file_name is not empty and valid
    {
        $new_file_name = $new_name[0].'.'.$ext;
        
        #check $new_file_existence
        my $upload_dir;
        my $temp_dir;
        get_dir(\$upload_dir, \$temp_dir);
        
        if(!(-e "$upload_dir$user_name$temp_dir/$new_file_name"))    #$new_file_name not exists in dir
        {
            duplication_upload_pic($user_name, $description, $old_file_name, $new_file_name);
            
            print <<__html_file__;
<html>
    <body>
        <title>Upload Successed</title>
        <p>File "$old_file_name" Renamed to "$new_file_name" and Upload Successed.</p><br/>
        <br/><a href="file_picking.html">Back to File Picking Interface</a>
        <br/><br/><a href="display_panel.html">Back to Display Panel</a>
__html_file__
        }
        else    #$new_file_name exists in dir
        {
            print <<__html_file__;
            <title>Duplication Handling Interface</title>
            <p>New File Name "$new_file_name" existed.</p><br/>
__html_file__
            
            print_form();
        }
    }
    else    #$new_file_name is empty or invalid
    {
        print "<title>Duplication Handling Interface</title><p>New File Name is empty or invalid.</p><br/>";
        print_form();
    }
}
elsif($duplicate_option = "cancel")
{
    #cancel upload process and delete the file in temp_dir
    my $upload_dir;
    my $temp_dir;
    get_dir(\$upload_dir, \$temp_dir);
    `rm "$upload_dir$user_name$temp_dir/$old_file_name"`;
    print "<title>Duplication Handling Interface</title><p>Upload Canceled.</p><br/>";
}
else    #nothing has been selected
{
    print "<title>Duplication Handling Interface</title><p>You must select one of these options.</p><br/>";
    print_form();
}

#######################################################
my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
my $img_dir = "_img";  #GLOBAL VARIABLE
my $shortcut_dir = "_shortcut";    #GLOBAL VARIABLE
my $temp_dir = "_temp";  #GLOBAL VARIABLE

my $out3 = `cd "$upload_dir" && ls -A`;
print "<h4>'upload_dir' = $out3</h4></br>";

$out3 = `cd "$upload_dir$user_name$temp_dir" && ls -A`;
print "<h4>'temp_dir' = $out3</h4></br>";

$out3 = `cd "$upload_dir$user_name$img_dir" && ls -A`;
print "<h4>'img_dir' = $out3</h4></br>";

$out3 = `cd "$upload_dir$user_name$shortcut_dir" && ls -A`;
print "<h4>'shortcut_dir' = $out3</h4></br>";
#######################################################

print <<__html_file__;
    </body>
</html>
__html_file__
#if end with __html_file__, must add a new line