from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from wagtail.admin.views.generic import CreateView, DeleteView, EditView, IndexView
from wagtail.compat import AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME
from wagtail.permission_policies import ModelPermissionPolicy
from wagtail.users.forms import UserCreationForm, UserEditForm
from wagtail.users.utils import user_can_delete_user
from wagtail.utils.loading import get_custom_form
from django.shortcuts import render,redirect
from home.models import CustomUser
from home.utils import  generate_short_uuid
from django.contrib.auth.hashers import make_password
import requests
User = get_user_model()


# Typically we would check the permission 'auth.change_user' (and 'auth.add_user' /
# 'auth.delete_user') for user management actions, but this may vary according to
# the AUTH_USER_MODEL setting
add_user_perm = f"{AUTH_USER_APP_LABEL}.add_{AUTH_USER_MODEL_NAME.lower()}"
change_user_perm = "{}.change_{}".format(
    AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower()
)
delete_user_perm = "{}.delete_{}".format(
    AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME.lower()
)

def get_user_creation_form():
    form_setting = "WAGTAIL_USER_CREATION_FORM"
    if hasattr(settings, form_setting):
        return get_custom_form(form_setting)
    else:
        return UserCreationForm


def send_post_request(company,customer_id, firstname, lastname, email, password):
    php_url = "https://www.advisorcrm.net/scripts/_account-user-add.php"
    query_string = {
        "acx_customer_id": customer_id,
        "customer_name": company,
        "first_name": firstname,
        "last_name": lastname,
        "email": email,
        "nickname": password,
        "phone": "(221)2223344",
        "timezone": "EST",
        "notes": "test notes",
        "twilio_phone": "9998884455",
        "twilio_sid": "kjsyetrxdf",
        "twilio_token": "pirstrwvn",
        "use_system_twilio": "0"
    }

    response = requests.post(php_url, data=query_string)


def create_user(request):
    template_name = "wagtailusers/users/create.html"
    form_class = get_user_creation_form()
    if request.method == "POST":

        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = first_name + ' ' + last_name
        password = request.POST.get('password1')
        company = request.user.company
        customer_id = generate_short_uuid()
        hash_password = make_password(password)
        is_superuser = 0

        if request.POST.get('is_superuser'):
            is_superuser = 1

        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            display_name=username,
            password=hash_password,
            company=company,
            customer_id=customer_id,
            is_superuser=is_superuser,
            domain_url=request.user.domain_url,

        )
        user.save()

        if request.POST.get('groups'):
            if request.POST.get('groups') == '1':
                group, created = Group.objects.get_or_create(name='Moderators')
            else:
                group, created = Group.objects.get_or_create(name='Editors')

            user.groups.add(group)

        send_post_request(company.company, company.id, first_name, last_name, email, password)
        return redirect('/cms/users/')
    else:
        return render(request, template_name, context={'form': form_class})




def get_user_edit_form():
    form_setting = "WAGTAIL_USER_EDIT_FORM"
    if hasattr(settings, form_setting):
        return get_custom_form(form_setting)
    else:
        return UserEditForm


def get_users_filter_query(q, model_fields):
    conditions = Q()

    for term in q.split():
        if "username" in model_fields:
            conditions |= Q(username__icontains=term)

        if "first_name" in model_fields:
            conditions |= Q(first_name__icontains=term)

        if "last_name" in model_fields:
            conditions |= Q(last_name__icontains=term)

        if "email" in model_fields:
            conditions |= Q(email__icontains=term)

    return conditions


