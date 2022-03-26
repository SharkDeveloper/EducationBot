from base64 import encode
from multiprocessing.sharedctypes import Value
import pandas 
import DataBase
import json

def get_timetable(group):
    a=pandas.read_excel(u"D:\Documents\VS_Code\Python\EducationBot\Raspisanie_zanyatiy\П_Бак.xls",index_col="День")
    print(a[['Время', group]].head(165))
    DataBase.timetables.insert(a)
    
#get_timetable("П-11")

def test():
    a=pandas.read_excel(u"D:\Documents\VS_Code\Python\EducationBot\Raspisanie_zanyatiy\П_Бак.xls")
    
    dicttmtble = a[[ "День","Время",'П-11']].head(165).to_dict(orient="records")
    
    print(dicttmtble)
    
    
    
    

test()