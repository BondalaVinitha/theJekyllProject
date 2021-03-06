# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView

from base.handlers.form_handler import FormHandler

from startbootstrap.constants import TemplateName
from startbootstrap.forms import (
    PageForm,
    PostForm,
    SiteProfileForm,
    SiteSocialForm
)
from startbootstrap.handlers.sbs_handlers import SBSHandler
from startbootstrap.handlers.sbs_form_handlers import SBSFormHandler

from theJekyllProject.dbio import RepoDbIO


class SBSThemeView(LoginRequiredMixin, View):
    """
    First view that will do all preliminary operations for setting up the
    startbootstrap blog.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle the post data. Ideally, reponame will be posted
        """
        user = self.request.user
        # FIXME can't do this we have to get the repo from the database.
        repo = request.data.get('repo')
        start_bootstrap = SBSHandler(user, repo)
        start_bootstrap.perform_initial_tasks()
        return HttpResponseRedirect(reverse('sbs-site-data'))


class SBSSiteDataView(LoginRequiredMixin, FormView):
    """
    Form View to handle site data of the startbootstrap theme
    """
    form_class = SiteProfileForm

    def get(self, request, *args, **kwargs):
        repo_name = RepoDbIO().get_repo(request.user).repo
        form_response = SBSFormHandler(
            request.user, repo_name).load_site_initials(
            request, self.form_class)

        return render(request,
                      TemplateName.SBS_POST_DATA, {'form': form_response})

    def post(self, request, *args, **kwargs):
        form_field_dict = FormHandler(
            request, self.form_class).handle_post_fields((
                'title',
                'description',
                'author',
                'baseurl',
                'url')
        )
        user = request.user
        repo_name = RepoDbIO().get_repo(request.user).repo
        SBSFormHandler(user,
                       repo_name).post_site_data(user, form_field_dict)

        return render(request, TemplateName.SBS_SITE_DATA,
                      {'msg': 'Site data updated successfully.'})


class SBSSocialDataView(LoginRequiredMixin, FormView):
    form_class = SiteSocialForm

    def get(self, request, *args, **kwargs):
        repo_name = RepoDbIO().get_repo(request.user).repo
        form_response = SBSFormHandler(
            request.user, repo_name).load_social_profile_initials(
            request, self.form_class)

        return render(request,
                      TemplateName.SBS_SOCIAL_DATA,
                      {'form': form_response})

    def post(self, request, *args, **kwargs):
        form_field_dict = FormHandler(
            request, self.form_class).handle_post_fields((
                'email',
                'facebook',
                'github',
                'twitter')
        )
        user = request.user
        repo_name = RepoDbIO().get_repo(request.user).repo
        SBSFormHandler(
            user, repo_name).post_social_profile_data(user, form_field_dict)

        return render(request, TemplateName.SBS_SOCIAL_DATA,
                      {'msg': 'Social data updated successfully.'})


# TODO Add index background in site data view. More work is required there.
class SBSPostView(LoginRequiredMixin, FormView):
    form_class = PostForm

    def get(self, request, pk='', *args, **kwargs):
        repo_name = RepoDbIO().get_repo(request.user).repo
        form_response = SBSFormHandler(
            request.user, repo_name).load_posts_initials(
            request, self.form_class, pk)

        return render(request, TemplateName.SBS_POST_DATA,
                      {'form': form_response, 'media': settings.MEDIA_URL})

    # TODO write the post method properly
    def post(self, request, pk='', *args, **kwargs):
        form_field_dict = FormHandler(
            request, self.form_class).handle_post_fields((
                'date',
                'time',
                'title',
                'subtitle',
                'background',
                'content')
        )
        user = request.user
        repo_name = RepoDbIO().get_repo(request.user).repo
        SBSFormHandler(
            user, repo_name).post_posts_data(user, form_field_dict)

        return render(request, TemplateName.SBS_POST_DATA,
                      {'msg': 'Post updated successfully.'})


# TODO Add index background in site data view. More work is required there.
class SBSPageView(LoginRequiredMixin, FormView):
    form_class = PageForm

    def get(self, request, pk='', *args, **kwargs):
        repo_name = RepoDbIO().get_repo(request.user).repo
        form_response = SBSFormHandler(
            request.user, repo_name).load_page_initials(
            request, self.form_class, pk)

        return render(request, TemplateName.SBS_PAGE_DATA,
                      {'form': form_response, 'media': settings.MEDIA_URL})

    # TODO write the post method properly
    def post(self, request, pk='', *args, **kwargs):
        form_field_dict = FormHandler(
            request, self.form_class).handle_post_fields((
                'title',
                'description',
                'background',
                'content')
        )
        user = request.user
        repo_name = RepoDbIO().get_repo(request.user).repo
        SBSFormHandler(
            user, repo_name).post_page_data(user, form_field_dict)

        return render(request, TemplateName.SBS_PAGE_DATA,
                      {'msg': 'Post updated successfully.'})
