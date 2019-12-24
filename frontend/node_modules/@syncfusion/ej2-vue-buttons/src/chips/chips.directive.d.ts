import Vue from 'vue';
export declare class ChipsDirective extends Vue {
    render(): void;
}
export declare const ChipsPlugin: {
    name: string;
    install(Vue: any): void;
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
export declare class ChipDirective extends Vue {
    render(): void;
}
export declare const ChipPlugin: {
    name: string;
    install(Vue: any): void;
};
