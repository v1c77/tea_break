# tea_break
-----------

you can just run the script with a crontab job...


    (crontab -l 2>/dev/null; echo "0 15 * * * SLACK_BOT_TOKEN=xoxp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx python yincha.py")| crontab -
    
    
> please make sure that the python version has been updated to 3.5.x or more.
