# from social_core.backends.linkedin import LinkedinOAuth2

# class CustomLinkedinOAuth2(LinkedinOAuth2):
#     def get_user_details(self, response):
#         """
#         Custom method to extract user details from LinkedIn's API response.
#         Only the fields that are available via OAuth 2.0 scopes are included.
#         """
#         user_data = {
#             'username': response.get('localizedFirstName', '') + ' ' + response.get('localizedLastName', ''),
#             'first_name': response.get('localizedFirstName', ''),
#             'last_name': response.get('localizedLastName', ''),
#             'email': response.get('emailAddress', ''),
#             'profile_photo_url': response.get('profilePicture', {}).get('displayImage', '')  # This provides the profile photo URL.
#         }
#         return user_data
def get_user_details(self, response):
    print(response)  # Log the entire response to check available fields
    first_name = response.get('firstName', {}).get('localized', {}).get('en_US', 'No first name')
    last_name = response.get('lastName', {}).get('localized', {}).get('en_US', 'No last name')
    return {
        'username': response.get('id'),
        'email': response.get('emailAddress'),
        'first_name': first_name,
        'last_name': last_name,
        'profile_picture': response.get('profilePicture', {}).get('displayImage', ''),
    }
