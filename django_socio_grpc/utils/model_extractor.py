def get_app_list():
    """
    Get list of Django application as List
    """
    from django.apps import apps

    dict_app = {}

    for app in apps.get_app_configs():
        dict_app[app.name] = app.verbose_name

    return dict_app


def get_model(current_model_name):
    """
    Get Model from name
    """
    from django.apps import apps
    from django.contrib.contenttypes.models import ContentType

    current_model = None

    if current_model_name:

        #  ----------------------------------------------------------
        #  ---  search if this model exist on Django content type ---
        #  ----------------------------------------------------------
        current_model = ContentType.objects.filter(model=current_model_name)

        # -------------------------------
        # ---  This Model is valid    ---
        # -------------------------------
        if current_model:
            app_label = current_model[0].app_label
            current_model = apps.get_model(app_label=app_label, model_name=current_model_name)
    return current_model


def get_model_column(model_object):
    """
    extract Column List from a Data Model
    """
    array_col = []

    colList = model_object._meta.get_fields(
        include_parents=False
    )  # ---- get column list of the foreignkey Data Model ----
    for each_col in colList:
        dict_col_info = extract_col_data(each_col)
        array_col.append(dict_col_info)

    return array_col


def extract_col_data(each_col):
    """
    extract main  characterostic of each column
    """

    dict_col = {}
    name = each_col.name
    type_col = each_col.get_internal_type()

    # --------------------------------------------
    # ----  extractcolumn lenght if available  ---
    # --------------------------------------------
    try:
        length = each_col.max_length
        if not length:
            length = ""
    except Exception:
        length = ""

    # --------------------------------------------
    # ----  extract verbose Name if available  ---
    # --------------------------------------------
    try:
        verbose_label = each_col.verbose_name
    except Exception:
        verbose_label = ""

    # ----------------------------------------
    #  ---- store characteristic of column ---
    # ----------------------------------------
    dict_col["column"] = each_col
    dict_col["label"] = verbose_label
    dict_col["name"] = name
    dict_col["length"] = length
    dict_col["type"] = type_col

    return dict_col
