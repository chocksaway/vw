# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect
from adverts.forms import UserForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from random import randint
from search.ForumSearch import ForumSearch


def index(request):
    return render_to_response('templates/index.html', {
    })


#@login_required
def search(request):
    forum_search = ForumSearch()
    #return HttpResponse(forum_search.parse_forum("http://ssvc.org.uk/phpbb/viewforum.php?f=4",
    #                                             "viewtopic\.php.*")
    #)

    forum_search = ForumSearch()
    return HttpResponse(forum_search.parse_forum("http://ssvc.org.uk/phpbb/viewforum.php?f=4",
                                                 {'class_': 'topictitle'})
                        )


    #return render_to_response('view_search.html', {
    #    'post': get_object_or_404(VWUser)
    #})

@cache_page(60 * 1)
def cache_me(request):
    cache.set('a-unique-key', randint(1, 100))
    return HttpResponse(cache.get('a-unique-key'))

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            user = user
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
        'templates/register.html',
        {'user_form': user_form, 'registered': registered},
        context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.

                user = login(request, user)

                return HttpResponse("You're logged in.")

                #return HttpResponseRedirect(reverse('index', args=(user.is_authenticated(),)))

                #return HttpResponse("You're logged in.")
                #return render_to_response('/mysite/', context, context_instance=RequestContext(request))

                #return redirect('/mysite/' % {user})
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your VW Adverts account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('templates/login.html', {}, context)