class Index(IndexView):
    """
    Lists the users for management within the admin.
    """

    template_name = "wagtailusers/users/index.html"
    results_template_name = "wagtailusers/users/results.html"
    any_permission_required = ["add", "change", "delete"]
    permission_policy = ModelPermissionPolicy(User)
    model = User
    context_object_name = "users"
    index_url_name = "wagtailusers_users:index"
    add_url_name = "wagtailusers_users:add"
    edit_url_name = "wagtailusers_users:edit"
    default_ordering = "name"
    paginate_by = 20
    is_searchable = True
    page_title = gettext_lazy("Users")

    model_fields = [f.name for f in User._meta.get_fields()]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, id=args[0]) if args else None
        self.group_filter = Q(groups=self.group) if self.group else Q()

    def get_index_results_url(self):
        if self.group:
            return reverse("wagtailusers_groups:users_results", args=[self.group.pk])
        else:
            return reverse("wagtailusers_users:index_results")

    def get_valid_orderings(self):
        return ["name", "username"]

    def get_queryset(self):
        model_fields = set(self.model_fields)
        if self.is_searching:
            conditions = get_users_filter_query(self.search_query, model_fields)
            users = User.objects.filter(self.group_filter, conditions, company=self.request.user.company)
        else:
            users = User.objects.filter(self.group_filter, company=self.request.user.company)

        if self.locale:
            users = users.filter(locale=self.locale)

        if "wagtail_userprofile" in model_fields:
            users = users.select_related("wagtail_userprofile")

        if "last_name" in model_fields and "first_name" in model_fields:
            users = users.order_by("last_name", "first_name")

        if self.get_ordering() == "username":
            users = users.order_by(User.USERNAME_FIELD)

        print('test',self.request.user.company)
        return users

    def get_context_data(self, *args, object_list=None, **kwargs):
        context_data = super().get_context_data(
            *args, object_list=object_list, **kwargs
        )
        context_data["ordering"] = self.get_ordering()
        context_data["group"] = self.group

        context_data.update(
            {
                "app_label": User._meta.app_label,
                "model_name": User._meta.model_name,
            }
        )
        return context_data




class Edit(EditView):
    """
    Provide the ability to edit a user within the admin.
    """

    model = User
    permission_policy = ModelPermissionPolicy(User)
    form_class = get_user_edit_form()
    template_name = "wagtailusers/users/edit.html"
    index_url_name = "wagtailusers_users:index"
    edit_url_name = "wagtailusers_users:edit"
    delete_url_name = "wagtailusers_users:delete"
    success_message = gettext_lazy("User '%(object)s' updated.")
    context_object_name = "user"
    error_message = gettext_lazy("The user could not be saved due to errors.")

    def get_page_title(self):
        return _("Editing %(object)s") % {"object": self.object.get_username()}

    def get_page_subtitle(self):
        return ""

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()
        self.can_delete = user_can_delete_user(request.user, self.object)
        self.editing_self = request.user == self.object

    def save_instance(self):
        instance = super().save_instance()
        if self.object == self.request.user and "password1" in self.form.changed_data:
            # User is changing their own password; need to update their session hash
            update_session_auth_hash(self.request, self.object)
        return instance

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "editing_self": self.editing_self,
            }
        )
        return kwargs

    def run_before_hook(self):
        return self.run_hook(
            "before_edit_user",
            self.request,
            self.object,
        )

    def run_after_hook(self):
        return self.run_hook(
            "after_edit_user",
            self.request,
            self.object,
        )

    def get_edit_url(self):
        return reverse(self.edit_url_name, args=(self.object.pk,))

    def get_delete_url(self):
        return reverse(self.delete_url_name, args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.pop("action_url")
        context["can_delete"] = self.can_delete
        return context


class Delete(DeleteView):
    """
    Provide the ability to delete a user within the admin.
    """

    permission_policy = ModelPermissionPolicy(User)
    permission_required = "delete"
    model = User
    template_name = "wagtailusers/users/confirm_delete.html"
    delete_url_name = "wagtailusers_users:delete"
    index_url_name = "wagtailusers_users:index"
    page_title = gettext_lazy("Delete user")
    context_object_name = "user"
    success_message = gettext_lazy("User '%(object)s' deleted.")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not user_can_delete_user(self.request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def run_before_hook(self):
        return self.run_hook(
            "before_delete_user",
            self.request,
            self.object,
        )

    def run_after_hook(self):
        return self.run_hook(
            "after_delete_user",
            self.request,
            self.object,
        )
