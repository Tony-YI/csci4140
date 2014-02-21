#!/usr/bin/perl -w

### This .cgi file is used to display the photos inside the album    ###
### 1. To view the album                                             ###
### 2. Remove photos from the album                                  ###
### 3. Only the inputs shown in the page is valid                    ###
### 4. The valid range for row and column is 1-9 inclusively         ###
### 5. Split in to pages if the number of photos in the album is     ###
###    larger than row*column                                        ###
### 6. Sort the display, sort by size, by name, by upload time.      ###
###    descending/ascending                                          ###
### 7. Display thumbnails only                                       ###
### 8. Display description of the photo when mouse move to the photo ###
### 9. Click and display the target photo                            ###
### 10. For un-authorized user, the album is read only               ###

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require "./lib.pl";

my $CGI_o = CGI->new();

my $user_name = 'admin';                                    ###TODO: get $user_name from cookies
my $submit = $CGI_o->param('submit');
my $last_option_r = $CGI_o->param('last_option_r');
my $last_option_c = $CGI_o->param('last_option_c');
my $last_option_sort = $CGI_o->param('last_option_sort');
my $last_option_order = $CGI_o->param('last_option_order');
my $last_option_page = $CGI_o->param('last_option_page');

my $option_r;
my $option_c;
my $option_sort;
my $option_order;
my $option_page;
my @option_remove;

print $CGI_o->header();

if($submit eq "Change") #string can't use == must use eq
{
    #submitted by "change" button
    #print "change<br/>";
    $option_r = $CGI_o->param('option_r');
    $option_c = $CGI_o->param('option_c');
    $option_sort = $CGI_o->param('option_sort');
    $option_order = $CGI_o->param('option_order');
    $option_page = 1;
    @option_remove = ();
}
elsif($submit eq "Remove Selected")
{
    #submitted by "Remove Selected" button
    #print "remove<br/>";
    $option_r = $last_option_r;
    $option_c = $last_option_c;
    $option_sort = $last_option_sort;
    $option_order = $last_option_order;
    $option_page = 1;
    #remove photo
    @option_remove = $CGI_o->param('option_remove');
    if(@option_remove)
    {
        remove_photo($user_name, @option_remove);
    }
}
elsif($submit eq "Go to Page")
{
    #submitted by "Go to Page" button
    #print "page<br/>";
    $option_r = $last_option_r;
    $option_c = $last_option_c;
    $option_sort = $last_option_sort;
    $option_order = $last_option_order;
    $option_page = $CGI_o->param('option_page');
    @option_remove = ();
}
else
{
    #first load
    #default values
    #print "default<br/>";
    $option_r = 3;
    $option_c = 8;
    $option_sort = 3;
    $option_order = 2	;
    $option_page = 1;
    @option_remove = ();
}

$last_option_r = $option_r;
$last_option_c = $option_c;
$last_option_sort = $option_sort;
$last_option_order = $option_order;
$last_option_page = $option_page;

print <<__html_file__;
<html>
    <body>
        <title>Album Display Interface</title>
        <form method="POST" action="album_display.cgi">
            <fieldset>
            <legend>Album Display Interface:</legend><br/>
            Dimension
            <select name="option_r" autofocus>
__html_file__

my $i;
for($i = 1; $i < 10; $i++)
{
    if($i eq $last_option_r)
    {
        print "<option value=$i selected>$i</option>\n";
    }
    else
    {
        print "<option value=$i>$i</option>\n";
    }
}

print <<__html_file__;
            </select>
            X
            <select name="option_c" autofocus>
__html_file__

for($i = 1; $i < 10; $i++)
{
    if($i eq $last_option_c)
    {
        print "<option value=$i selected>$i</option>\n";
    }
    else
    {
        print "<option value=$i>$i</option>\n";
    }
}

print <<__html_file__;
            </select>

            &nbsp;&nbsp;&nbsp;&nbsp;Sort By
            <select name="option_sort" autofocus>
__html_file__

my @sort_type = ('File Size', 'Name', 'Upload Time');

for($i = 1; $i <= 3; $i++)
{
    if($i eq $option_sort)
    {
        print "<option value=$i selected>$sort_type[$i - 1]</option>\n";
    }
    else
    {
        print "<option value=$i>$sort_type[$i - 1]</option>\n";
    }
}

