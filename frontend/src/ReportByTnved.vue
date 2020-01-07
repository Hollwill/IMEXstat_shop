<template>
  <div class="report-by-tnved">
    <dynamic-selected-tnved
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-selected-tnved>
    <dynamic-country-by-selected-tnved
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-country-by-selected-tnved>
    <dynamic-region-by-selected-tnved
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-region-by-selected-tnved>
  </div>
</template>

<script>
    export default {
        name: "ReportByTnved",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        components: {
            DynamicSelectedTnved: () => import('./report_tnved/DynamicSelectedTnved'),
            DynamicCountryBySelectedTnved: () => import('./report_tnved/DynamicCountryBySelectedTnved'),
            DynamicRegionBySelectedTnved: () => import('./report_tnved/DynamicRegionBySelectedTnved'),
        }
    }
</script>

<style scoped>

</style>