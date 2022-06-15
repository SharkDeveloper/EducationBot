
import threading
import time
import schedule
import datetime



def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


#def background_job():
#  print('Hello from the background thread')

"""def Notification_checker():
    print("time manager working")
    data = DataBase.get({"weekday":calendar.day_name[now.weekday()],"time":now.time().isoformat(timespec="minutes")})
    if data != None:
        bot.send_notification(data)
"""






