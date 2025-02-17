from enum import Enum
import re
from fuzzywuzzy import fuzz
from typing import Any, List, Optional, Tuple, TypedDict, Union, Dict
from datetime import date, datetime, timezone
from flask import Request
from requests import Response
from dateutil.relativedelta import relativedelta
from helpers.error import Error


class SignzyTaskConstants(Enum):
    GSTIN_DETAILED = "detailedGstinSearch"


class MonthNameEnum(Enum):
    January = "January"
    February = "February"
    March = "March"
    April = "April"
    May = "May"
    June = "June"
    July = "July"
    August = "August"
    September = "September"
    October = "October"
    November = "November"
    December = "December"


MonthNameToValue = {}
MonthNameToValue[MonthNameEnum.January.value] = 10
MonthNameToValue[MonthNameEnum.February.value] = 11
MonthNameToValue[MonthNameEnum.March.value] = 12
MonthNameToValue[MonthNameEnum.April.value] = 1
MonthNameToValue[MonthNameEnum.May.value] = 2
MonthNameToValue[MonthNameEnum.June.value] = 3
MonthNameToValue[MonthNameEnum.July.value] = 4
MonthNameToValue[MonthNameEnum.August.value] = 5
MonthNameToValue[MonthNameEnum.September.value] = 6
MonthNameToValue[MonthNameEnum.October.value] = 7
MonthNameToValue[MonthNameEnum.November.value] = 8
MonthNameToValue[MonthNameEnum.December.value] = 9

MonthValueToName = {}
MonthValueToName[10] = MonthNameEnum.January.value
MonthValueToName[11] = MonthNameEnum.February.value
MonthValueToName[12] = MonthNameEnum.March.value
MonthValueToName[1] = MonthNameEnum.April.value
MonthValueToName[2] = MonthNameEnum.May.value
MonthValueToName[3] = MonthNameEnum.June.value
MonthValueToName[4] = MonthNameEnum.July.value
MonthValueToName[5] = MonthNameEnum.August.value
MonthValueToName[6] = MonthNameEnum.September.value
MonthValueToName[7] = MonthNameEnum.October.value
MonthValueToName[8] = MonthNameEnum.November.value
MonthValueToName[9] = MonthNameEnum.December.value


class StatementPeriod(TypedDict):
    from_date: date
    to_date: date


class AmountWithDate(TypedDict):
    amount: float
    date: date


