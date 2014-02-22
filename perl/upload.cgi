#!/usr/bin/perl -w

###   This .cgi file is used to pick and upload photos   ###
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

sub print_header
{
    print $CGI_o->header();
    print <<__html_file__;
<html>
    <body>
__html_file__
}

sub print_form  #usage: print_form($file_name, $description)
{
    my $file_name = shift @_;
    my $description = shift @_;
    
    print <<__html_file__;
    <form enctype="multipart/form-data" action="upload.cgi" method="POST">
    <fieldset>
    <legend>Duplication Handle Interface:</legend><br/>
    <input type="radio" name="duplicate" value="overwrite"/>Overwrite the existing file "$file_name".<br/><br/>
    <input type="radio" name="duplicate" value="rename"/>Rename the uploading file. New filename
    <input type="text" name="new_filename" maxlength="255" size="35"/><br/><br/>
    <input type="radio" name="duplicate" value="cancel"/>Cancel the current upload.<br/><br/>
    <input type="hidden" name="file_name" value="$file_name"/>
    <input type="hidden" name="description" value="$description"/>
    <input type="hidden" name="duplication_flag" value="YES"/>
    <input type="submit" value="Proceed"/>
    </fieldset>
    </form>
__html_file__
}

if(cookie_check($CGI_o) eq 0) #cookie is invalid
{
    #redirect
    print $CGI_o->redirect('./login.cgi');
}

#get $user_name from cookies
my $user_name;
cookie_get_user_name($CGI_o, \$user_name);

my $duplication_flag = $CGI_o->param("duplication_flag");

