from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class AdminRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self): return self.request.user.is_staff or self.request.user.is_superuser
    def handle_no_permission(self): return super().handle_no_permission()
