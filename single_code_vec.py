import pexpect
from pexpect.popen_spawn import PopenSpawn
from argparse import ArgumentParser
import os
import shutil

command = "python code2vec.py --load ../models/java14_model/saved_model_iter8.release  --predict  --export_code_vectors --only_code_vectors"

def read_args():
    parser = ArgumentParser()
    parser.add_argument("--file", dest="data_filename",
                            help="filename to get code vector", required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # copy a given file to Input.java, cause this is what is expected
    args = read_args()

    if not os.path.exists(args.data_filename):
        print("File {} does not exists".format(args.data_filename))
        exit

    shutil.copy(args.data_filename, 'Input.java')    
    

    child = pexpect.popen_spawn.PopenSpawn(command)
    child.timeout = 90
    child.expect("Modify the file")
    child.sendline('b')

    child.expect('Original name')
    funcname = child.readline()
    child.expect('Code vector:')
    child.readline()
    code_vec = child.readline()

    print(code_vec.strip())