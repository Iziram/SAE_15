if [ $# -gt 1 ]
then
    chemin=${0::-15}
    key="${chemin}iutsshkey"
    ping=$(ping -c 1 $1 | grep "time=" | cut -d " " -f 8 | tr -d "time=")
    download_number=`curl -w '%{speed_download}\n' $2 |& tail -n 1`
    upload_number=`scp -vi $key $key iut@iziram.fr:/home/iut/upload |& tail -n 2 | head -n 1 | cut -d " " -f 5`
    upload_number=${upload_number::-1}

    upload_number=`bc <<< $upload_number*1000 `
    upload_number=`bc <<< $upload_number/8 `
    upload_number=`bc <<< $upload_number/1000 `
    depoch=$(date +%s)
    echo "$ping,$download_number,$upload_number,$depoch"
fi