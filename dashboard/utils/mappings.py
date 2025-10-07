from datetime import date


def transform_data_for_backend(data):
    transformed = data.copy()

    if "date_naissance" in data and isinstance(data["date_naissance"], date):
        transformed["DAYS_BIRTH"] = (transformed["date_naissance"] - date.today()).days
        transformed["date_naissance"] = data["date_naissance"].strftime("%Y-%m-%d")

    return transformed
