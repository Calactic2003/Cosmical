from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import ThreadForm, MessageForm
from .models import Profile, Post, LikePost, FollowersCount, Post, SavedPost, ReportedPost, ThreadModel, MessageModel, Notification
from itertools import chain
from django.shortcuts import get_object_or_404
import random
# Create your views here.

@login_required(login_url='login')
def index(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    # Get list of usernames the user is following
    following_records = FollowersCount.objects.filter(follower=user.username)
    user_following_list = [f.user for f in following_records]
    
    # Create a list of followed usernames (for the recommended section UI)
    followed_users = user_following_list

    # User suggestion logic - MOVED BEFORE RETURN
    all_users = User.objects.all()
    user_following_all = []

    for followed_username in user_following_list:
        try:
            user_list = User.objects.get(username=followed_username)
            user_following_all.append(user_list)
        except User.DoesNotExist:
            continue

    # Create suggestions list excluding users already followed and current user
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if x not in list(current_user)]
    random.shuffle(final_suggestions_list)

    # Get profiles for suggested users
    username_profile = []
    username_profile_list = []  # Fixed variable name (was username_profile_List)

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)  # Fixed field name (was is_user)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    # Get user profiles for subscriptions (showing in the sidebar)
    subscriptions = []
    for followed_username in user_following_list:
        try:
            followed_user = User.objects.get(username=followed_username)
            followed_profile = Profile.objects.get(user=followed_user)
            subscriptions.append({
                'username': followed_username,
                'profile_img': followed_profile.profileimg.url
            })
        except (User.DoesNotExist, Profile.DoesNotExist):
            continue

    # Include the current user in the feed if not already followed
    if user.username not in user_following_list:
        user_following_list.append(user.username)

    # Get posts for each followed user
    feed = [Post.objects.filter(user=username) for username in user_following_list]
    feed_list = list(chain(*feed))

    # Sort by creation time (newest first), if 'created_at' exists
    try:
        feed_list.sort(key=lambda post: post.created_at, reverse=True)
    except AttributeError:
        pass  # created_at might not exist in some edge cases

    return render(request, 'index.html', {
        'user_profile': user_profile,
        'posts': feed_list,
        'subscriptions': subscriptions,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4],
        'followed_users': followed_users  # Pass the list of followed users to the template
    })

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    # Get subscriptions for side menu
    following_records = FollowersCount.objects.filter(follower=request.user.username)
    subscriptions = []
    for record in following_records:
        try:
            followed_user = User.objects.get(username=record.user)
            followed_profile = Profile.objects.get(user=followed_user)
            subscriptions.append({
                'username': record.user,
                'profile_img': followed_profile.profileimg.url
            })
        except (User.DoesNotExist, Profile.DoesNotExist):
            continue

    if request.method == 'POST':
        # Check for profile picture upload
        if request.FILES.get('profile_pic') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('profile_pic')

        # Check for profile banner upload
        if request.FILES.get('banner_image') == None:
            banimage = user_profile.bannerimg
        else:
            banimage = request.FILES.get('banner_image')
        
        
        # Get form fields
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')
        
        # Update profile
        user_profile.profileimg = image
        user_profile.bannerimg = banimage
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
        # Add success message
        messages.success(request, 'Your settings have been saved successfully!')
        return redirect('settings')

    return render(request, 'settings.html', {
        'user_profile': user_profile,
        'subscriptions': subscriptions
    })

@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    # Get subscriptions for side menu
    following_records = FollowersCount.objects.filter(follower=request.user.username)
    subscriptions = []
    for record in following_records:
        try:
            followed_user = User.objects.get(username=record.user)
            followed_profile = Profile.objects.get(user=followed_user)
            subscriptions.append({
                'username': record.user,
                'profile_img': followed_profile.profileimg.url
            })
        except (User.DoesNotExist, Profile.DoesNotExist):
            continue
    
    # Initialize username_profile_list as empty
    username_profile_list = []
            
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    
    # Create a single context dictionary with all variables
    context = {
        'user_profile': user_profile,
        'username_profile_list': username_profile_list,
        'subscriptions': subscriptions
    }

    return render(request, 'search.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']  
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken!')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login) 
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not matching!')
            return redirect('register')
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Incorrect details')
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    return HttpResponse('<h1>Upload View</h1>')

