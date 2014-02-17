#!/usr/bin/perl -w

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require "./lib.pl";

my $CGI_o = CGI->new();

my $old_CGI_o = $CGI_o->param("old_CGI_o");   #old query
$old_CGI_o = CGI->new($old_CGI_o);
my $user_name = $CGI_o->param("user_name");

my $file_name = $old_CGI_o->param("photo");
my $description = $old_CGI_o->param("description");


print $CGI_o->header();
print <<__html_file__;
<html>
    <body>
        "$user_name"<br/>
        "$file_name"<br/>
        "$description"<br/>
        "$old_CGI_o"<br>
    </body>
</html>
__html_file__
#if end with __html_file__, must add a new line