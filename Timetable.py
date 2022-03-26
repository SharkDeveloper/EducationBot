import calendar
import DataBase
import pandas as pd

class week:
    num_week = 0
    group =  "П-11"  # DataBase.get("group")


current_week = week

def get_timetable():
    a=pd.read_excel(u"D:\Documents\VS_Code\Python\EducationBot\Raspisanie_zanyatiy\П_Бак.xls",index_col="День")
    print(a[['Время', 'П-11']].head(165))

# 1 вмместо П-11 передавать переменную ,спросив ее у пользователя
# 2 сделать привязку расписания к дате 
# 3 понять как рабоатет числитель делтель в числителии и делителе

