let tabs = document.querySelectorAll('.tab');
let contents = document.querySelectorAll('.tab-content');

tabs.forEach((tab, i) => {
    tab.onclick = function() {
        contents.forEach((content) => {
            content.classList.remove('active');
        });
        tabs.forEach((tab) => {
            tab.classList.remove('active');
        });
        contents[i].classList.add('active');
        tabs[i].classList.add('active');
    };
});