function shipei() {
    if (document.documentElement.clientWidth > 1024) {
        document.documentElement.style.width = 1024;
        document.documentElement.style.fontSize = 1024 / 10 + 'px';
    } else if (document.documentElement.clientWidth < 320) {
        document.documentElement.style.width = 320;
        document.documentElement.style.fontSize = 320 / 10 + 'px';
    } else {
        document.documentElement.style.fontSize = document.documentElement.clientWidth / 10 + 'px';
    }
}
shipei();
window.onresize = shipei;