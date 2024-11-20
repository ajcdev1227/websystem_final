from django import template

from home.models import CustomUser, Client

register = template.Library()


@register.simple_tag
def limit_string_tag(length, string):
    if len(string) > length:
        return string[:length] + "..."
    else:
        return string[:length]


@register.simple_tag
def status(status):
    if status == 'APPROVED':
        return '<span class="badge badge-sm bg-gradient-success">{0}</span>'.format(status)
    elif status == 'DENIED':
        return '<span class="badge badge-sm bg-gradient-success">{0}</span>'.format(status)
    else:
        return '<span class="badge badge-sm bg-gradient-primary">PENDING</span>'


@register.simple_tag
def enabledTenant(customer_id):
    tenant = CustomUser.objects.filter(customer_id=customer_id).first()
    if tenant.approved == 1:
        return "checked"
    else:
        return ""


@register.simple_tag
def enable_self_managed_compliance(username: str) -> str:
    client = Client.objects.filter(tenant_name=username).first()
    if client.enable_self_managed_compliance:
        return "checked"
    else:
        return ""


@register.filter
def create_range(value):
    return range(1, value + 1)


@register.inclusion_tag('includes/tree_template.html')
def generate_nested_list(data):
    return {'data': data}


@register.inclusion_tag('menu/navbar_template.html')
def navbar(data):
    return {'data': data}


@register.inclusion_tag('menu/submenu_template.html')
def submenu(menu_items):
    return {'menu_items': menu_items}

@register.filter
def replace_space_to_dash(value):
    return value.replace(" ", "_")
