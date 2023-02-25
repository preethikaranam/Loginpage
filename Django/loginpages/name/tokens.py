from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def make_has_value(self,user,timestamp):
        return(text_type(info.pk)+text_type(timestamp))
        #pk=primekeygenerate code #generate string

generate_token=TokenGenerator()