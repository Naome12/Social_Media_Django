import pandas as pd
from .models import Post, Comment, Follower, User

# Function to get all posts in a DataFrame
def get_posts_dataframe():
    posts = Post.objects.all().values('id', 'user__username', 'content', 'created_at', 'updated_at')
    df = pd.DataFrame(posts)
    return df

# Function to get all comments in a DataFrame
def get_comments_dataframe():
    comments = Comment.objects.all().values('id', 'post__id', 'user__username', 'content', 'created_at')
    df = pd.DataFrame(comments)
    return df

# Function to get followers information in a DataFrame
def get_followers_dataframe():
    followers = Follower.objects.all().values('follower__username', 'following__username')
    df = pd.DataFrame(followers)
    return df

# Function to get user activity (posts) in a DataFrame
def get_user_activity_dataframe():
    df = get_posts_dataframe()
    user_activity = df.groupby('user__username').size().reset_index(name='post_count')
    return user_activity

# Function to export posts DataFrame to CSV
def export_posts_to_csv():
    df = get_posts_dataframe()
    df.to_csv('posts_report.csv', index=False)

# Function to convert a DataFrame to HTML (for rendering in templates)
def get_posts_as_html():
    df = get_posts_dataframe()
    return df.to_html(classes='table table-striped')


#views.py
# def posts_report(request):
#     posts_html = get_posts_as_html()  # Fetch posts as HTML table
#     return render(request, 'posts_report.html', {'posts_html': posts_html})

# # View to export posts data to CSV
# def export_posts_to_csv_view(request):
#     # Generate CSV response
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=posts_report.csv'
    
#     # Use the utility function to generate the CSV file
#     df = get_posts_dataframe()
#     df.to_csv(path_or_buffer=response, index=False)  # Export without index
    
#     return response

# # Optional: You can create a view to handle the user activity report as well
# def user_activity_report(request):
#     df = get_user_activity_dataframe()
#     user_activity_html = df.to_html(classes='table table-striped')
#     return render(request, 'user_activity_report.html', {'user_activity_html': user_activity_html})