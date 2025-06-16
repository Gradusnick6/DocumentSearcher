from datetime import datetime


class TimeHandler:
    @staticmethod
    def get_str_by_time(time):
        """
        :param time: Time
        :return: str чч:мм:сс
        """
        try:
            time_str = str(time)
            time_without_milli_str = time_str.split('.')[0]
            return time_without_milli_str
        except Exception as ex:
            raise ex

    @staticmethod
    def get_cur_time_str():
        """
        :return: str чч:мм:сс
        """
        try:
            return TimeHandler.get_str_by_time(datetime.now())
        except Exception as ex:
            raise ex

    @staticmethod
    def get_cur_datetime_str():
        """
        :return: str дд:мм:гг чч:мм:сс
        """
        try:
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%d:%m:%y %H:%M:%S')
            return formatted_datetime
        except Exception as ex:
            raise ex
