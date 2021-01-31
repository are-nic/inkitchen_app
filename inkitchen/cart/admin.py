'''
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    filter_horizontal = ('ingredients',)           # выбор ингрединетов в горизонтальном фильтре
    '''

