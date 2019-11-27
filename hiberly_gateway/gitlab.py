from social_core.backends.gitlab import GitLabOAuth2 as SocialGitLabOAuth2 # type: ignore
from django.conf import settings
    
class GitLabOAuth2(SocialGitLabOAuth2):
    DEFAULT_SCOPE = ['api']
    API_URL = settings.GITLAB_URL
