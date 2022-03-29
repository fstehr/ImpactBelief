let activeTab = 0;

function showCurrentTabOnly() {
    let tabIndex = 0;

    for (let tab of document.getElementsByClassName('tab')) {
        tab.style.display = tabIndex === activeTab ? 'block' : 'none';
        tabIndex++;
    }
}

showCurrentTabOnly();
for (let btn of document.getElementsByClassName('btn-tab')) {
    btn.onclick = function () {
        activeTab += parseInt(btn.dataset.offset);
        showCurrentTabOnly();
        window.scrollTo(0, 0);
    }
}