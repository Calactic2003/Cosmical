# Create this file as context_processors.py in your app directory

from .models import FollowersCount, Profile
from django.contrib.auth.models import User

def subscription_processor(request):
    """
    Context processor to make subscriptions available across all templates
    """
    context = {'subscriptions': []}
    
    if request.user.is_authenticated:
        # Get list of usernames the user is following
        following_records = FollowersCount.objects.filter(follower=request.user.username)
        
        # Get user profiles for subscriptions
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
        
        context['subscriptions'] = subscriptions
        
    return context