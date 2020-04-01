<template>
    <div class="report-by-region">
        <top-block
                :date="date"
                :params="params"
                :interval="interval"
                :category="category"
                :item_list="tnved_list"
                :get_by="'region'"
                :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
        ></top-block>
        <middle-down-block
                :date="date"
                :params="params"
                :interval="interval"
                :category="category"
                :item_list="tnved_list"
                :get_by="'region'"
                :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
                :block_place="'middle'"
        ></middle-down-block>
        <middle-down-block
                :date="date"
                :params="params"
                :interval="interval"
                :category="category"
                :item_list="tnved_list"
                :get_by="'region'"
                :headers="['some_name 1', 'some_name 1', 'some_name 1', 'some_name 1', 'some_name 1']"
                :block_place="'down'"
        ></middle-down-block>


        <!--    <dynamic-selected-region-->
        <!--            :date="date"-->
        <!--            :params="params"-->
        <!--            :interval="interval"-->
        <!--            :category="category"-->
        <!--            :tnved_list="tnved_list"-->
        <!--    ></dynamic-selected-region>-->
        <!--    <dynamic-tnved-by-selected-region-->
        <!--            :date="date"-->
        <!--            :params="params"-->
        <!--            :interval="interval"-->
        <!--            :category="category"-->
        <!--            :tnved_list="tnved_list"-->
        <!--    ></dynamic-tnved-by-selected-region>-->
        <!--    <dynamic-country-by-selected-region-->
        <!--            :date="date"-->
        <!--            :params="params"-->
        <!--            :interval="interval"-->
        <!--            :category="category"-->
        <!--            :tnved_list="tnved_list"-->
        <!--    ></dynamic-country-by-selected-region>-->
    </div>
</template>

<script>
    export default {
        name: "ReportByRegion",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        components: {
            TopBlock: () => import('./report_blocks/TopBlock'),
            MiddleDownBlock: () => import('./report_blocks/MiddleDownBlock')            // DynamicSelectedRegion: () => import('./report_region/DynamicSelectedRegion'),
            // DynamicTnvedBySelectedRegion: () => import('./report_region/DynamicTnvedBySelectedRegion'),
            // DynamicCountryBySelectedRegion: () => import('./report_region/DynamicCountryBySelectedRegion'),
        }
    }
</script>

<style scoped>

</style>