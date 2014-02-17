#!/usr/bin/perl -w

use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

require "./lib.pl";

my $CGI_o = CGI->new();

my $user_name = $CGI_o->param("user_name")
my $file_name = $CGI_o->param("file_name");
my $description = $CGI_o->param("description");
my $CGI_o_ptr = $CGI_o->param("CGI_o_ptr");

print $CGI_o->header();
print <<__html_file__;
<html>
    <body>
        "$user_name"<br/>
        "$file_name"<br/>
        "$description"<br/>
        "$CGI_o_ptr"<br>
    </body>
</html>
__html_file__
#if end with __html_file__, must add a new line