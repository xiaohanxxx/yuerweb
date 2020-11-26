(function () {
    window.Toolfun = {
        clearClass: function (className, items) {
            for (var i = 0; i < items.length; i++) {
                if (items.eq(i).hasClass(className)) {
                    items.eq(i).removeClass(className);
                }
            }
        },
        diguiClass: function (datalis, comment) {
            var resData = [];
            for (const a in comment) {
                comment[a].child = [];
                var hChild = [];
                for (const b in datalis) {
                    if (comment[a].id == datalis[b].parent) {
                        hChild.push(datalis[b]);
                    }
                }
                if (hChild) {
                    comment[a].child = Toolfun.diguiClass(datalis, hChild);
                }
                resData.push(comment[a])
            }
            return comment = resData;
        }
    }
})();