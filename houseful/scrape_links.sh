#!/bin/bash

page_num=1

while ((page_num <= 163))
do
    echo "Running scrapy with page_num=$page_num"
    scrapy crawl zolo_links -o links.csv -a page_num=$page_num
    sleep 5
    ((page_num++))
done