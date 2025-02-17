from functools import wraps
from typing import List
import json
from flask import request
from helpers.body_field_validation import BodyFieldValidation
from helpers.error import Error
from utils.logger import logger
from utils.misc import MiscUtils
from utils.response import ResponseUtils


def request_body_validators(fields: List[BodyFieldValidation], allow_all: bool = False, allow_null: bool = False):
    def _request_body_validator(f):
        @wraps(f)
        def __request_body_validator(*args, **kwargs):
            try:
                request_body = {
                    **request.get_json()} if request.is_json else {}
                validated_request_body = {}
                for field in fields:
                    value = None
                    key_is_present = field.name in request_body.keys()
                    if key_is_present is False or (key_is_present is True and MiscUtils.check_unknown_empty_value(request_body.get(field.name)) == None):
                        if field.default is not None:
                            value = field.default() if callable(field.default) else field.default
                    else:
                        value = request_body.get(field.name, None)
                        request_body.pop(field.name)
                    if field.required == True and value is None:
                        raise Error(
                            msg=f"key '{field.name}' is required in request body", status_code=400)
                    if value is not None:
                        if field.blank_allowed == False and field.value_type is str and str(value).strip() == "":
                            raise Error(
                                msg=f"key '{field.name}' is blank", status_code=400)
                        if field.parser_fn is not None:
                            try:
                                value = field.parser_fn(value)
                            except Exception as error:
                                raise Error(
                                    msg=f"'{field.name}' is not a valid '{field.value_type.__name__}'")
                        if field.validation_fn is not None:
                            try:
                                field.validation_fn(value)
                            except Exception as error:
                                raise error
                        # Type check for List[str]
                        if hasattr(field.value_type, '__origin__') and field.value_type.__origin__ is list:
                            if not isinstance(value, list):
                                raise Error(f"Expected key '{field.name}' to be of type '{field.value_type}' in request body", 400)
                            item_type = field.value_type.__args__[0]
                            if not all(isinstance(item, item_type) for item in value):
                                raise Error(f"Expected all items in '{field.name}' to be of type '{item_type.__name__}'", 400)
                        elif type(value) != field.value_type:
                            raise Error(
                                msg=f"Expected key '{field.name}' to be of type '{field.value_type}' in request body", status_code=400)
                    if field.new_name is None:
                        validated_request_body[field.name] = value
                    else:
                        validated_request_body[field.new_name] = value
                if allow_all is True:
                    validated_request_body.update(request_body)
                validated_request_body = MiscUtils.sanitise_dict(
                    validated_request_body, not allow_null)
                logger.info(
                    f"VALIDATED REQUEST BODY: {validated_request_body}")
                return f(validated_request_body,fields,*args, **kwargs)
            except Exception as error:
                return ResponseUtils.get_error_response(error)
        return __request_body_validator
    return _request_body_validator


def request_form_validators(fields: List[BodyFieldValidation], allow_all: bool = False):
    def _request_form_validator(f):
        @wraps(f)
        def __request_form_validator(*args, **kwargs):
            try:
                request_body = request.form.to_dict()
                validated_request_body = {}
                for field in fields:
                    value = None
                    key_is_present = field.name in request_body.keys()
                    if key_is_present is False or (key_is_present is True and MiscUtils.check_unknown_empty_value(request_body.get(field.name)) == None):
                        if field.default is not None:
                            value = field.default() if callable(field.default) else field.default
                    else:
                        value = request_body.get(field.name, None)
                        request_body.pop(field.name)
                    if field.required == True and value is None:
                        raise Error(
                            msg=f"key '{field.name}' is required in request body", status_code=400)
                    if value is not None:
                        if field.blank_allowed == False and field.value_type is str and str(value).strip() == "":
                            raise Error(
                                msg=f"key '{field.name}' is blank", status_code=400)
                        if field.parser_fn is not None:
                            try:
                                value = field.parser_fn(value)
                            except Exception as error:
                                raise Error(
                                    msg=f"'{field.name}' is not a valid {field.value_type}")
                        if field.validation_fn is not None:
                            try:
                                field.validation_fn(value)
                            except Exception as error:
                                raise error
                        if type(value) != field.value_type:
                            raise Error(
                                msg=f"Expected key '{field.name}' to be of type '{field.value_type}' in request body", status_code=400)
                    if field.new_name is None:
                        validated_request_body[field.name] = value
                    else:
                        validated_request_body[field.new_name] = value
                    if field.new_name is None:
                        validated_request_body[field.name] = value
                    else:
                        validated_request_body[field.new_name] = value
                if allow_all is True:
                    validated_request_body.update(request_body)
                logger.info(
                    f"VALIDATED REQUEST BODY: {validated_request_body}")
                return f(validated_request_body, *args, **kwargs)
            except Exception as error:
                return ResponseUtils.get_error_response(error)
        return __request_form_validator
    return _request_form_validator