if($duplication_flag eq "NO")   #nomal upload form
{
    my $file_name = $CGI_o->param("photo");
    my $description = $CGI_o->param("description");

    if(!$file_name) #no file selected
    {
        print_header();
        print "<title>Upload Failed</title><p>Upload Failed.<br/>File not selected or file too large.</p></body></html>";
        print <<__html_file__;
        <br/><a href="file_picking.cgi">Back to File Picking Interface</a>
        <br/><br/><a href="display_panel.cgi">Back to Display Panel</a>
    </body>
</html>
__html_file__
        exit 0;
    }

    #user selected a file
    $file_name =~ tr/A-Z/a-z/;  #convert uppercase to lowercase
    $_ = $file_name;
    my ($name, $ext) = /([-a-z0-9_ ]+)\.([-a-z0-9_ ]+)/;

    my $flag;   #1 is sucessful, 2 is file exited, 3 is file too large, 4 is can't open dir, 5 is invalid extension

    #check whether the file name and file ext is valided
    if($name && $ext)
    {
        if($ext eq "png" || $ext eq "jpg" || $ext eq "jpeg" || $ext eq "gif")
        {
            #check file size, check file existence and upload photo/description
            upload_pic($CGI_o, $user_name, $file_name, $description, \$flag);
            
            print_header();
            
            if($flag eq 1)    #upload sucessfully
            {
                print "<title>Upload Successed</title><p>Upload Successed.<br/></p>";
            }
            elsif($flag eq 2)   #file existed
            {
                #<inpute type="hidden" ..../>
                print <<__html_file__;
                <title>Duplication Handling Interface</title>
                <p>File "$file_name" already existed. Please select an option and proceed.</p><br/>
__html_file__
                print_form($file_name, $description);
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
    #my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
    #my $img_dir = "_img";  #GLOBAL VARIABLE
    #my $shortcut_dir = "_shortcut";    #GLOBAL VARIABLE
    #my $temp_dir = "_temp";  #GLOBAL VARIABLE

    #my $out3 = `cd "$upload_dir" && ls -A`;
    #print "<h4>'upload_dir' = $out3</h4></br>";

    #$out3 = `cd "$upload_dir$user_name$temp_dir" && ls -A`;
    #print "<h4>'temp_dir' = $out3</h4></br>";

    #$out3 = `cd "$upload_dir$user_name$img_dir" && ls -A`;
    #print "<h4>'img_dir' = $out3</h4></br>";

    #$out3 = `cd "$upload_dir$user_name$shortcut_dir" && ls -A`;
    #print "<h4>'shortcut_dir' = $out3</h4></br>";
    #######################################################

    if($flag != 2)
    {
        print <<__html_file__;
            <br/><a href="file_picking.cgi">Back to File Picking Interface</a>
            <br/><br/><a href="display_panel.cgi">Back to Display Panel</a>
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
}

if($duplication_flag eq "YES")  #duplication handler interface
{
    my $old_file_name = $CGI_o->param("file_name");
    my $new_file_name = $CGI_o->param("new_filename");
    my $description = $CGI_o->param("description");
    my $duplicate_option = $CGI_o->param("duplicate");
    
    #check option
    if($duplicate_option eq "overwrite")
    {
        #update existing file record in database, file in img_dir and shortcut_dir
        duplication_upload_pic($user_name, $description, $old_file_name);
        
        print_header();
        print <<__html_file__;
        <title>Upload Successed</title>
        <p>File "$old_file_name" Overwriting Successed.</p><br/>
        <br/><a href="file_picking.cgi">Back to File Picking Interface</a>
        <br/><br/><a href="display_panel.cgi">Back to Display Panel</a>
__html_file__
    }
    elsif($duplicate_option eq "rename")
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
            my $img_dir;
            my $temp_dir;
            get_img_dir(\$upload_dir, \$img_dir);
            get_temp_dir(\$upload_dir, \$temp_dir);
            
            if(!(-e "$upload_dir$user_name$img_dir/$new_file_name"))    #$new_file_name not exists in dir
            {
                duplication_upload_pic($user_name, $description, $old_file_name, $new_file_name);
                
                print_header();
                print <<__html_file__;
                <html>
                <body>
                <title>Upload Successed</title>
                <p>File "$old_file_name" Renamed to "$new_file_name" and Upload Successed.</p><br/>
                <br/><a href="file_picking.cgi">Back to File Picking Interface</a>
                <br/><br/><a href="display_panel.cgi">Back to Display Panel</a>
__html_file__
            }
            else    #$new_file_name exists in dir
            {
                print_header();
                print <<__html_file__;
                <title>Duplication Handling Interface</title>
                <p>New File Name "$new_file_name" existed.</p><br/>
__html_file__
                
                print_form($new_file_name, $description);
            }
        }
        else    #$new_file_name is empty or invalid
        {
            print_header();
            print "<title>Duplication Handling Interface</title><p>New File Name is empty or invalid.</p><br/>";
            print_form();
        }
    }
    elsif($duplicate_option eq "cancel")
    {
        #cancel upload process and delete the file in temp_dir
        my $upload_dir;
        my $temp_dir;
        get_temp_dir(\$upload_dir, \$temp_dir);
        if(-e "$upload_dir$user_name$temp_dir/$old_file_name")
        {
            `rm "$upload_dir$user_name$temp_dir/$old_file_name"`;
        }
        print_header();
        print <<__html_file__;
        <title>Duplication Handling Interface</title>
        <p>Upload Canceled.</p><br/>
        <br/><a href="file_picking.cgi">Back to File Picking Interface</a>
        <br/><br/><a href="display_panel.cgi">Back to Display Panel</a>
__html_file__
    }
    else    #nothing has been selected
    {
        print_header();
        print "<title>Duplication Handling Interface</title><p>You must select one of these options.</p><br/>";
        print_form($old_file_name, $description);
    }
    
    #######################################################
    #my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
    #my $img_dir = "_img";  #GLOBAL VARIABLE
    #my $shortcut_dir = "_shortcut";    #GLOBAL VARIABLE
    #my $temp_dir = "_temp";  #GLOBAL VARIABLE
    
    #my $out3 = `cd "$upload_dir" && ls -A`;
    #print "<h4>'upload_dir' = $out3</h4></br>";
    
    #$out3 = `cd "$upload_dir$user_name$temp_dir" && ls -A`;
    #print "<h4>'temp_dir' = $out3</h4></br>";
    
    #$out3 = `cd "$upload_dir$user_name$img_dir" && ls -A`;
    #print "<h4>'img_dir' = $out3</h4></br>";
    
    #$out3 = `cd "$upload_dir$user_name$shortcut_dir" && ls -A`;
    #print "<h4>'shortcut_dir' = $out3</h4></br>";
    #######################################################
    
    print <<__html_file__;
    </body>
    </html>
__html_file__
    #if end with __html_file__, must add a new line
}