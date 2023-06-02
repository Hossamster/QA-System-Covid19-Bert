#get elastic search docker image
docker pull elasticsearch:7.17.10

#run the container
docker run -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.17.10