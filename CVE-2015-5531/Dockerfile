# CVE-2015-5531

# docker apache tag list
# https://github.com/docker-library/repo-info/blob/master/repos/debian/tag-details.md
FROM java:8

# Download and Extract elasticsearch
RUN wget -c -O elasticsearch-1.3.4.tar.gz https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.3.4.tar.gz
RUN tar xvf elasticsearch-1.3.4.tar.gz && rm -rf elasticsearch-1.3.4.tar.gz

CMD ["/elasticsearch-1.3.4/bin/elasticsearch"]

# How to use the Dockerfile ?
# $ docker build -t elasticsearch:CVE-2015-5531 -f Dockerfile .
# $ docker run -d -p 9200:9200 elasticsearch:CVE-2015-5531


## References
# https://stackoverflow.com/questions/36663742/docker-unauthorized-authentication-required-upon-push-with-successful-login
# https://stackoverflow.com/questions/29956500/docker-public-registry-push-fails-repository-does-not-exist/37036348