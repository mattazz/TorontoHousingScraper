@echo off
setlocal enabledelayedexpansion

set /a page_num=101

:loop
echo Running scrapy with page_num=!page_num!
scrapy crawl zolo -o listing.jl -a page_num=!page_num!
timeout /t 5
set /a page_num=!page_num!+1

if !page_num! leq 163 goto loop