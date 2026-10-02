def scoped(queryset, organization):
    return queryset.filter(organization=organization)
