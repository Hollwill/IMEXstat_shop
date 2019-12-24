import { ComponentBase } from '@syncfusion/ej2-vue-base';
export declare const properties: string[];
export declare const modelProps: string[];
/**
 * Represents the Essential JS 2 VueJS Button Component
 * ```html
 * <ejs-button>Button</ejs-button>
 * ```
 */
export declare class ButtonComponent extends ComponentBase {
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
    render(createElement: any): any;
    click(): void;
    focusIn(): void;
}
export declare const ButtonPlugin: {
    name: string;
    install(Vue: any): void;
};
