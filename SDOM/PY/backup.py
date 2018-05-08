import shutil
import datetime

def backup():
    shutil.copy2('../.zzz/data.zzz','../.BackUps/'+str(datetime.datetime.now())+'.bak')
    print('Backup Complete...')

if __name__ == '__main__':
    inn = raw_input('Backup data.zzz now? (y/n)')
    if inn == 'y':
        backup()
    else:
        print('Cancelling Backup...')
    
