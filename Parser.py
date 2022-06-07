
import pandas 
import DataBase
import json

def get_timetable():
    a=pandas.read_excel(u"D:\Documents\VS_Code\Python\EducationBot\Raspisanie_zanyatiy\П_Бак.xls",)
    dicttmtble = a.head(165).to_dict(orient="records")
    return dicttmtble

def destroy_nan(dicttmtble=list,name=str,index=int): #recursion search last "День" or "Время" and add instead of "nan"
    
    if str(dicttmtble[index][name]) == "nan" :
        dicttmtble[index][name] = destroy_nan(dicttmtble,name,index-1)
        return dicttmtble[index][name]
    else:
        return dicttmtble[index][name]
        
def sort_timetable(dicttmtble=list):
    for i in range(0,len(dicttmtble)):
        if i == len(dicttmtble):
            break
        if "{'День': nan, 'Время': nan, 'П-11': nan, 'П-12': nan, 'П-13': nan, 'П-21': nan, 'П-22': nan, 'П-23': nan, 'П-31': nan, 'П-32': nan, 'П-33': nan, 'П-41': nan, 'П-42': nan, 'П-43': nan}" ==  str(dicttmtble[i]):
            dicttmtble.remove(dicttmtble[i])
        else:
            #print(dicttmtble[i])
            if str(dicttmtble[i]["День"]) == "nan":
                dicttmtble[i]["День"] = destroy_nan(dicttmtble,"День",i)
            if str(dicttmtble[i]["Время"]) == "nan":
                dicttmtble[i]["Время"] = destroy_nan(dicttmtble,"Время",i)
           
            
sort_timetable(get_timetable())
print("Я работаю")

