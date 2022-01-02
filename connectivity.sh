if [ $# -gt 2 ]
then
    ping=$(ping -c 1 $1 | grep "time=" | cut -d " " -f 8 | tr -d "time=")
    download_number=`curl -w '%{speed_download}\n' $2 | tail -n 1`
    upload_number=`scp -vi iutsshkey iutsshkey iut@iziram.fr:/home/iut/upload |& tail -n 2 | head -n 1 | cut -d " " -f 5`
    depoch=$(date +%s)
    echo "$ping,$download_number,$upload_number$depoch" >> $3
fi