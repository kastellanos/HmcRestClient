import pandas as pd

class ExcelUtil(object):
    def __init__(self) :
        self.sheets = []
        self.file_path=None
        self.file_name=None
    def add(self, sheet_index,sheet_column,sheet_data, sheet_name ):
        self.sheets.append( (pd.DataFrame(sheet_data,sheet_index,columns=sheet_column),sheet_name))
    def writeExcel(self, file_path="/tmp/", file_name="default.xlsx"):
        self.file_name=file_name
        self.file_path=file_path
        if len(self.sheets)>0:
            writer = pd.ExcelWriter(file_path+file_name,engine="xlsxwriter")
            for df,name in self.sheets:
                print(name)
                df.to_excel(writer,name)
            writer.save()

        else:
            print( "No data to write")