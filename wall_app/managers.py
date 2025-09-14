from django.db import models
import re 
from collections import defaultdict
import bcrypt

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z\s\-'`]{1,}$")
PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$")
EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

class UserManager(models.Manager):
    def validate_registration(self,postData):
        err = defaultdict(list)
        fName = postData.get('first_name')
        lName = postData.get('last_name')
        email = postData.get('email')
        pw = postData.get('password')
        confirm_pw = postData.get('confirm_password')
        
        # first_name and last_name validation
        if len(fName) < 2 or not NAME_RE.fullmatch(fName):
            err['first_name'].append("First name must be at least 2 letters.")
        if len(lName) < 2 or not NAME_RE.fullmatch(lName):
            err['last_name'].append("Last name must be at least 2 letters.")
        
        # email validation
        if not email or not EMAIL_RE.fullmatch(email):
            err['email'].append("Please enter a valid email address")
        elif self.model.objects.filter(email=email).exists():
            err['email'].append("This email is already used")
        
        # password and confirm pass validation
        if not pw or len(pw) < 8 or not PASSWORD_RE.fullmatch(pw):
            err['password'].append('Password must be 8+ chars and include a letter and a number.')
            
        if pw != confirm_pw:
            err['confirm_password'].append('Passwords not matched.')
        
        return dict(err)
    def validate_login(self,postData):
        err = defaultdict(list)
        email = postData.get('email')
        pw = postData.get('password')


        # Email
        if not email:
            err['email'].append('Please enter email.')
        elif not EMAIL_RE.fullmatch(email):
            err['email'].append('Please enter a valid email address.')

        # Password
        if not pw:
            err['password'].append('Please enter password.')
        elif len(pw) < 8:
            err['password'].append('Password must be at least 8 characters.')

        if not err.get('email') and not err.get('password'):
            user = self.model.objects.filter(email=email).first()
            if not user:
                err['login'].append('This email or password is not correct.')
            else:
                try:
                    if not bcrypt.checkpw(pw.encode(), user.password.encode()):
                        err['login'].append('This email or password is not correct.')
                except (TypeError, ValueError):
                    err['login'].append('This email or password is not correct.')

        return dict(err)
        