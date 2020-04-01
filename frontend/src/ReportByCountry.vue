<template>
    <div class="report-by-tnved">
        <top-block
                :date="date"
                :params="params"
                :interval="interval"
                :category="category"
                :item_list="tnved_list"
                :get_by="'country'"
                :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
        ></top-block>
        <middle-down-block
                :date="date"
                :params="params"
                :interval="interval"
                :category="category"
                :item_list="tnved_list"
                :get_by="'country'"
                :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
                :block_place="'middle'"
        ></middle-down-block>
        <middle-down-block
                :date="date"
                :params="params"
                :interval="interval"
                :category="category"
                :item_list="tnved_list"
                :get_by="'country'"
                :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
                :block_place="'down'"
        ></middle-down-block>
        <!--    <dynamic-selected-country-->
        <!--            :date="date"-->
        <!--            :params="params"-->
        <!--            :interval="interval"-->
        <!--            :category="category"-->
        <!--            :tnved_list="tnved_list"-->
        <!--    ></dynamic-selected-country>-->
        <!--    <dynamic-tnved-by-selected-country-->
        <!--            :date="date"-->
        <!--            :params="params"-->
        <!--            :interval="interval"-->
        <!--            :category="category"-->
        <!--            :tnved_list="tnved_list"-->
        <!--    ></dynamic-tnved-by-selected-country>-->
        <!--    <dynamic-region-by-selected-country-->
        <!--            :date="date"-->
        <!--            :params="params"-->
        <!--            :interval="interval"-->
        <!--            :category="category"-->
        <!--            :tnved_list="tnved_list"-->
        <!--    ></dynamic-region-by-selected-country>-->
    </div>
</template>

<script>
    export default {
        name: "ReportByTnved",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        components: {
            TopBlock: () => import('./report_blocks/TopBlock'),
            MiddleDownBlock: () => import('./report_blocks/MiddleDownBlock')
            // DynamicSelectedCountry: () => import('./report_country/DynamicSelectedCountry'),
            // DynamicTnvedBySelectedCountry: () => import('./report_country/DynamicTnvedBySelectedCountry'),
            // DynamicRegionBySelectedCountry: () => import('./report_country/DynamicRegionBySelectedCountry'),
        }
    }
</script>

<style scoped>

</style>