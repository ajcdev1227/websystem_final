
Vvveb.ComponentsGroup['SoftUI'] =
["html/softcard", "html/softtextinput"];

Vvveb.Components.extend("_base", "html/softcard", {
    classes: ["card"],
    image: "icons/panel.svg",
    name: "Card",
    html: '<div class="card">\
            <div class="card-body p-3">\
                <div class="row">\
                    <div class="col-8">\
                        <div class="numbers">\
                            <p class="text-sm mb-0 text-capitalize font-weight-bold">Heading Text</p>\
                            <h5 class="font-weight-bolder mb-0">\
                                0\
                                <span class="text-success text-sm font-weight-bolder">+0%</span>\
                            </h5>\
                        </div>\
                    </div>\
                    <div class="col-4 text-end">\
                        <div class="icon icon-shape bg-gradient-primary shadow text-center border-radius-md">\
                            <i class="ni ni-world text-lg opacity-10" aria-hidden="true"></i>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>'
});

Vvveb.Components.extend("_base", "html/softtextinput", {
    name: "Input",
	nodes: ["input"],
	attributes: {"type":"text"},
    image: "icons/text_input.svg",
    html: '<div class="input-group">\
            <span class="input-group-text text-body"><i class="fas fa-search" aria-hidden="true"></i></span>\
            <input type="text" class="form-control" placeholder="Type here..." onfocus="focused(this)" onfocusout="defocused(this)">\
            </div>',
    properties: [{
        name: "Value",
        key: "value",
        htmlAttr: "value",
        inputtype: TextInput
    }, {
        name: "Type",
        key: "type",
        htmlAttr: "type",
		inputtype: SelectInput,
        data: {
            options: [{
                value: "text",
                text: "text"
            }, {
                value: "button",
                text: "button"
            }, {
                value: "checkbox",
                text: "checkbox"
            }, {
                value: "color",
                text: "color"
            }, {
                value: "date",
                text: "date"
            }, {
                value: "datetime-local",
                text: "datetime-local"
            }, {
                value: "email",
                text: "email"
            }, {
                value: "file",
                text: "file"
            }, {
                value: "hidden",
                text: "hidden"
            }, {
                value: "image",
                text: "image"
            }, {
                value: "month",
                text: "month"
            }, {
                value: "number",
                text: "number"
            }, {
                value: "password",
                text: "password"
            }, {
                value: "radio",
                text: "radio"
            }, {
                value: "range",
                text: "range"
            }, {
                value: "reset",
                text: "reset"
            }, {
                value: "search",
                text: "search"
            }, {
                value: "submit",
                text: "submit"
            }, {
                value: "tel",
                text: "tel"
            }, {
                value: "text",
                text: "text"
            }, {
                value: "time",
                text: "time"
            }, {
                value: "url",
                text: "url"
            }, {
                value: "week",
                text: "week"
            }]
        }
    }, {
        name: "Placeholder",
        key: "placeholder",
        htmlAttr: "placeholder",
        inputtype: TextInput
    }, {
        name: "Disabled",
        key: "disabled",
        htmlAttr: "disabled",
		col:6,
        inputtype: CheckboxInput,
	},{
        name: "Required",
        key: "required",
        htmlAttr: "required",
		col:6,
        inputtype: CheckboxInput,
    }]
});