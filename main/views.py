from django.http import Http404
from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


@login_required
def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'main/topics.html', context)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    user_name = request.user
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic,
               'entries': entries, 'user_name': str(user_name)}
    return render(request, 'main/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.user_name = request.user
            form.save()
            return redirect('main:topics')
    context = {'form': form}
    return render(request, 'main/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.user_name = request.user
            new_entry.save()
            return redirect('main:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'main/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if entry.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            entry.save()
            return redirect('main:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'main/edit_entry.html', context)
