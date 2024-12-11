from guardian.shortcuts import assign_perm
from .models import User, Role

# user_role = Role.objects.get(name='user')
# users_with_user_role = User.objects.filter(roles=user_role)

# for user in users_with_user_role:
#     assign_perm('profiles.view_user', user)

# nickname = 'Dimatron'
# user = User.objects.get(nickname=nickname)
# assign_perm('profiles.view_user', user)