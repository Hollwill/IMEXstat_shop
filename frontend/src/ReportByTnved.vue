<template>
    <div class="report-by-tnved">
        <top-block
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :item_list="tnved_list"
            :get_by="'tnved'"
            :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
        ></top-block>
        <middle-down-block
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :item_list="tnved_list"
            :get_by="'tnved'"
            :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
            :block_place="'middle'"
        ></middle-down-block>
        <middle-down-block
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :item_list="tnved_list"
            :get_by="'tnved'"
            :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
            :block_place="'down'"
        ></middle-down-block>
<!--        <middle-down-block-->
<!--            :date="date"-->
<!--            :params="params"-->
<!--            :interval="interval"-->
<!--            :category="category"-->
<!--            :item_list="tnved_list"-->
<!--            :get_by="'tnved'"-->
<!--            :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"-->
<!--            :block_place="'down'"-->
<!--        ></middle-down-block>-->



<!--        <dynamic-selected-tnved-->
<!--                :date="date"-->
<!--                :params="params"-->
<!--                :interval="interval"-->
<!--                :category="category"-->
<!--                :tnved_list="tnved_list"-->
<!--        ></dynamic-selected-tnved>-->
<!--        <dynamic-country-by-selected-tnved-->
<!--                :date="date"-->
<!--                :params="params"-->
<!--                :interval="interval"-->
<!--                :category="category"-->
<!--                :tnved_list="tnved_list"-->
<!--        ></dynamic-country-by-selected-tnved>-->
<!--        <dynamic-region-by-selected-tnved-->
<!--                :date="date"-->
<!--                :params="params"-->
<!--                :interval="interval"-->
<!--                :category="category"-->
<!--                :tnved_list="tnved_list"-->
<!--        ></dynamic-region-by-selected-tnved>-->
    </div>
</template>

<script>
    export default {
        name: "ReportByTnved",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        components: {
            TopBlock: () => import('./report_blocks/TopBlock'),
            MiddleDownBlock: () => import('./report_blocks/MiddleDownBlock')
            // DynamicSelectedTnved: () => import('./report_tnved/DynamicSelectedTnved'),
            // DynamicCountryBySelectedTnved: () => import('./report_tnved/DynamicCountryBySelectedTnved'),
            // DynamicRegionBySelectedTnved: () => import('./report_tnved/DynamicRegionBySelectedTnved'),
        }
    }
</script>

<style scoped>

</style>