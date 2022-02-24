import logging
import datetime



def clear_files(self, uid_to_be_deleted):
    logging.basicConfig(filename="{}.log".format(datetime.datetime.now()), level=logging.INFO)
    for uid in uid_to_be_deleted:
        if os.path.exists('{}/{}.ics'.format(Path.cwd(), uid)):
            os.remove('{}/{}.ics'.format(Path.cwd(), uid))
            logging.info('{} - {}.ics successfully removed.'.format(datetime.datetime.now(), uid))
        else:
            logging.error('{} - {}.ics not found. File could not be removed.'.format(datetime.datetime.now(), uid))