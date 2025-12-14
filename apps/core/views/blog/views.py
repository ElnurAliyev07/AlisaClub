from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from apps.blog.models import Blog, BlogCategory, SidebarGallery, BlogPageSettings, Event


def blog(request):
    """Blog list"""
    # Get active blogs
    blog_list = Blog.objects.filter(is_active=True).select_related('category')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        blog_list = blog_list.filter(category__slug=category_slug)
    
    # Search
    search_query = request.GET.get('q')
    if search_query:
        blog_list = blog_list.filter(title__icontains=search_query) | blog_list.filter(short_content__icontains=search_query)
    
    # Pagination
    paginator = Paginator(blog_list, 5)  # 5 blogs per page
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    
    # Sidebar data
    categories = BlogCategory.objects.filter(is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True)[:3]
    featured_blogs = Blog.objects.filter(is_active=True, is_featured=True)[:3]
    sidebar_gallery = SidebarGallery.objects.filter(is_active=True)[:6]
    upcoming_events = Event.objects.filter(is_active=True, event_date__gte=timezone.now()).order_by('event_date')[:3]
    
    # Page settings
    page_settings = BlogPageSettings.objects.filter(is_active=True).first()
    
    context = {
        'blogs': blogs,
        'categories': categories,
        'recent_blogs': recent_blogs,
        'featured_blogs': featured_blogs,
        'sidebar_gallery': sidebar_gallery,
        'upcoming_events': upcoming_events,
        'search_query': search_query,
        'page_settings': page_settings,
    }
    
    return render(request, 'pages/blog/blog.html', context)


def blog_detail(request, slug):
    """Blog detail"""
    blog = get_object_or_404(Blog, slug=slug, is_active=True)
    
    # Previous and next blogs
    previous_blog = blog.get_previous_blog()
    next_blog = blog.get_next_blog()
    
    # Sidebar data
    categories = BlogCategory.objects.filter(is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True).exclude(id=blog.id)[:3]
    featured_blogs = Blog.objects.filter(is_active=True, is_featured=True).exclude(id=blog.id)[:3]
    sidebar_gallery = SidebarGallery.objects.filter(is_active=True)[:6]
    upcoming_events = Event.objects.filter(is_active=True, event_date__gte=timezone.now()).order_by('event_date')[:3]
    
    # Page settings
    page_settings = BlogPageSettings.objects.filter(is_active=True).first()
    
    context = {
        'blog': blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
        'categories': categories,
        'recent_blogs': recent_blogs,
        'featured_blogs': featured_blogs,
        'sidebar_gallery': sidebar_gallery,
        'upcoming_events': upcoming_events,
        'page_settings': page_settings,
    }
    
    return render(request, 'pages/blog/blog-detail.html', context)


def event_detail(request, slug):
    """Event detail"""
    from django.utils import timezone
    
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    context = {
        'event': event,
    }
    
    return render(request, 'pages/blog/event-detail.html', context)
