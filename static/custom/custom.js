function onPublishBtnClicked(page_id) {
    var messageData = {
        data: page_id,
        flag: "onPublishBtnClicked"
    };
    parent.postMessage(messageData, '*');
}