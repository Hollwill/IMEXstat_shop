<template>
  <div class="report-by-tnved">
    <dynamic-selected-country
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-selected-country>
    <dynamic-tnved-by-selected-country
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-tnved-by-selected-country>
    <dynamic-region-by-selected-country
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-region-by-selected-country>
  </div>
</template>

<script>
    export default {
        name: "ReportByTnved",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        components: {
            DynamicSelectedCountry: () => import('./report_country/DynamicSelectedCountry'),
            DynamicTnvedBySelectedCountry: () => import('./report_country/DynamicTnvedBySelectedCountry'),
            DynamicRegionBySelectedCountry: () => import('./report_country/DynamicRegionBySelectedCountry'),
        }
    }
</script>

<style scoped>

</style>