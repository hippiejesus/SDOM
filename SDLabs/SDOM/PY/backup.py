import shutil
import datetime
import logger

def writeLog():
    lg = logger.log('backup')
    lg.write('Backing up at '+str(datetime.datetime.now()))
    lg.close()
    
def backup():
    shutil.copy2('../.zzz/data.zzz','../.BackUps/'+str(datetime.datetime.now())+'.bak')


if __name__ == '__main__':
    inn = raw_input('Backup data.zzz now? (y/n)')
    if inn == 'y':
        backup()
        writeLog()
        print('Backup Complete...')
    else:
        print('Cancelling Backup...')
    
