from pandas import read_excel
from io import BytesIO


def check_schema(schema, file_schema):
    if schema is file_schema:
        return True
    if len(schema) > len(file_schema):
        print("web schema is larger")


def read_file(input_file):
    read = read_excel(BytesIO(input_file.read()))
    schema = []
    headers = [*read]
    if "factor" in headers and "level" in headers:
        current_factor = ''
        levels = []
        for _id, row in read.sort_values(by=['factor']).iterrows():
            if current_factor == '':
                current_factor = row["factor"]
            if current_factor != row["factor"]:
                schema.append({"factor": current_factor, "levels": levels})
                current_factor = row['factor']
                levels = [{"level": row["level"]}]
                continue
            if _id == len(read) - 1:
                schema.append({"factor": current_factor, "levels": levels})
            levels.append({"level": row["level"]})

    return schema, read


def put_into_db(file):
    pass


def handle_file(schema, file_name, file):
    file_schema, file = read_file(file[0])
    print(check_schema(schema, file_schema))
