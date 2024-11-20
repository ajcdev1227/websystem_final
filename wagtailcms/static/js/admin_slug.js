$(document).ready(function () {
    $("input[name='slug']").on('keyup paste', function () {
        $("input[name='slug']").not(this).val($(this).val());
    });
    $("input[name='seo_title']").on('keyup paste', function () {
        $("input[name='seo_title']").not(this).val($(this).val());
    });
    $("textarea[name='search_description']").on('keyup paste', function () {
        $("textarea[name='search_description']").not(this).val($(this).val());
    });
    $("input[name='show_in_menus']").change(function () {
        $("input[name='show_in_menus']").not(this).prop('checked', this.checked);
    });
});
