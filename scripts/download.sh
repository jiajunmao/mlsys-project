#wget https://minio.naturecraft.world/jiajunm-misc/scrape-result.zip
#mkdir -p ../data
#mv scrape-result.zip ../data
cd ../data && unzip scrape-result.zip
mv ../data/scrape-result/* ../data
rm -r ../data/scrape-result