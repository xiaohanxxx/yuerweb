/**
 * @license Copyright (c) 2003-2020, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function (config) {
    // Define changes to default configuration here. For example:
    config.language = 'zh-cn';
    config.uiColor = '#D1D1D1';
    config.toolbar = [
        ['Source', 'NewPage', 'DocProps', 'Preview'],
        ['Copy', 'Undo', 'Redo'],
        ['Find', 'Replace', 'SelectAll'],
        ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],
        ['Link', 'Unlink', 'Anchor'],
        ['Image',  'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
        '/', ['Styles', 'Format', 'Font', 'FontSize'],
        ['TextColor', 'BGColor'],
        ['Maximize', 'ShowBlocks']
    ];
    config.filebrowserImageUploadUrl = '/luntan/imageup/';
    config.resize_enabled = false;
    config.height = 520;
};