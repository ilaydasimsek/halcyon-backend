from django.contrib import admin

from users.models import User, PasswordResetVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(PasswordResetVerification)
class PasswordResetVerificationAdmin(admin.ModelAdmin):
    pass

