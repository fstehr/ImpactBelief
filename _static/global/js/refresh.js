// https://stackoverflow.com/questions/18999501/bootstrap-3-keep-selected-tab-on-page-refresh

// Here I tried to remove this variable
function resetTabs() {
    console.log("Hello world!");

    // This keeps active tab in front when refreshing page or when there are form errors
    $('a[data-toggle="tab"]').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

}

    $('a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
        var id = $(e.target).attr("href");
        localStorage.setItem('selectedTab', id)
    });

    var selectedTab = localStorage.getItem('selectedTab');
    if (selectedTab != null) {
        $('a[data-toggle="tab"][href="' + selectedTab + '"]').tab('show');
    }

    window.onunload = (event) => {
    console.log('The page is unloaded');
};

    window.onload = (event) => {
    console.log('The page is loaded');
};