class MiscUtils:
    DATETIME_ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
    DATE_ISO_FORMAT = "%Y-%m-%d"

    @staticmethod
    def format_msg(msg: str) -> str:
        formatted_msg = ""
        for i, part in enumerate(msg.split("'")):
            if i % 2 == 0:
                formatted_msg += part.lower()
            else:
                formatted_msg += f"'{part}'"
        if len(formatted_msg) > 0:
            formatted_msg = formatted_msg[0].upper() + formatted_msg[1:]
        return formatted_msg


    @staticmethod
    def title_case(s: str) -> str:
        if isinstance(s, str):
            str_arr = s.split(" ")
            for i in range(len(str_arr)):
                if len(str_arr[i]) > 0:
                    str_arr[i] = str_arr[i][0].upper() + str_arr[i][1:].lower()
            return " ".join(str_arr)
        return s

    @staticmethod
    def get_request_body(request: Request):
        try:
            request_body = dict(request.get_json() if request.is_json else {})
            return request_body
        except Exception as error:
            if isinstance(error, Error):
                raise error
            raise Error(msg="invalid request body", status_code=400)

    @staticmethod
    def get_value_from_dictionary(d: dict, key: Union[str, List[str]]) -> Any:
        if d is None:
            return None
        if isinstance(key, str):
            if key in d.keys():
                return d[key]
        elif isinstance(key, list):
            current_dict = d
            count = 0
            while current_dict is not None and count < len(key):
                if isinstance(current_dict, dict) and key[count] in current_dict.keys():
                    current_dict = current_dict[key[count]]
                    count += 1
                else:
                    return None
            return current_dict
        else:
            return None

    @staticmethod
    def get_value_from_dict(
        d: dict,
        keys: Union[str, List[str]],
        default: Any = None,
        none_accepted: bool = False,
        empty_accepted: bool = True,
    ):
        if isinstance(d, dict):
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                if key in d:
                    value = d[key]
                    if value is None and none_accepted == False:
                        raise Error(
                            msg=f"Could not extract '{key}' from dictionary", status_code=400
                        )
                    return (
                        MiscUtils.check_unknown_empty_value(value)
                        if empty_accepted is False
                        else value
                    )
            return default
        else:
            raise Error(msg="Object passed is not a dictionary",
                        status_code=400)
        
    @staticmethod
    def get_nested_value_from_dict(d: dict, keys: list, default: Any = None):
        if not isinstance(d, dict):
            raise Error(msg="Object passed is not a dictionary",
                        status_code=400)

        current_value = d
        for key in keys:
            if isinstance(current_value, dict) and key in current_value:
                current_value = current_value[key]
            else:
                return default

        return current_value

    @staticmethod
    def typecast_string(s: Union[str, Any, None], to_type: type, typecast_function):
        try:
            if s is None:
                return None
            elif isinstance(s, str):
                if len(s) == 0:
                    return s
                return typecast_function(s)
            elif isinstance(s, to_type):
                return s
            else:
                raise Error(
                    msg=f"Cannot typecast from string to {to_type.__name__}",
                    status_code=400,
                )
        except Exception as error:
            if isinstance(error, ValueError):
                raise Error(msg=f"Cannot parse string to {to_type.__name__}")

    @staticmethod
    def value_to_enum(value: Any, enum) -> Optional[Enum]:
        if value is None:
            return None
        try:
            return enum[value]             # previously it was -> enum(value)
        except:
            raise Error(
                msg=f"value '{value}' not found in enum '{enum.__name__}'")

    @staticmethod
    def get_filtered_dict(d: dict, keys: List[str]):
        filtered_d = {}
        for key in d.keys():
            if key in keys:
                filtered_d[key] = d[key]
        return filtered_d

    @staticmethod
    def get_curl(response: Response):
        req = response.request
        command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        method = req.method
        uri = req.url
        data = req.body
        headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
        headers = " -H ".join(headers)
        return command.format(method=method, headers=headers, data=data, uri=uri)

    @staticmethod
    def check_nullability(object: Any, name: str = "object", error_out: bool = True):
        if object is None:
            if error_out is True:
                raise Error(msg=f"{name} has a null value", status_code=404)
            return None

    @staticmethod
    def raise_error_from_call(call: Any) -> Optional[Error]:
        error = None
        if call.info.success == False:
            error = Error(
                msg=call.meta.error_message, status_code=call.info.status_code
            )
            raise error

    @staticmethod
    def sanitise_dict(d: dict, ignore_null: bool = True) -> dict:
        sanitised_d = {}
        # Make dict null free
        for key, value in d.items():
            if not ignore_null or value is not None:
                sanitised_d[key] = value
        return sanitised_d

    @staticmethod
    def merge_nested_dicts(d1: dict, d2: dict, ignore_null: bool = True) -> dict:
        merged_d = d1.copy()
        d2 = MiscUtils.sanitise_dict(d2, ignore_null)
        for d2_key, d2_value in d2.items():
            if (
                d2_key in merged_d.keys()
                and isinstance(merged_d[d2_key], dict)
                and isinstance(d2_value, dict)
            ):
                merged_d[d2_key] = MiscUtils.merge_nested_dicts(
                    merged_d[d2_key], d2_value
                )
            else:
                merged_d[d2_key] = d2_value
        return merged_d

    @staticmethod
    def mask_string(s: str, start_index: int, end_index: int) -> str:
        if not s or not isinstance(s, str) or start_index >= end_index:
            return s
        # Make sure start_index and end_index are within the string's bounds
        start_index = max(start_index, 0)
        end_index = min(end_index, len(s))
        # Generate the masked string
        masked_string = (
            s[:start_index] + "X" * (end_index - start_index) + s[end_index:]
        )
        return masked_string

    @staticmethod
    def date_parser(date_str: str, date_format: str = "%d/%m/%Y") -> Union[date, Any]:
        try:
            date = (
                datetime.strptime(date_str, date_format).date()
                if isinstance(date_str, str)
                else date_str
            )
            return date
        except:
            return date_str

    def parse_date_to_format(
        input_date, input_format: str = "%Y-%m-%d", output_format: str = "%d/%m/%Y"
    ):
        try:
            if input_date:
                date_obj = MiscUtils.date_parser(input_date, input_format)
                formatted_date = MiscUtils.date_string(date_obj, output_format)
                return formatted_date
            else:
                return None
        except ValueError:
            return input_date

    def date_string(d: Optional[date], format: str = "%Y-%m-%d") -> str:
        try:
            formatted_date = d.strftime(format)
            return formatted_date
        except:
            return d

    @staticmethod
    def date_iso_string(date_obj: date):
        if isinstance(date_obj, date):
            return date_obj.isoformat()
        return date_obj

    @staticmethod
    def string_to_date(
        date_str: str, format: Optional[str] = None, error: Optional[bool] = False
    ) -> date:
        format = MiscUtils.DATE_ISO_FORMAT if format is None else format
        date_obj = date_str
        try:
            if isinstance(date_str, str):
                date_obj = datetime.strptime(date_str, format).date()
            elif isinstance(date_str, date):
                date_obj = date_str
            else:
                raise Exception(f"Expected '{date_str}' to be a date string")
        except Exception as err:
            if error is True:
                raise Error(msg=err, status_code=400)
        return date_obj

    @staticmethod
    def date_to_string(
        date_obj: date, format: Optional[str] = None, error: Optional[bool] = False
    ) -> str:
        format = MiscUtils.DATE_ISO_FORMAT if format is None else format
        date_str = date_obj
        try:
            if isinstance(date_obj, date):
                date_str = date_obj.strftime(format)
            else:
                raise Exception(f"Expected '{date_obj}' to be a date object")
        except Exception as err:
            if error is True:
                raise Error(msg=err, status_code=400)
        return date_str

    @staticmethod
    def string_to_datetime(datetime_str: str, format: Optional[str] = None) -> datetime:
        if datetime_str is None:
            return None
        format = MiscUtils.DATETIME_ISO_FORMAT if format is None else format
        try:
            datetime_obj = datetime.strptime(datetime_str, format)
            # Check if the input string contains timezone info as +/-hh:mm
            if len(datetime_str) > len(format) and (
                datetime_str[-6] == "+" or datetime_str[-6] == "-"
            ):
                # Extract the timezone offset from the input string
                tz_offset = datetime_str[-6:]
                hours = int(tz_offset[1:3])
                minutes = int(tz_offset[4:6])
                # Create a timezone object with the extracted offset
                tz = timezone(datetime.timedelta(hours=hours, minutes=minutes))
                # Attach the timezone to the datetime object
                datetime_obj = datetime_obj.replace(tzinfo=tz)
            return datetime_obj
        except Exception as e:
            return datetime_str

    @staticmethod
    def datetime_to_string(datetime_obj: date, format: Optional[str] = None) -> str:
        if datetime_obj is None:
            return None
        format = MiscUtils.DATETIME_ISO_FORMAT if format is None else format
        try:
            if isinstance(datetime_obj, datetime) and datetime_obj.tzinfo is not None:
                # Get the timezone offset in hours and minutes
                offset = datetime_obj.utcoffset()
                hours, remainder = divmod(offset.seconds, 3600)
                minutes = remainder // 60
                sign = "+" if offset >= timezone.utc else "-"
                # Add timezone information in +/-hh:mm format
                format += f"{sign}{hours:02}:{minutes:02}"
            # Format the date object
            date_str = datetime_obj.strftime(format)
            return date_str
        except Exception as e:
            return str(datetime_obj)

    @staticmethod
    def age_from_dob(dob: Optional[date] = None) -> Optional[int]:
        if not isinstance(dob, date):
            return None
        today = date.today()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
        return age

    @staticmethod
    def check_unknown_empty_value(x: Any) -> Any:
        """Check the value of x based on the type and return None if empty else x value"""
        if x is None:
            return None
        elif isinstance(x, list):
            return None if len(x) == 0 else x
        elif isinstance(x, dict):
            return None if len(x.keys()) == 0 else x
        elif isinstance(x, str):
            return None if len(x.strip()) == 0 else x.strip()
        elif isinstance(x, int) or isinstance(x, float):
            return x
        else:
            return x
    @staticmethod  
    def return_null_if_empty(value):
        # Check if the value is None or an empty string
        if value is None or value == "":
            return None
        return value

    @staticmethod
    def preprocess(s: str) -> str:
        """Preprocess the string for better matching."""
        s = s.lower()  # Convert to lowercase
        s = re.sub(r"[^\w\s]", "", s)  # Remove punctuation
        s = " ".join(s.split())  # Remove extra spaces
        return s

    @staticmethod
    def fuzzy(s1: str, s2: str, threshold: float) -> Tuple[float, bool]:
        """Check if two names are matching based on the fuzzy score."""
        s1, s2 = MiscUtils.preprocess(s1), MiscUtils.preprocess(s2)
        score1 = fuzz.ratio(s1, s2)
        score2 = fuzz.partial_ratio(s1, s2)
        score3 = fuzz.token_sort_ratio(s1, s2)
        avg_score = (score1 + score2 + score3) / 3.0
        return avg_score, avg_score > threshold

    @staticmethod
    def pick_non_null(*options: List[Any]) -> Optional[Any]:
        if options is None:
            return None
        for option in options:
            if option is not None:
                return option
        return None

    @staticmethod
    def camel_to_snake(name):
        name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    @staticmethod
    def dict_keys_to_snake_case(data):
        if isinstance(data, list):
            return [MiscUtils.dict_keys_to_snake_case(item) for item in data]
        elif isinstance(data, dict):
            return {
                MiscUtils.camel_to_snake(key): MiscUtils.dict_keys_to_snake_case(value)
                for key, value in data.items()
            }
        else:
            return data

    @staticmethod
    def from_name_split(
        name_split: List[str],
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        first_name = None
        middle_name = None
        last_name = None
        if len(name_split) >= 3:
            first_name = MiscUtils.check_unknown_empty_value(name_split[0])
            middle_name = MiscUtils.check_unknown_empty_value(
                " ".join(name_split[1:-1])
            )
            last_name = MiscUtils.check_unknown_empty_value(name_split[-1])
        elif len(name_split) == 2:
            first_name = MiscUtils.check_unknown_empty_value(name_split[0])
            last_name = MiscUtils.check_unknown_empty_value(name_split[1])
        elif len(name_split) == 1:
            first_name = MiscUtils.check_unknown_empty_value(name_split[0])
        return first_name, middle_name, last_name

    @staticmethod
    def replace_na_with_null(values_dict: dict, na_like_values: List[str]) -> dict:
        na_like_values = [na_like_value.lower()
                          for na_like_value in na_like_values]
        for key, value in values_dict.items():
            if isinstance(value, str) and value.lower() in na_like_values:
                values_dict[key] = None
        return values_dict

    @staticmethod
    def flatten_dict(
        d: Dict[str, Any], separator: Optional[str] = ".", prefix: Optional[str] = ""
    ) -> Dict[str, Any]:
        res = {}
        for key, value in d.items():
            if isinstance(value, dict):
                res.update(
                    MiscUtils.flatten_dict(
                        value, separator, prefix + key + separator)
                )
            else:
                res[prefix + key] = value
        return res

    @staticmethod
    def remove_prefix(s: str, prefix: str) -> str:
        if s.startswith(prefix):
            s = s[len(prefix):]
        return s

    @staticmethod
    def unflatten_dict(
        d: Dict[str, Any], separator: Optional[str] = ".", prefix: Optional[str] = ""
    ) -> Dict[str, Any]:
        res = {}
        for key, value in d.items():
            parts = key.split(separator)
            d = res
            for part in parts[:-1]:
                part = MiscUtils.remove_prefix(part, prefix)
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[MiscUtils.remove_prefix(parts[-1], prefix)] = value
        return res
    
    @staticmethod
    def calculate_months_between_dates(start_date, end_date):
        """
        Calculate the number of months between two dates considering only month and year.
        
        Parameters:
        start_date (datetime): The start date (oldest_loan_date).
        end_date (datetime): The end date (current date).
        
        Returns:
        int: The number of months between start_date and end_date.
        """
        if start_date is None or end_date is None:
            return 0
        # Normalize dates to the first day of their respective months
        normalized_start_date = start_date.replace(day=1)
        normalized_end_date = end_date.replace(day=1)
        if normalized_start_date > normalized_end_date:
            raise Error("start_date cannot be after end_date", 400)
        delta = relativedelta(normalized_end_date, normalized_start_date)
        number_of_months = delta.years * 12 + delta.months
        return number_of_months
    
    @staticmethod
    def extract_generated_file_name(url: str) -> str:
        # Extract the filename from the URL
        generated_file_name = url.split('/')[-1]
        return generated_file_name

    @staticmethod
    def approximate_original_file_name(generated_file_name: str) -> str:
        # Split the filename by underscore
        parts = generated_file_name.split('_')  # Split into maximum 3 parts
        base_name = parts[0] if parts is not None and len(parts) > 0 else ""
        extension = generated_file_name.split('.')[-1] if '.' in generated_file_name else ""
        # Reconstruct the original name with the extension if it exists
        return f"{base_name}.{extension}" if extension else base_name

    @staticmethod
    def original_file_name_from_url(url: str) -> str:
        generated_file_name = MiscUtils.extract_generated_file_name(url)
        original_file_name = MiscUtils.approximate_original_file_name(generated_file_name)
        return original_file_name
    
    def unix_to_date(unix_timestamp):
    # Convert the Unix timestamp to a timezone-aware datetime object in UTC
        if isinstance(unix_timestamp, str):
            unix_timestamp = int(unix_timestamp)
        date_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        # Format the datetime object to 'YYYY-MM-DD' format
        return date_time.strftime('%Y-%m-%d')