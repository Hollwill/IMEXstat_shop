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
import Vue from 'vue';
import { EJComponentDecorator } from '@syncfusion/ej2-vue-base';
var ChipsDirective = /** @class */ (function (_super) {
    __extends(ChipsDirective, _super);
    function ChipsDirective() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ChipsDirective.prototype.render = function () {
        return;
    };
    ChipsDirective = __decorate([
        EJComponentDecorator({})
    ], ChipsDirective);
    return ChipsDirective;
}(Vue));
export { ChipsDirective };
export var ChipsPlugin = {
    name: 'e-chips',
    install: function (Vue) {
        Vue.component(ChipsPlugin.name, ChipsDirective);
    }
};
/**
 * `e-chip` directive represent a chip of the Vue ChipList.
 * ```html
 * <ejs-chiplist >
 *   <e-chips>
 *    <e-chip text='chip1'></e-chip>
 *    <e-chip text='chip2'></e-chip>
 *   </e-chips>
 * </ejs-chiplist>
 * ```
 */
var ChipDirective = /** @class */ (function (_super) {
    __extends(ChipDirective, _super);
    function ChipDirective() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ChipDirective.prototype.render = function () {
        return;
    };
    ChipDirective = __decorate([
        EJComponentDecorator({})
    ], ChipDirective);
    return ChipDirective;
}(Vue));
export { ChipDirective };
export var ChipPlugin = {
    name: 'e-chip',
    install: function (Vue) {
        Vue.component(ChipPlugin.name, ChipDirective);
    }
};
