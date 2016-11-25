#!/usr/bin/perl -w

#This .cgi file is used to pick and upload photos
#
#1. Allow the user to input a text description of the photo and maximum length is 50 characters
#2. Guarantee a viewable verbatim output. Convert <>"'&
#3. The maximum file size is 1MB. Upload fails if such requirement can not fulfilled
#4. The file extensions are: .jpg .gif and .png
#5. Filename contains only lower-case, digit and underscore. Convert the filename if needed
#6. Check whether the upload file is really an image or not. "identify". Otherwise, fails.
#7. Generate thumbnail of the photo. "convert". no name restriction
#8. Check whether the upload filename is already existed or not

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require './lib.pl';

my $CGI_o = CGI->new();

if(cookie_check($CGI_o) eq 0) #cookie is invalid
{
    #redirect
    print $CGI_o->redirect('./login.cgi');
}

print $CGI_o->header();
print <<__html_file__;
<html>
	<body>
		<title>File Picking Interface</title>
		<form enctype="multipart/form-data" action="upload.cgi" method="POST">
            <fieldset>
            <legend>File Picking Interface:</legend><br/>
            <input type="file" name="photo" accept="image/gif, image/jpeg, image/png" />
            <br/><br/>
            Description (50 characters max)
            <br/>
            <input type="text" name="description" maxlength="50" size="35"/>
            <br/>
            <br/>
            <input type="hidden" name="duplication_flag" value="NO"/>
            <input type="submit" value="Upload"/>
            </fieldset>
        </form>
        <br/>
        <a href="display_panel.cgi">Back to Display Panel</a>
	</body>
</html>
__html_file__
#if __html_file__ is the last line, must add a new line