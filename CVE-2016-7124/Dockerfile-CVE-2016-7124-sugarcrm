# CVE-2016-7124

# docker php tag list
# https://www.seebug.org/vuldb/ssvid-92404
# https://github.com/docker-library/repo-info/blob/master/repos/php/tag-details.md
# http://stackoverflow.com/questions/33795923/how-to-connect-to-mysql-running-on-docker-from-the-host-machine
# http://stackoverflow.com/questions/7739645/install-mysql-on-ubuntu-without-password-prompt

FROM php:5.6-apache

RUN echo "deb http://mirrors.163.com/debian/ jessie main non-free contrib" > /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/debian/ jessie-updates main non-free contrib" >> /etc/apt/sources.list
RUN apt-get update

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install MYSQL-Server
RUN echo 'mysql-server mysql-server/root_password password password' | debconf-set-selections
RUN echo 'mysql-server mysql-server/root_password_again password password' | debconf-set-selections
RUN apt-get -y install mysql-server


# Install PHP extensions
RUN apt-get install -y libpng12-dev libjpeg-dev wget apt-utils
RUN docker-php-ext-configure gd --with-png-dir=/usr --with-jpeg-dir=/usr
RUN docker-php-ext-install -j$(nproc) mysqli gd zip

# Download and Extract SugarCRM
RUN wget -c -O sugarcrm_dev-6.5.23.tar.gz https://codeload.github.com/sugarcrm/sugarcrm_dev/tar.gz/6.5.23
RUN tar xvf sugarcrm_dev-6.5.23.tar.gz
RUN mv sugarcrm_dev-6.5.23/ /var/www/html/sugarcrm/
RUN chown -R www-data /var/www/html/sugarcrm/

CMD service mysql start && apache2-foreground

# How to use the Dockerfile ?
# $ docker build -t sugarcrm:CVE-2016-7124 -f Dockerfile .
# $ docker run -p 3306:3306 -p 80:80 sugarcrm:CVE-2016-7124
