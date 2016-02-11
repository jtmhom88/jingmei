#!/usr/bin/perl

use strict;
use DBI;
use DateTime;
use JSON;

# redirect STDERR to STDOUT
*STDERR = *STDOUT;


# Set Globals
#my $ipaddress = "172.31.27.121";
#my $host = "172.31.39.51";
my $host = $ENV{'MYSQL_IP'};
my $user = $ENV{'MYSQL_USER'};
my $anshobango = $ENV{'MYSQL_PWD'};
my $database = 'sentiment';

#print "$host $user $anshobango $database \n";

# Get all the keywords
my $key_file = "./conf/keywords.txt";
open(my $fh, $key_file) || die "Cannot read $key_file\n";;
my @keywords;
while (my $row = <$fh>) {
  #print $row;
  chomp($row);
  if ($row =~ m/(\w+)/) {
    #print "match $1\n";
    push(@keywords,$1);
  };
};

# my $teststring = "http://www.thestreet.com/story/13426926/1/vw-digs-itself-into-deeper-hole-over-diesel-emissions.html";
# $teststring = lc($teststring);
# print "Teststring: $teststring\n";

# foreach my $word (@keywords) {
#    if ($teststring =~ m/$word/) {
#      print "Found: $word $teststring\n";
#    }
# }
# die "OOPS";

# Connect to Mysql
my $dbh = DBI->connect(
    "dbi:mysql:dbname=$database;host=$host",
    "$user",
    "$anshobango",
    {RaiseError => 1, AutoCommit =>1, mysql_auto_reconnect=>1}
) or die $DBI::errstr;

# Get article urls
my $table = 'article_urls';

my $sql = "SELECT * from $database.$table where dt_modified > DATE_SUB(NOW(), INTERVAL 2 HOUR) ";

my $sth = $dbh->prepare($sql)
    || die "$DBI::errstr";
$sth->execute();

my %relevancy;
my $i=0;
# Print number of rows found
if ($sth->rows < 0) {
    die "Zero rows found.\n";
} else {
    # Loop if results found
    while (my $results = $sth->fetchrow_hashref) {
			my $idx = $results->{idx}; # get idx
			my $url = $results->{url}; # get the URL field
			$url = lc($url); # lowercase
			my $title = $results->{title}; # get the URL field
			#print "$idx $url $title\n";
			foreach my $word (@keywords) {
			  if ($url =~ /$word/) {
			    #print "Found: $word in $url\n";
			    $relevancy{$idx}++;
			    $i++;
			  }
			}
    }
}
print "Found $i rows\n";
printf ">> Total %d rows\n", $sth->rows;

$i=0;
foreach my $key (keys %relevancy) {
	print "$key $relevancy{$key}\n";
	my $sql="UPDATE IGNORE $database.$table set relevancy_score=$relevancy{$key} where idx=$key ";
	print "$sql\n";
	$dbh->do($sql) || die "$DBI::errstr";;
	$i++;
}
print "Total matched urls $i\n";

# Disconnect
$sth->finish;
$dbh->disconnect;

exit;

