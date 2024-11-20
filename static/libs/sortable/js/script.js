let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()

function updatepath(dataLeft) {
    $.ajax({
        url: './updatepath',
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            dataLeft: JSON.stringify(dataLeft),
        },
        success: function (response) {
        }
    })
}

function removePage(page_id) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: './remove_page',
            type: 'POST',
            data: {
                page_id: page_id,
                csrfmiddlewaretoken: csrfmiddlewaretoken,
            },
            success: function (data) {
                resolve(data)
            },
            error: function (error) {
                reject(error)
            }
        })
    })
}


function buildTree(data, parentId) {
    const tree = [];
    data.forEach(item => {
        if (item.parent_id === parentId) {
            const children = buildTree(data, item.id);
            if (children.length) {
                item.children = children;
            }
            tree.push(item);
        }
    });
    return tree;
}

$(document).ready(async function () {
    let dataLeft = [
        {
            id: 1,
            parent_id: 0,
            title: 'Branch 1',
            level: 1,
        },
        {
            id: 2,
            parent_id: 1,
            title: 'Branch 1',
            level: 1,
        },
        {
            id: 3,
            parent_id: 1,
            title: 'Branch 1',
            level: 1,
        },
        {
            id: 2,
            parent_id: 2,
            title: 'Branch 1',
            level: 2,
        },
    ];


    await $.ajax({
        url: './getpagelist',
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
        },
        success: function (response) {
            dataLeft = response.page_list;
        }
    })

    const leftTreeId = '#left-tree';
    const leftSortable = new TreeSortable({
        treeSelector: leftTreeId,
    });
    const $leftTree = $(leftTreeId);
    const $content = dataLeft.map(leftSortable.createBranch);
    $leftTree.html($content);
    leftSortable.run();

    const delay = () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve();
            }, 1000);
        });
    };

    leftSortable.onSortCompleted(async (event, ui) => {
        await delay();
        dataLeft = []
        await $leftTree.find('li').map((index, item) => {
            const id = $(item).data('id');
            let parent_id = $(item).data('parent');
            const level = $(item).data('level');
            const title = $(item).find('.branch-title').text()
            if (level === 1) parent_id = 0;
            dataLeft.push({
                id: id,
                parent_id: parent_id,
                title: title,
                level: level,
            });
        });
        updatepath(dataLeft);
    });

    // leftSortable.addListener('click', '.add-child', function (event, instance) {
    //     event.preventDefault();
    //     instance.addChildBranch($(event.target));
    // });
    //
    // leftSortable.addListener('click', '.add-sibling', function (event, instance) {
    //     event.preventDefault();
    //     instance.addSiblingBranch($(event.target));
    // });

    leftSortable.addListener('click', '.remove-branch', function (event, instance) {
        event.preventDefault();
        const confirm = window.confirm('Are you sure you want to delete this branch?');
        if (!confirm) {
            return;
        }
        let page_id = $(event.target).data('id');

        removePage(page_id)
            .then((data) => {
                instance.removeBranch($(event.target));
            })
            .catch((error) => {

            })
    });
    tippy('[data-tippy-content]');
});
