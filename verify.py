from werkzeug.utils import secure_filename

ALL_FORMAT =['png','jpg','jpeg']

def check_format(name):
    print(name[-3::])
    if(name[-3::] in ALL_FORMAT):
        return True
    else:
        return False

def get_file_name(id,ext):
    return secure_filename(id+ext[-4::])

    