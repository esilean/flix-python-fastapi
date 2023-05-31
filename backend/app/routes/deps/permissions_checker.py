from fastapi import Depends

from app.configs.errors import Forbidden

from app.routes.deps.get_current_user import get_current_user


class PermissionChecker:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user = Depends(get_current_user)) -> bool:        
        claims = current_user['token']['claims']

        for req_permission in self.required_permissions:
            if req_permission not in claims:
                raise Forbidden(errors={})
        return True