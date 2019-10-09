from social_core.backends.gitlab import GitLabOAuth2 as SocialGitLabOAuth2 # type: ignore
    
class GitLabOAuth2(SocialGitLabOAuth2):
    DEFAULT_SCOPE = ['api']
