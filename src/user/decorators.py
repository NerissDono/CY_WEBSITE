from django.core.exceptions import PermissionDenied

def xp_level_required(required_level):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_level = request.user.xp_level
            levels = ['simple', 'intermediate', 'complex', 'admin']  # Ajout de "intermediate"
            if levels.index(user_level) >= levels.index(required_level):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
