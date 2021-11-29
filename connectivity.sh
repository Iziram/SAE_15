if [ $# -gt 0 ]
then
    p=$(ping -c 1 $1 || echo "null")
    ping=$("$p" | grep "time=" | cut -d " " -f 8 | tr -d "time=")
    depoch=$(date +%s)
    echo $ping, $depoch
fi