#!/usr/bin/perl -w

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
        "$file_name"<br/>
        "$description"<br/>
    </body>
</html>
__html_file__
#if end with __html_file__, must add a new line