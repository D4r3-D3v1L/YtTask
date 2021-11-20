from django.shortcuts import render , redirect
from googleapiclient.discovery import build
from .forms import SearchForm 
from .models import Video
from datetime import datetime
from django.views.generic import ListView
from django.core.paginator import Paginator

def home(request):
	return render(request,"base.html")

class VideoListView(ListView):
	model = Video
	template_name = "videos.html"
	context_object_name = 'videos'
	ordering = ["-publishedAt"]
	paginate_by = 10

def dataExtractView(request):
	videos_list=[]
	if request.method=="GET":
		word = "cricket"
		api_key = 'AIzaSyAU0SbOPMnqN3mCOwsOmlG2rJc56V5SD80'
		youtube = build('youtube', 'v3', developerKey=api_key)
		token = None
		query = youtube.search().list(
			order = "date",
			part = "snippet",
			q=word,
			type='video',
			publishedAfter="2021-11-18T21:00:00Z",
			pageToken = token,
			maxResults=10,
		)
		result = query.execute()
		for item in result['items']:
			snippetValues = item["snippet"]

			title = snippetValues["title"]
			description = snippetValues["description"]
			publishedAt = stringToDate(snippetValues["publishedAt"])
			thumbnailsUrls = []
			for thumbnailKey,thumbnailValue in snippetValues["thumbnails"].items():
				thumbnailsUrls.append(thumbnailValue["url"])

			for video in Video.objects.all():
				if (video.title == title and video.description == description):
					break
			else:
				Video.objects.create(title=title,description=description,publishedAt=publishedAt,thumbnailsUrls=thumbnailsUrls[0])

			
			# print({"title":title,"description":description,"publishedAt":publishedAt,"thumbnailsUrls":thumbnailsUrls})
	return redirect('videos')

def stringToDate(string):
	
	string = string.split("+")[0]
	date = datetime.strptime(string, '%Y-%m-%dT%XZ')
	return date

def searchView(request):
	if request.method=="GET":
		form = SearchForm()
		if "search_word" in request.GET:
			print("Hello")
			search_word = request.GET["search_word"]
			videos=[]
			for video in Video.objects.all():
				if ( (search_word.lower() in video.title.lower()) or (search_word.lower() in video.description.lower()) ):
					videos.append(video)
			print(len(videos))
			paginator = Paginator(videos,10)
			page_number = request.GET.get("page")
			page_obj = paginator.get_page(page_number)
			return render(request,"search.html",{"page_obj":page_obj,"search_word":search_word})
		else:
			return render(request,"search_form.html",{"form":form})
	return redirect("videos")
