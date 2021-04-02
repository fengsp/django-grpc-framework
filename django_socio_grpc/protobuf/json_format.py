from google.protobuf.json_format import MessageToDict, ParseDict


def message_to_dict(message, **kwargs):
    kwargs.setdefault("including_default_value_fields", True)
    kwargs.setdefault("preserving_proto_field_name", True)
    return MessageToDict(message, **kwargs)


def parse_dict(js_dict, message, **kwargs):
    kwargs.setdefault("ignore_unknown_fields", True)
    return ParseDict(js_dict, message, **kwargs)
