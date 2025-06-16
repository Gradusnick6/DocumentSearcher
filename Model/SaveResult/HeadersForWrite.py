from Model.SaveResult.WriterType import WriterType


headers_for_write_dict = {WriterType.WRITE_PATTERN_STRINGS: ["Имя паттерна", "Тип", "Тэг", "Страницы"],
                          WriterType.WRITE_SEARCH_RESULT: ["Имя паттерна", "Тип", "Regex", "Тэг",
                                                           "В этих", "колонках", "и дальше", "–", "позиции"],
                          WriterType.NOT_FOUND: ["Имя паттерна", "Тип", "Regex", "Тэг"]
                          }
