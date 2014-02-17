#!/usr/bin/perl -w

###   This .html file is used to pick and upload photos   ###
###   1. Allow the user to input a text description of    ###
###      the photo and maximum length is 50 characters    ###
###   2. Guarantee a viewable verbatim output.            ###
###      Convert <>"'&                                    ###
###   3. The maximum file size is 1MB. Upload fails if    ###
###      such requirement can not fulfilled               ###
###   4. The file extensions are: .jpg .gif and .png      ###
###   5. Filename contains only lower-case, digit and     ###
###      underscore. Convert the filename if needed       ###
###   6. Check whether the upload file is really an       ###
###      image or not. "identify". Otherwise, fails.      ###
###   7. Generate thumbnail of the photo. "convert".      ###
###      no name restriction                              ###
###   8. Check whether the upload filename is already     ###
###      existed or not                                   ###

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require "./lib.pl";

my $CGI_o = CGI->new();

my $user_name = "admin"; ###############################################
my $file_name = $CGI_o->param("photo");
my $description = $CGI_o->param("description");

print $CGI_o->header();
print <<__html_file__;
<html>
<body>
__html_file__

if(!$file_name) #no file selected
{
    print "<title>Upload Failed</title><p>Upload Failed.<br/>You must select a file.</p></body></html>";
    
    exit 0;
}

#user selected a file
$file_name =~ tr/A-Z/a-z/;  #convert uppercase to lowercase
$_ = $file_name;
my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;

#check whether the file name and file ext is valided
if($name && $ext)
{
    if($ext eq "png" || $ext eq "jpg" || $ext eq "jpeg" || $ext eq "gif")
    {
        #check file size, check file existence and upload photo/description
    }
    else    #invalid extension
    {
        print "<title>Upload Failed</title><p>Upload Failed.<br/>Only [.jpg .jpeg .png .gif] file is allowed.</p></body></html>"
        
        exit 0;
    }
}
else    #ivalid file name and file extension
{
    print "<title>Upload Failed</title><p>Upload Failed.<br/>You file name is invalid.</p></body></html>";
    
    exit 0;
}

print <<__html_file__;
    </body>
</html>
__html_file__
#if end with __html_file__, must add a new line