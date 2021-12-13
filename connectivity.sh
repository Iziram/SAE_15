if [ $# -gt 2 ]
then
    ping=$(ping -c 1 $1 | grep "time=" | cut -d " " -f 8 | tr -d "time=")
    touch /tmp/wget_verbose
    wget -O /tmp/test $2 -o /tmp/wget_verbose --delete-after
    download_text=`tail -n 2 /tmp/wget_verbose | cut -d "(" -f2 | cut -d ")" -f1`
    download_number=`echo $download_text | cut -d " " -f1`
    download_suffix=`echo $download_text | cut -d " " -f2`

    if [ $(echo $download_suffix | grep M -n) ]
    then
        download_number=`bc <<< $download_number*1000`
    fi

    depoch=$(date +%s)
    echo "$ping,$download_number,$depoch" >> $3
fi