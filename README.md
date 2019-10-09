# Hibely GitLab API Gateway

This API gateway allows you to let your users use Hiberly on GitLab without giving access to your code.

The gateway has its own OAuth provider which Hiberly plugs in to. Schematically it works something like this:
```
Authentication:
                                                          
    Hiberly redirects user to Gateway (holds gateway token)
              |   |                                       
              |   |                                       
    Gateway (holds GitLab access token, which Hiberly never sees)                
              |   |                                       
              |   |                                       
    GitLab authorization process                         
                                                          
API request:                             
                                                          
    Hiberly makes request to Gateway                      
              |   |                                       
              |   |                                       
    Gateway checks token against DB,                           
       only allows certain endpoints and redacts others   
              |   |                                       
              |   |                                       
    GitLab API request                                    
```

You can see the exact endpoints and redacting in `hiberly_gateway/urls.py`

## Getting started

`docker-compose up`

Run migrations

`docker-compose exec web python manage.py migrate`

Create an application (and send those credentials to us)
`docker-compose exec web python manage.py create_app`

Create a GitLab app at https://gitlab.com/profile/applications

Edit the GitLab credentials with your own app credentials in settings.py

Done!