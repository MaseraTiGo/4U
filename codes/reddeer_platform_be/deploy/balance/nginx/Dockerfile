FROM tutum/nginx

RUN rm -rf /etc/nginx/sites-enabled/ \
    && mkdir -p /nginx/cdn \
    && chmod 777 /nginx/cdn \
    && mkdir -p /nginx/im \
    && chmod 777 /nginx/im

add conf/ /etc/nginx
