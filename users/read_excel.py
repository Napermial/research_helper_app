from pandas import read_excel
from io import BytesIO
from .models import Factor, Level, Item


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
    lines = []
    for _id, row in read.iterrows():
        lines.append(Line(row['factor'],
                          row['level'],
                          row['stimulus'],
                          row['pre_context'],
                          row['post_context']))
    return lines


def create_item(line):
    item = Item()
    item.item_text = line.stimulus
    item.pre_item_context = line.pre_context
    item.post_item_context = line.post_context
    item.lexicalization = line.lexicalization
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
    levels = []
    for factor in schema:
        db_factor = Factor(name=factor["name"], experiment_id=experiment_id)
        db_factor.save()
        for level in factor["level"]:
            db_level = Level(name=level["name"], factor=db_factor)
            db_level.save()
            levels.append((db_level.pk, db_level.name, db_factor.pk))
    return levels


def handle_file(schema, file):
    file = read_file(file[0])
    return file
