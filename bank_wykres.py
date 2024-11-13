from datetime import datetime

def csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]
        return [line.strip().split(',') for line in lines]
    
def dane(data, typ):

    daty = [row[3] for row in data]
    czas = [row[4] for row in data]

    datetime_objects = [datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S') for date, time in zip(daty, czas)]

    miesiac = datetime.now().month
    rok = datetime.now().year

    if typ == "dzien":
        return [dt.day for dt in datetime_objects if dt.month == miesiac]
    elif typ == "tydzien":
        return [dt.isocalendar()[1] for dt in datetime_objects if dt.year == rok]
    else:
        months_data = [dt.month for dt in datetime_objects]
        last_12_months_data = [month if month >= miesiac or dt.year == rok - 1 else month + 12 for month, dt in zip(months_data, datetime_objects)]
        return last_12_months_data
