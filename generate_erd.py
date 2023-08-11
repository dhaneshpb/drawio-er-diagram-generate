
from erd.generate import execute
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drawio Diagram Generator",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--db-type", help="Database type - Default postgres", default="postgres")
    parser.add_argument("-a", "--host", help="sql database host", required=True)
    parser.add_argument("-p", "--port", help="sql database port", default="5432")
    parser.add_argument("-d", "--database", help="sql database name", required=True)
    parser.add_argument("-u", "--username", help="sql database username", required=True)
    parser.add_argument("-k", "--password", help="sql database password", required=True)
    parser.add_argument("-o", "--output-path", help="Diagram output file path", default="er_gen.drawio")
    args = parser.parse_args()
    config = vars(args)
    execute(
        config['output_path'],
        config['db_type'],
        config['host'],
        config['port'],
        config['database'],
        config['username'],
        config['password']
    )
