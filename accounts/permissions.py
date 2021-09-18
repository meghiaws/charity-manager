from rest_framework.permissions import IsAuthenticated, BasePermission
from charities.models import Benefactor, Charity


class IsBenefactor(BasePermission):
    def has_permission(self, request, view):
        try:
            benefactor = Benefactor.objects.get(user=request.user)
        except Benefactor.DoesNotExist:
            return False
            
        return True


class IsCharityOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            charity = Charity.objects.get(user=request.user)
        except Charity.DoesNotExist:
            return False

        return True
