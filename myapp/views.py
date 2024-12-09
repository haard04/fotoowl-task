from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, BookRequest, CustomUser
from .serializers import BookSerializer, BookRequestSerializer, UserSerializer
import csv
from django.http import HttpResponse

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    is_librarian = request.data.get('is_librarian', False)

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.create_user(
            username=username, 
            password=password,
            email=email,
            is_librarian=is_librarian
        )
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_librarian': user.is_librarian
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    print(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    print("user",user)
    if user:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@csrf_exempt
def list_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@csrf_exempt
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def get_book_details(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@login_required
def create_book_request(request):
    serializer = BookRequestSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # Check for overlapping requests
        book = serializer.validated_data['book']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        overlapping_requests = BookRequest.objects.filter(
            book=book,
            status='APPROVED',
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        
        if overlapping_requests.exists():
            return Response(
                {'error': 'Book is already borrowed during this period'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save request for current user
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
def list_book_requests(request):
    if request.user.is_librarian:
        # Librarian sees all requests
        book_requests = BookRequest.objects.all()
    else:
        # User sees only their own requests
        book_requests = BookRequest.objects.filter(user=request.user)
    
    serializer = BookRequestSerializer(book_requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def book_request_history(request):
    # Export user's book request history as CSV
    book_requests = BookRequest.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="book_history.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Book Title', 'Start Date', 'End Date', 'Status'])
    
    for req in book_requests:
        writer.writerow([
            req.book.title, 
            req.start_date, 
            req.end_date, 
            req.get_status_display()
        ])
    
    return response

@api_view(['POST'])
@login_required
def approve_book_request(request, request_id):
    # Librarian-only action to approve a book request
    if not request.user.is_librarian:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        book_request = BookRequest.objects.get(id=request_id)
        book_request.status = 'APPROVED'
        book_request.save()
        return Response({'status': 'Request approved'})
    except BookRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@login_required
def deny_book_request(request, request_id):
    # Librarian-only action to deny a book request
    if not request.user.is_librarian:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        book_request = BookRequest.objects.get(id=request_id)
        book_request.status = 'DENIED'
        book_request.save()
        return Response({'status': 'Request denied'})
    except BookRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)