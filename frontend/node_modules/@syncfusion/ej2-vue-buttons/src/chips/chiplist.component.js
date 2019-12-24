var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    }
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { ComponentBase, EJComponentDecorator } from '@syncfusion/ej2-vue-base';
import { ChipList } from '@syncfusion/ej2-buttons';
import { ChipsDirective, ChipDirective, ChipsPlugin, ChipPlugin } from './chips.directive';
export var properties = ['avatarIconCss', 'avatarText', 'chips', 'cssClass', 'enableDelete', 'enablePersistence', 'enableRtl', 'enabled', 'leadingIconCss', 'locale', 'selectedChips', 'selection', 'text', 'trailingIconCss', 'click', 'created', 'delete'];
export var modelProps = [];
/**
 * Represents the Essential JS 2 VueJS ChipList Component.
 * ```html
 * <ejs-chiplist></ejs-chiplist>
 * ```
 */
var ChipListComponent = /** @class */ (function (_super) {
    __extends(ChipListComponent, _super);
    function ChipListComponent() {
        var _this = _super.call(this) || this;
        _this.propKeys = properties;
        _this.models = modelProps;
        _this.hasChildDirective = true;
        _this.hasInjectedModules = false;
        _this.tagMapper = { "e-chips": "e-chip" };
        _this.tagNameMapper = {};
        _this.ej2Instances = new ChipList({});
        _this.bindProperties();
        _this.ej2Instances._setProperties = _this.ej2Instances.setProperties;
        _this.ej2Instances.setProperties = _this.setProperties;
        return _this;
    }
    ChipListComponent.prototype.setProperties = function (prop, muteOnChange) {
        var _this = this;
        if (this.ej2Instances && this.ej2Instances._setProperties) {
            this.ej2Instances._setProperties(prop, muteOnChange);
        }
        if (prop && this.models && this.models.length) {
            Object.keys(prop).map(function (key) {
                _this.models.map(function (model) {
                    if ((key === model) && !(/datasource/i.test(key))) {
                        _this.$emit('update:' + key, prop[key]);
                    }
                });
            });
        }
    };
    ChipListComponent.prototype.render = function (createElement) {
        return createElement('div', this.$slots.default);
    };
    ChipListComponent.prototype.add = function (chipsData) {
        return this.ej2Instances.add(chipsData);
    };
    ChipListComponent.prototype.find = function (fields) {
        return this.ej2Instances.find(fields);
    };
    ChipListComponent.prototype.getSelectedChips = function () {
        return this.ej2Instances.getSelectedChips();
    };
    ChipListComponent.prototype.remove = function (fields) {
        return this.ej2Instances.remove(fields);
    };
    ChipListComponent.prototype.select = function (fields) {
        return this.ej2Instances.select(fields);
    };
    ChipListComponent = __decorate([
        EJComponentDecorator({
            props: properties
        })
    ], ChipListComponent);
    return ChipListComponent;
}(ComponentBase));
export { ChipListComponent };
export var ChipListPlugin = {
    name: 'ejs-chiplist',
    install: function (Vue) {
        Vue.component(ChipListPlugin.name, ChipListComponent);
        Vue.component(ChipPlugin.name, ChipDirective);
        Vue.component(ChipsPlugin.name, ChipsDirective);
    }
};
