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
    print <<__html_file__;
    <br/><a href="file_picking.html">Back to File Picking Interface</a>
    <br/><br/><a href="display_panel.html">Back to Display Panel</a>
    </body>
</html>
__html_file__
    exit 0;
}

#user selected a file
$file_name =~ tr/A-Z/a-z/;  #convert uppercase to lowercase
$_ = $file_name;
my ($name, $ext) = /([a-z0-9_]+)\.([a-z0-9_]+)/;

my $flag;   #1 is sucessful, 2 is file exited, 3 is file too large, 4 is can't open dir, 5 is invalid extension

#check whether the file name and file ext is valided
if($name && $ext)
{
    if($ext eq "png" || $ext eq "jpg" || $ext eq "jpeg" || $ext eq "gif")
    {
        #check file size, check file existence and upload photo/description
        upload_pic(\$CGI_o, $user_name, $file_name, $description, \$flag);
        if($flag eq 1)    #upload sucessfully
        {
            print "<title>Upload Successed</title><p>Upload Successed.<br/></p>";
        }
        elsif($flag eq 2)   #file existed
        {
            my $CGI_o_ptr = "\$CGI_o";
            print <<__html_file__;
            <title>Duplication Handling Interface</title>
            <form action="duplicate.cgi" method="POST">
                <input type="radio" name="duplicate" value="overwrite"/>Overwrite the existing file "$file_name".<br/><br/>
                <input type="radio" name="duplicate" value="rename"/>Rename the uploading file. New filename
                <input type="text" name="new_filename" maxlength="255" size="15"/><br/><br/>
                <input type="radio" name="duplicate" value="cancle"/>Cancle the current upload.<br/><br/>
                <input type="hidden" name="user_name" value="$user_name"/>
                <input type="hidden" name="file_name" value="$file_name"/>
                <input type="hidden" name="description" value="$description"/>
                <input type="hidden" name="CGI_o_ptr" value="$CGI_o_ptr"/>
                <input type="submit" value="Proceed"/>
            </form>
__html_file__
        }
        elsif($flag eq 3)   #file size too large
        {
            print "<title>Upload Failed</title><p>Upload Failed.<br/>The maximun file size of each photo is 1 MB.</p>";
        }
        elsif($flag eq 4)   #can't open dir
        {
            print "<title>Upload Failed</title><p>Upload Failed.<br/>Can't open file for writing.</p>";
        }
        elsif($flag eq 5)   #invalid extension
        {
            print "<title>Upload Failed</title><p>Upload Failed.<br/>Only [.jpg .jpeg .png .gif] file is allowed.</p>";
        }
        else    #unknown error
        {
            print "<title>Upload Failed</title><p>Upload Failed.<br/>Unknown ERROR.</p>";
        }
    }
    else    #invalid extension
    {
        print "<title>Upload Failed</title><p>Upload Failed.<br/>Only [.jpg .jpeg .png .gif] file is allowed.</p>";
    }
}
else    #ivalid file name and file extension
{
    print "<title>Upload Failed</title><p>Upload Failed.<br/>You file name is invalid.</p>";;
}

#######################################################
my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
my $img_dir = "_img";  #GLOBAL VARIABLE
my $shortcut_dir = "_shortcut";    #GLOBAL VARIABLE

my $out3 = `cd "$upload_dir" && ls -A`;
print "<h4>$out3</h4></br>";

$out3 = `cd "$upload_dir$user_name$img_dir" && ls -A`;
print "<h4>$out3</h4></br>";

$out3 = `cd "$upload_dir$user_name$shortcut_dir" && ls -A`;
print "<h4>$out3</h4></br>";
#######################################################

if($flag != 2)
{
    print <<__html_file__;
        <br/><a href="file_picking.html">Back to File Picking Interface</a>
        <br/><br/><a href="display_panel.html">Back to Display Panel</a>
    </body>
</html>
__html_file__
}
else
{
    print <<__html_file__;
    </body>
    </html>
__html_file__
}
#if end with __html_file__, must add a new line