print <<__html_file__;
            </select>

            &nbsp;&nbsp;&nbsp;&nbsp;
            Order
            <select name="option_order" autofocus required>
__html_file__

my @order_type = ('Ascending', 'Descending');

for($i = 1; $i <= 2; $i++)
{
    if($i eq $option_order)
    {
        print "<option value=$i selected>$order_type[$i - 1]</option>\n";
    }
    else
    {
        print "<option value=$i>$order_type[$i - 1]</option>\n";
    }
}

print <<__html_file__;
            </select>

            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="submit" name="submit" value="Change"/><br/>
__html_file__

#get photos
my $amount = $option_r * $option_c;
my @result;
my $row_len;    #number of attributes in one database result
my $count;      #number of records in the "file" table inside database

get_photo($user_name, $amount, $option_sort, $option_order, \@result, \$row_len, \$count);

#print "<br/>@result<br/>";

#show photos
my $total_page = int($count / $amount);
if($count % $amount)
{
    $total_page++;
}

my $photo_in_one_page = $amount;
if($count < $amount)
{
    $photo_in_one_page = $count;
}

print <<__html_file__;
            <br/>
            <table>
__html_file__

for($i = 1; $i <= $photo_in_one_page; $i++)
{
    if(($i % $option_c) eq 1)   #start of an row
    {
        print "<tr>";
    }
    
    if($result[ ($row_len*$i)-1 + ($option_page-1)*($row_len*$photo_in_one_page)-1])
    {
        my $shortcut_src = $result[ ($row_len*$i) + ($option_page-1)*($row_len*$photo_in_one_page) - 1 ];
        my $img_src = $result[ ($row_len*$i)-1 + ($option_page-1)*($row_len*$photo_in_one_page) - 1 ];
        my $title = $result[ ($row_len*$i)-2 + ($option_page-1)*($row_len*$photo_in_one_page) - 1 ];
        my $photo_name = $result[ ($row_len*$i)-4 + ($option_page-1)*($row_len*$photo_in_one_page) - 1 ];
        print <<__html_file__;
                <td style="width:142px">
                <div style="align:center; height:100px; width:100px">
                <a href="$img_src">
                <img title="$title" src="$shortcut_src" style="max-height:100%; max-width:100%"/>
                </a>
                </div>
                <div style="width:120px; align:center">
                <p>
                <input type="checkbox" name="option_remove" value="$photo_name"/>
                $photo_name
                </p>
                </div>
                </td>
__html_file__
    }
    
    if(($i % $option_c) eq 0)    #end of a row
    {
        print "</tr>";
    }
}

#print the remain form
print <<__html_file__;
            </table><br/>
            <input type="submit" name="submit" value="Remove Selected"/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            Page
            &nbsp;&nbsp;
            <select name="option_page" autofocus>
__html_file__

for($i = 1; $i <= $total_page; $i++)
{
    if($i eq $last_option_page)
    {
        print "<option value=$i selected>$i</option>\n";
    }
    else
    {
        print "<option value=$i>$i</option>\n";
    }
}

print <<__html_file__;
            </select>
            &nbsp;&nbsp;
            of
            &nbsp;&nbsp;
            $total_page
            &nbsp;&nbsp;&nbsp;&nbsp;
            <input type="submit" name="submit" value="Go to Page"/>
__html_file__


print <<__html_file__;
            <input type="hidden" name="last_option_r" value="$last_option_r">
            <input type="hidden" name="last_option_c" value="$last_option_c">
            <input type="hidden" name="last_option_sort" value="$last_option_sort">
            <input type="hidden" name="last_option_order" value="$last_option_order">
            <input type="hidden" name="last_option_page" value="$last_option_page">
__html_file__

#########################
#print "<br/>submit = $submit<br/>count = $count<br/>option_r = $option_r<br/>option_c = $option_c<br/>amount = $amount<br/>option_sort = $option_sort<br/>option_order = $option_order<br/>option_page=$option_page<br/>option_remove = @option_remove<br/>";
#########################

print <<__html_file__;
            </fieldset>
        </form>
        <br/><br/>
        <a href="display_panel.html">Back to Display Panel</a>
    </body>
</html>
__html_file__
#if __html_file__ is the last, then must add a new line