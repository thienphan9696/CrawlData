import schedule
import time
import os

print('Scheduler initialised')
schedule.every(2).seconds.do(lambda: os.system('2+2'))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(1)