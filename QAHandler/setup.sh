version= `date "+%M-%M-%S_%d-%m-%y"`
echo $version

sudo docker built -t qa-api .
sudo docker tag qa-api qa-api:version

#sudo docker run -p 85:8080 -e es_ip='localhost' -e es_port=9200 qa-api