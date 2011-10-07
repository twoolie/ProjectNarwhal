from datetime import timedelta

# Default settings for ProjectNarwhal
SITE_NAME = "Project Narwhal"

#tracker settings
TRACKER_BACKEND = 'django'
TRACKER_PRIVATE = True
TRACKER_ANNOUNCE_STATS = True #keep U/D stats on users
TRACKER_ANNOUNCE_INTERVAL = 300

# Profile Settings
PROFILE_AVATAR_PROTECT = True # when set to true, this fetches a copy of all external avatars to the server locally so external observers cannot snoop your HTTP_REFERER
PROFILE_AVATAR_SIZE_SMALL = "30"
PROFILE_AVATAR_SIZE_MEDIUM = "94"
PROFILE_AVATAR_SIZE_LARGE = "200"
PROFILE_GRAVATAR_STANDIN = 'mm' #can be one of the options from http://en.gravatar.com/site/implement/images/
PROFILE_ACTIVE_TIMEOUT = 60 #seconds
PROFILE_IDLE_TIMEOUT = 300 #seconds

# Reddit Auth Backend (setup for a member in good standing)
USER_AGENT = 'ProjectNarwhal'
JOIN_MIN_COMMENT_KARMA = 350
JOIN_MIN_LINK_KARMA = 1
JOIN_MIN_MEMBER_TIME = timedelta(days=6*30)