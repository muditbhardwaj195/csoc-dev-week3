from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name='store/book_detail.html'
    context={
        'book':None, # set this to an instance of the required book
        'num_available':None, # set this 1 if any copy of this book is available, otherwise 0
    }
    # START YOUR CODE HERE
    context['book']=Book.objects.get(id=bid)
    #print(context['book'],bid)

    try:
        present = BookCopy.objects.get(book = Book.objects.get(id = bid),status = True)
        #print(present)
        context['num_available']=1
    except:
        #print("HI")
        context['num_available']=0

    
    return render(request,template_name, context=context)


def bookListView(request):
    template_name='store/book_list.html'
    context={
        'books':None, # set here the list of required books upon filtering using the GET parameters
    }
    get_data=request.GET
    # START YOUR CODE HERE

    books = Book.objects.all()
    print(books)

    try:
        temp_title = get_data['title']
        books = books.filter(title = temp_title)
        print(books)
    except:
        pass

    try:
        temp_author = get_data['author']
        books = books.filter(author = temp_author)
    except:
        pass

    try:
        temp_genre = get_data['genre']
        books = books.filter(genre = temp_genre)
    except:
        pass

    
    context['books'] = books
    
    return render(request,template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name='store/loaned_books.html'
    context={
        'books':None,
    }
    '''
    The above key books in dictionary context should contain a list of instances of the 
    bookcopy model. Only those books should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    
    id_user = request.user


    books = BookCopy.objects.filter(borrower = id_user, status = False)

    context['books'] = books;


    return render(request,template_name,context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data={
        'message':None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = None # get the book id from post data

    book_id = request.POST.get("bid")
    print(book_id,"##")

    try:
        temp = BookCopy.objects.get(book = Book.objects.get(id = book_id))
        print(temp)
        if temp.status == True :
            temp.borrow_date = datetime.datetime.now().date();
            temp.borrower = request.user
            temp.status = False
            temp.save()
            print('saved it')
            response_data['message']= 1
        else:
            response_data['message'] = 'failure'
    except:
        response_data['message'] = 'failure'

    #if(response_data['message'] == 1):
        #BookCopy.objects.create(book = Book.objects.get(id = book_id), borrow_date = datetime.datetime.now().date(), borrower = request.user)

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):

    response_data={
        'message':None,
    }

    book_id = request.POST.get("bid")
    print(book_id)

    try:
        temp = BookCopy.objects.get(book = Book.objects.get(id = book_id))
        BookCopy.objects.get(book = Book.objects.get(id = book_id)).delete()
        response_data['message']=1
    except:
        response_data['message']='failure'

    return JsonResponse(response_data)




@csrf_exempt
@login_required
def rateBookView(request,bid):
    template_name='store/rate.html'
    #bid = request.POST.get("bid")
    context={
        'book':None, # set this to an instance of the required book
        'num_available':None, # set this 1 if any copy of this book is available, otherwise 0
    }
    # START YOUR CODE HERE
    context['book']=Book.objects.get(id=bid)
    context['num_available']=0
    print("hello",bid,context['book'],context['num_available'])
    #print(context['book'],bid)
    
    return render(request,template_name, context=context)


@csrf_exempt
@login_required
def ratingChangeBookView(request):
    response_data={
        'message':None,
    }
    print('calledit')
    book_id = request.POST.get("bid")
    
    rating_change = request.POST.get("rating")
    print(int(rating_change))
    print(book_id,rating_change)
    book = Book.objects.get(id =book_id)
    current_rating = book.rating
    current_ratedby = book.rated_by
    current_ratedby = current_ratedby + 1
    current_rating = current_rating + int(rating_change)
    current_rating = int(current_rating/current_ratedby)

    print(current_rating,current_ratedby)

    book.rating = current_rating
    book.rated_by = current_ratedby
    book.save()

    temp = BookCopy.objects.get(book = Book.objects.get(id = book_id))
    temp.status = True
    temp.save()
    

    response_data['message']=1

    return JsonResponse(response_data)

def loginTemplate(request):
    template_name = "authentication/login.html"

    return render(request,template_name,{})

def registerTemplate(request):
    template_name = "authentication/register.html"
    return render(request, template_name, {})
