class Validator:
    REQUIRED = {
        "title": str,
        "module": str,
        "description": str,
        "students": int,
        "is_active": bool,
    }

    def is_valid(**data) -> dict | bool:
        verify_keys = Validator.verify_keys(**data)
        if verify_keys[0] is False:
            return verify_keys

        verify_values = Validator.verify_values(**data)
        if verify_values[0] is False:
            return verify_values

        return verify_values

    def verify_keys(**data) -> dict:
        result = [True, data.copy()]
        for valid_key in Validator.REQUIRED.keys():
            if valid_key not in data.keys():
                result[1][valid_key] = "missing key"
                result[0] = False
        return result

    def verify_values(**data) -> dict | bool:
        result = [True, data.copy()]

        for valid_key, expected_type in Validator.REQUIRED.items():
            if type(data[valid_key]) is not expected_type:
                result[1][valid_key] = f"must be a {expected_type.__name__}"
                result[0] = False
        return result
