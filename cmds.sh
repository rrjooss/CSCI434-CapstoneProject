# Generate intervals.csv from timinings.csv (column labels added manually)
cat timings.csv | paste - - | sed -e 's/^([a-z]*\.(com|org)), ([^,]*), ([^,]*), start \1 ([^,]*), \3, end$/\1,\2,\3,\4/g' > intervals.csv

# Generate pkt_stats.csv from tcpdump.pcap
tshark -r tcpdump.pcap -Y "tcp.port == 80 or tcp.port == 443" -T fields -e frame.time_epoch -e frame.time_delta -e tcp.len -E separator=, -E header=y > pkt_stats.csv
