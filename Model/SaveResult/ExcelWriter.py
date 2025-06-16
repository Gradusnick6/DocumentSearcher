from Model.SaveResult.ExcelHandler import ExcelHandler
import ViewModel


class ExcelWriter:
    def write(self, file_path, data):
        """
        :param file_path: str
        :param data: dict<list<list<str>>>
        :return: None
        """
        try:
            excel = ExcelHandler(file_path)
            for key, value in data.items():
                self._write_to_sheet(excel, key, value)
                ViewModel.multi_progress_bar.add_progress()

            self._format_file(excel)
            ViewModel.multi_progress_bar.add_progress()
        except Exception as ex:
            raise ex

    def _write_to_sheet(self, excel, sheet_name, data):
        """
        :param excel: ExcelHandler
        :param sheet_name: str
        :param data: list<list<str/float/int>>
        :return: None
        """
        try:
            sheet = excel.create_sheet(sheet_name)
            for row_index, row_data in enumerate(data, start=1):
                for col_index, cell_value in enumerate(row_data, start=1):
                    sheet.cell(row=row_index, column=col_index, value=cell_value)
        except Exception as ex:
            raise ex

    def _format_file(self, excel):
        """
        :param excel: ExcelHandler
        """
        default_sheet_name = "Sheet"
        excel.delete_sheet(default_sheet_name)
        excel.set_align()
        excel.format_columns()
