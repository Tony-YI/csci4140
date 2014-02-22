#!/usr/bin/perl -w

use CGI;	#use the CGI module
use strict;	#then every variable should have "my"
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $CGI_o = CGI->new();

print $CGI_o->header();


use Date::Parse;
use POSIX qw/strftime/;


my $local_time = strftime("%Y-%m-%d %H:%M:%S", localtime);
my $local_second = str2time($local_time);
my $expire_second = 8;
my $target_second = $local_second + $expire_second;

while($target_second - $local_second)
{
    $local_time = strftime("%Y-%m-%d %H:%M:%S", localtime);
    $local_second = str2time($local_time);
}

print "Hello World";
