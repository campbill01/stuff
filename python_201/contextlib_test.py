from contextlib import contextmanager

@contextmanager
def file_open(path):
    try:
        f_obj = open(path, 'w')
        yield f_obj
    except OSError:
        print("Unable to open file")
    finally:
        print('Closing file')
        f_obj.close()

if __name__ == '__main__':
    with file_open('./test_file.txt') as fobj:
        fobj.write('Testing context manager')
