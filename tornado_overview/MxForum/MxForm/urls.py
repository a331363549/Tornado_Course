from MxForum.apps.users import urls as user_urls
from MxForum.apps.community import urls as community_urls
from MxForum.apps.question import urls as question_urls

urlpattern = []

urlpattern += user_urls.urlpattern