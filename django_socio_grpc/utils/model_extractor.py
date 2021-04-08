def getModelChoice(arrValue, application="", mode=""):
    """
    Convert array to Model Choices List
    """
    from collections import defaultdict

    ctrValue = 0
    returnList = defaultdict(list)

    for value in arrValue:
        if not mode:
            returnBlock = (value, arrValue[value])
        else:
            returnBlock = (value, value)
        returnList[application].append(returnBlock)
        ctrValue += 1

    if ctrValue > 0:
        return returnList.get(application)
    else:
        return returnList


def getAppList():
    """
    Get list of Django application as List
    """
    from django.apps import apps

    dictApp = {}

    for app in apps.get_app_configs():
        dictApp[app.name] = app.verbose_name

    return dictApp


def getModelList(appName=""):
    """
    Get list of Django Data Model List
    """
    from django.apps import apps

    dicModel = {}

    if not appName:
        for app in apps.get_app_configs():
            for model in app.get_models():
                modelName = model.__name__
                dicModel[modelName] = app.name
    else:
        appTables = apps.get_app_config(appName)
        if appTables:
            for model in appTables.models:
                modelName = model
                dicModel[modelName] = appName

    dicModel = getModelChoice(dicModel, mode="single")
    return dicModel


def getModel(currentModelName):
    """
    Get Model from name
    """
    from django.apps import apps
    from django.contrib.contenttypes.models import ContentType

    currentModel = None

    if currentModelName:

        #  ----------------------------------------------------------
        #  ---  search if this model exist on Django content type ---
        #  ----------------------------------------------------------
        currentModel = ContentType.objects.filter(model=currentModelName)

        # -------------------------------
        # ---  This Model is valid    ---
        # -------------------------------
        if currentModel:
            app_label = currentModel[0].app_label
            currentModel = apps.get_model(app_label=app_label, model_name=currentModelName)
    return currentModel


def getModelColumn(modelObject):
    """
    extract Column List from a Data Model
    """
    arrayCol = []

    colList = modelObject._meta.get_fields(
        include_parents=False
    )  # ---- get column list of the foreignkey Data Model ----
    for eachCol in colList:
        dicColInfo = extractColData(eachCol)
        arrayCol.append(dicColInfo)

    return arrayCol


def extractColData(eachCol):
    """
    extract main  characterostic of each column
    """

    dicCol = {}
    name = eachCol.name
    typeCol = eachCol.get_internal_type()

    # --------------------------------------------
    # ----  extractcolumn lenght if available  ---
    # --------------------------------------------
    try:
        length = eachCol.max_length
        if not length:
            length = ""
    except Exception:
        length = ""

    # --------------------------------------------
    # ----  extract verbose Name if available  ---
    # --------------------------------------------
    try:
        verboseLabel = eachCol.verbose_name
    except Exception:
        verboseLabel = ""

    # ----------------------------------------
    #  ---- store characteristic of column ---
    # ----------------------------------------
    dicCol["column"] = eachCol
    dicCol["label"] = verboseLabel
    dicCol["name"] = name
    dicCol["length"] = length
    dicCol["type"] = typeCol

    return dicCol
