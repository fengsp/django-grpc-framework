def get_model_pk(model):
    opts = model._meta.concrete_model._meta
    pk = opts.pk
    rel = pk.remote_field

    while rel and rel.parent_link:
        # If model is a child via multi-table inheritance, use parent's pk.
        pk = pk.remote_field.model._meta.pk
        rel = pk.remote_field

    return pk