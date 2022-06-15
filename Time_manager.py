#import aioschedule as schedule

import schedule
import time
import asyncio

def job():
    print("I'm working...")
async def fun():
    await schedule.every(10).seconds.do(job)
    await schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)