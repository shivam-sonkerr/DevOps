import zipfile
import gzip
import learn_csv
import shutil

print('Enter the path of the main zip file')

source_directory = input()

dest_directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'zips', 'files')

os.makedirs(dest_directory, exist_ok=True)

for filename in os.listdir(source_directory):

    if filename.endswith('.zip'):
        zip_path = os.path.join(source_directory, filename)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_directory)

subfolders = next(os.walk(dest_directory))[1]

gz_folder = os.path.join(dest_directory, subfolders[0])

for filename in os.listdir(gz_folder):
    if filename.lower().endswith('.gz'):
        gz_path = os.path.join(gz_folder, filename)

        output_path = os.path.join(gz_folder, filename[:-3])

        with gzip.open(gz_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(gz_path)
        print(f"Extracted: {filename}")

print("All files extracted successfully")

logPath = gz_folder

check_path_existence = os.path.exists(logPath)

if not check_path_existence:
    print("The given path is not valid, please check if it exists")

if logPath.startswith("'"):
    print("Please remove single quotes from the path and then re-enter path of the log file")

print('Path of the log file given is: ', logPath)


# ecm = open(logPath)


def process_logs():
    os.makedirs(os.path.join(os.path.expanduser('~'), 'Downloads', 'logs'), exist_ok=True)

    error_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'logs', 'error.log')
    debug_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'logs', 'debug.log')
    extra_info_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'logs', 'extra.log')

    print("Press 1 for ERROR logs\n Press 2 for DEBUG logs\n Press 3 for WARN logs \n Press 4 for INFO logs \n Press "
          "Press 5 for CRITICAL logs\n Press 6 for worker logs\n Press 7 for Keyword specific search")
    log_type = input()

    thread = None
    if log_type == '6':
        print("Enter the worker thread for which you want the logs:")
        thread = input()

    keyword_search = None
    if log_type == '7':
        print('Enter the keyword to be searched in the logs')
        keyword_search = input()


    with open(error_file_path, 'a',encoding='utf-8', errors='replace') as error, \
            open(debug_file_path, 'a',encoding='utf-8', errors='replace') as debug, \
            open(extra_info_file_path, 'a',encoding='utf-8', errors='replace') as extra:

        for filename in os.listdir(logPath):
            file_path = os.path.join(logPath, filename)

            with open(file_path, 'r',encoding='utf-8', errors='replace') as ecm:
                for line in ecm:
                    if 'ERROR' in line and log_type == '1':
                        error.write(line)
                    elif 'DEBUG' in line and log_type == '2':
                        debug.write(line)
                    elif 'WARN' in line and log_type == '3':
                        extra.write(line)
                    elif 'INFO' in line and log_type == '4':
                        extra.write(line)
                    elif 'CRITICAL' in line and log_type == '5':
                        extra.write(line)
                    elif f'quartzScheduler_Worker-{thread}' in line and log_type == '6':
                        extra.write(line)
                    elif log_type == '7' and keyword_search and keyword_search in line:
                        extra.write(line)

    print("Logs have been collected, please check now")


process_logs()
