import { ComponentBase } from '@syncfusion/ej2-vue-base';
export declare const properties: string[];
export declare const modelProps: string[];
/**
 * Represents the Essential JS 2 VueJS CheckBox Component
 * ```html
 * <ejs-checkbox label='Default'></ejs-checkbox>
 * ```
 */
export declare class CheckBoxComponent extends ComponentBase {
    ej2Instances: any;
    propKeys: string[];
    models: string[];
    hasChildDirective: boolean;
    protected hasInjectedModules: boolean;
    tagMapper: {
        [key: string]: Object;
    };
    tagNameMapper: Object;
    constructor();
    setProperties(prop: any, muteOnChange: boolean): void;
    trigger(eventName: string, eventProp: {
        [key: string]: Object;
    }, successHandler?: Function): void;
    render(createElement: any): any;
    click(): void;
    focusIn(): void;
}
export declare const CheckBoxPlugin: {
    name: string;
    install(Vue: any): void;
};