@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')
    
@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    # Get only posts with images for the media tab
    user_media_posts = Post.objects.filter(user=pk, image__isnull=False).exclude(image='')
    
    # Get liked posts for this user to show liked status
    liked_post_ids = []
    if request.user.is_authenticated:
        liked_posts = LikePost.objects.filter(username=request.user.username)
        liked_post_ids = [post.post_id for post in liked_posts]

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unsubscribe'
    else:
        button_text = 'Subscribe'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    # Get subscriptions for side menu
    following_records = FollowersCount.objects.filter(follower=request.user.username)
    subscriptions = []
    for record in following_records:
        try:
            followed_user = User.objects.get(username=record.user)
            followed_profile = Profile.objects.get(user=followed_user)
            subscriptions.append({
                'username': record.user,
                'profile_img': followed_profile.profileimg.url
            })
        except (User.DoesNotExist, Profile.DoesNotExist):
            continue

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_media_posts': user_media_posts,  # Add media posts to context
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'subscriptions': subscriptions,
        'liked_posts': liked_post_ids,  # Add liked posts to context
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        # Get the redirect_url parameter if available, default to profile
        redirect_url = request.POST.get('redirect_url', '/profile/'+user)

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect(redirect_url)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect(redirect_url)
    else:
        return redirect('/')
    
@login_required
def delete_post(request, post_id):
    """Delete a post if the current user is the owner"""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user is the owner of the post
    if request.user.username == post.user:
        # Delete the post
        post.delete()
        return redirect('index')  # Redirect to the homepage or another appropriate page
    else:
        # If not the owner, redirect with an error message
        # You could use Django messages framework here for a better UX
        return redirect('index')

@login_required
def edit_post(request, post_id):
    """Edit a post if the current user is the owner"""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user is the owner of the post
    if request.user.username != post.user:
        return redirect('index')  # Not the owner, redirect
    
    if request.method == 'POST':
        # Update the post with the submitted data
        post.caption = request.POST.get('caption')
        
        # If an image is included in the request, update it
        if 'image_upload' in request.FILES:
            post.image = request.FILES['image_upload']
        
        post.save()
        return redirect('index')  # Redirect after successful edit
    
    # For GET requests, render the edit form
    return render(request, 'edit_post.html', {'post': post})

@login_required
def save_post(request, post_id):
    """Save a post for the current user"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        # Check if the post is already saved
        saved, created = SavedPost.objects.get_or_create(
            user=request.user,
            post_id=str(post_id)
        )
        
        # If the post was already saved, this means the user wants to unsave it
        if not created:
            saved.delete()
            return JsonResponse({'success': True, 'message': 'Post unsaved'})
        
        return JsonResponse({'success': True, 'message': 'Post saved successfully'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def report_post(request, post_id):
    """Report a post"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        details = request.POST.get('details', '')
        
        # Create a new report
        report = ReportedPost.objects.create(
            reporter=request.user,
            post_id=str(post_id),
            reason=reason,
            details=details
        )
        
        return redirect('index')  # Redirect after successful report
    
    # For GET requests, render the report form
    return render(request, 'report_post.html', {'post': post})

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'inbox.html', context)
    
class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'create_thread.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            # In CreateThread view:
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            
            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            "form": form,
            'message_list': message_list
        }

        return render(request, 'thread.html', context)
    
class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('body')
        )

        message.save()

        notification = Notification.objects.create(
            notification_type=1,
            from_user=request.user,
            to_user=receiver,
            thread=thread
        )
        return redirect('thread', pk=pk)