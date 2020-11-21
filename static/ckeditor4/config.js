/**
 * @license Copyright (c) 2003-2020, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function (config) {
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    // config.uiColor = '#AADC6E';
    // config.toolbar = [
    //     ['Source', 'NewPage', 'DocProps', 'Preview'],
    //     ['Copy', 'Undo', 'Redo'],
    //     ['Find', 'Replace', 'SelectAll'],
    //     ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
    //     ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],
    //     ['Link', 'Unlink', 'Anchor'],
    //     ['Image',  'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
    //     '/', ['Styles', 'Format', 'Font', 'FontSize'],
    //     ['TextColor', 'BGColor'],
    //     ['Maximize', 'ShowBlocks']
    // ]
    // config.filebrowserImageUploadUrl = '/luntan/imageup/';
    CKEDITOR.editorConfig = function (config) {
        // Define changes to default configuration here. For example:
        // config.language = 'fr';
        // config.uiColor = '#AADC6E';
        config.toolbarGroups = [
            {name: 'clipboard', groups: ['clipboard', 'undo']},
            {name: 'editing', groups: ['find', 'selection', 'spellchecker', 'editing']},
            {name: 'forms', groups: ['forms']},
            {name: 'basicstyles', groups: ['basicstyles', 'cleanup']},
            {name: 'paragraph', groups: ['list', 'indent', 'blocks', 'align', 'bidi', 'paragraph']},
            {name: 'links', groups: ['links']},
            {name: 'insert', groups: ['insert']},
            {name: 'styles', groups: ['styles']},
            {name: 'colors', groups: ['colors']},
            {name: 'document', groups: ['document', 'doctools', 'mode']},
            {name: 'tools', groups: ['tools']},
            {name: 'others', groups: ['others']},
            {name: 'about', groups: ['about']}
        ];

        //上传图片窗口用到的接口
        config.filebrowserImageUploadUrl = '/luntan/imageup/';
        config.filebrowserUploadUrl = "https://192.168.0.1/api/ECategoryDetail/UploadImg";

        // 使上传图片弹窗出现对应的“上传”tab标签
        config.removeDialogTabs = 'image:advanced;link:advanced';

//粘贴图片时用得到
        config.extraPlugins = 'uploadimage';
        config.uploadUrl = 'https://192.168.0.1/api/ECategoryDetail/UploadImg';
    };
};