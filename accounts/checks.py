from django.core.checks import Error, register
from django.db.models import Model

from .models import BaseProfile


@register("models")
def check_base_profile_subclasses(app_configs, **kwargs):
    """
    Checks that all concrete subclasses of BaseProfile define a 'user' field.
    """
    errors = []
    # Ensure models are fully loaded before running the check
    if app_configs is None:
        from django.apps import apps

        app_configs = apps.get_app_configs()

    # Find all models that inherit from BaseProfile
    profile_models = [
        cls
        for cls in apps.get_models()
        if issubclass(cls, BaseProfile) and not cls._meta.abstract
    ]

    for model in profile_models:
        try:
            # This will raise an exception if the field does not exist
            model._meta.get_field("user")
        except Exception:
            errors.append(
                Error(
                    f"The model '{model.__name__}' must define a 'user' field.",
                    hint=f"Add a OneToOneField or ForeignKey named 'user' to {model.__name__}.",
                    obj=model,
                    id="accounts.E001",
                )
            )
    return errors
