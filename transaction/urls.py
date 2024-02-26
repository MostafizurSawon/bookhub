from django.urls import path
from . import views
 
urlpatterns = [
    path('deposit-money/', views.DepositView.as_view(), name='deposit_money'),
    path('transaction/', views.TransactionView.as_view(), name="transaction"),
    path('profile/', views.BorrowedBooksView.as_view(), name="pborrow"),
]