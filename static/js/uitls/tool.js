(function() {
    window.Toolfun = {
        clearClass: function(className, items) {
            for (var i = 0; i < items.length; i++) {
                if (items.eq(i).hasClass(className)) {
                    items.eq(i).removeClass(className);
                }
            }
        }
    }
})();