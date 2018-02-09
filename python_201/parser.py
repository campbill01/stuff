import argparse

def get_args():
    """ some doc type stuff """
    parser = argparse.ArgumentParser(
        description="A simple argument parser",
        epilog="This is where you might put example usage"
    )
    parser.add_argument('-x', '--execute', action="store", required=True,
                        help='Help text for option X')
    parser.add_argument('-y', help='Help for option Y', default=False)
    parser.add_argument('-z', help='Help for option z', type=int)
    print (parser.parse_args())

if __name__=="__main__":
    get_args()
