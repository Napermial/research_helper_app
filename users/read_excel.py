from pandas import read_excel
from io import BytesIO
from .models import Factor, Level, Item


def check_schema(schema, file_schema):
    print(file_schema)
    # if schema == file_schema:
    #     return True
    # if len(schema) > len(file_schema):
    #     print("web schema is larger")


class Line:
    def __init__(self, factor, level, stimulus, pre_context, post_context):
        self.factor = factor
        self.level = level
        self.stimulus = stimulus
        self.pre_context = pre_context
        self.post_context = post_context

    def __str__(self):
        return self.stimulus


def read_file(input_file):
    read = read_excel(BytesIO(input_file.read()))
    schema = []
    lines = []
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

        for _id, row in read.iterrows():
            lines.append(Line(row['factor'],
                              row['level'],
                              row['stimulus'],
                              row['pre_context'],
                              row['post_context']))
    return schema, lines


def create_item(line, experiment):
    item = Item()
    item.level = Level.objects.filter(name=line.level).first()
    item.item_text = line.stimulus
    item.pre_item_context = line.pre_context
    item.post_item_context = line.post_context
    item.experiment = experiment
    print(item)
    item.save()


def put_into_db(file, schema, experiment):
    for line in file:
        if Factor.objects.filter(name=line.factor):
            if Level.objects.filter(name=line.level):
                create_item(line, experiment)
        else:
            factor = Factor(name=line.factor)
            factor.save()
            level = Level(name=line.level, factor=factor)
            level.save()
            create_item(line, experiment)


def insert_factors(schema, experiment_id):
    for factor in schema:
        db_factor = Factor(name=factor["name"])
        db_factor.save()
        for level in factor["level"]:
            Level(name=level["name"], factor=db_factor).save()


def handle_file(schema, file):
    file_schema, file = read_file(file[0])
    if check_schema(schema, file_schema):
        pass
    return schema, file
