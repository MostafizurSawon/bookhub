from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from .models import Book
from transaction.models import Transaction
from transaction.constants import BORROW, RETURN
from review.forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_borrow_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = book.reviews.all()
        
        context["comments"] = reviews
        context["reviews"] = reviews
        
        return context
    
    

class BookReviewView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'give_review.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = book.reviews.all()
        review_form = ReviewForm()
        
        context["comments"] = reviews
        context["review_form"] = review_form
        context["reviews"] = reviews
        
        return context


@login_required
def BorrowBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    request.user.account.borrowed_books.add(book)
    
    if(book.borrow_price > request.user.account.balance):
       return redirect("deposit_money")
    else:
        Transaction.objects.create(user=request.user.account, amount=book.borrow_price, balance_after_transaction=request.user.account.balance - book.borrow_price, transaction_type=BORROW)
        account = request.user.account
        account.balance -= book.borrow_price 

        account.save(
            update_fields=[
                'balance'
            ]
        )
        
        send_borrow_email(request.user, book.borrow_price, f"Successfully Borrowed {book.title} on BookHub", "borrow_email.html")
        return redirect("pborrow")
    

@login_required
def ReturnBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    request.user.account.borrowed_books.remove(book)
    Transaction.objects.create(user=request.user.account, amount=book.borrow_price, balance_after_transaction=request.user.account.balance + book.borrow_price, transaction_type=RETURN)
    
    account = request.user.account
    account.balance += book.borrow_price 
    account.save(
        update_fields=[
            'balance'
        ]
    )
    
    send_borrow_email(request.user, book.borrow_price, f"Successfully Returned {book.title} on BookHub!", "book_return_email.html")
    
    return redirect("pborrow")