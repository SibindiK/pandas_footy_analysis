import openpyxl
import pandas as pd

class MyExcelFile():
    def __init__(self, path:str):
        self.path = path
        self.df = pd.DataFrame()
    
    def load_df_from_excel_file(self):
        self.df = pd.read_excel(self.path)

    def write_df_to_excel_file(self, df:pd.DataFrame):
        with pd.ExcelWriter(self.path, mode="a", engine="openpyxl", 
            if_sheet_exists="replace", date_format="DD-MM-YYYY") as writer:
            df.to_excel(writer, sheet_name="DF1")
            writer.save()


def main():
    excelfile = MyExcelFile("Hello")
    excelfile.write_df_to_excel_file()

if __name__ == "__main__":
    main()