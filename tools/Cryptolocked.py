import ntpath
import os.path
from services.utils import *
from datetime import datetime, timedelta

N_TENTACTLES = 5
MAX_WORKERS = 5
DATABASE = "persistent/cryptolocked.db"


class Cryptolocked(Core):
    def __init__(self, tool):
        super().__init__()
        self.files = []
        self.paths = tool.paths
        self.method = get_method(tool.method)
        self.action = ""

    def initialization(self):
        filenames = {}
        # create a list of random filenames in the given paths
        for path in self.paths:
            if os.path.isdir(path):
                log.sintetic_write(log.DEBUG, "CRYPTOLOCKED", "will monitor '{}'".format(path))
                for i in range(N_TENTACTLES):
                    # why while loop? we do not want to have duplicates in dict, so if duplicate do it again
                    while True:
                        name = str(hex(random.randint(1, 10000))[2:])
                        filename = path + '/' + name
                        if name not in filenames:
                            filenames[name] = filename
                            break
            else:
                log.sintetic_write(log.ERROR, "CRYPTOLOCKED", "error, '{}' is not a directory".format(path))

        # DB initialization
        conn = create_connection(DATABASE)
        if conn is not None:
            create_table_files(conn)
        else:
            log.sintetic_write(log.ERROR, "CRYPTOLOCKED", "error, cannot create the DB connection")

        # Clean previous trip files and DB
        cryptolocked_clean(conn)

        # Place trip files
        for name, filename in filenames.items():
            if file_exists(filename):
                destroy_file(filename)
            content = rand_data()
            create_file(filename, content, None)
            date = random_date(datetime.now() - timedelta(days=120), datetime.now(), random.random())
            modTime = time.mktime(date.timetuple())
            os.utime(filename, (modTime, modTime))
            try:
                subprocess.check_output("auditctl -w {} -p war".format(filename), shell=True)
            except subprocess.CalledProcessError as e:
                log.sintetic_write(log.DEBUG, "CRYPTOLOCKED", "auditctl error: {}".format(e.output))
            db_insert_file_entry(conn, filename)
            self.files.append(filename)
        log.sintetic_write(log.INFO, "CRYPTOLOCKED", "finished initialization")
        return self.files

    def process(self, event):
        (header, types, target, name) = event
        mask = header.mask
        self.action = get_action(mask)
        if not (mask & Core.IN_ISDIR):
            if check_mask(mask):
                conn = create_connection(DATABASE)
                if conn is None:
                    log.sintetic_write(log.ERROR, "CRYPTOLOCKED", "error, cannot create the DB connection")

                if len(name) == 0:
                    _, name = ntpath.split(target)

                if is_in_file(conn, target):
                    audit_info, ppid, comm, user = check_audit(target)
                    # TODO: check audit should look for path+name, but for unknown reasons sometimes
                    #  it doesn't work by providing the entire path

                    if self.method & Core.LOG_EVENT:
                        log.sintetic_write(log.CRITICAL, "CRYPTOLOCKED", "file '{}' has been {}! {}"
                                           .format(target, self.action, audit_info))
                    # execute action only if the event was not caused by adarch itself
                    if comm != "adarch":
                        execute_action("CRYPTOLOCKED", self.method, ppid, user, target)
        return
