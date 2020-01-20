<template>
  <div class="report-by-region">
    <dynamic-selected-region
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-selected-region>
    <dynamic-tnved-by-selected-region
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-tnved-by-selected-region>
    <dynamic-country-by-selected-region
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-country-by-selected-region>
  </div>
</template>

<script>
    export default {
        name: "ReportByRegion",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        components: {
            DynamicSelectedRegion: () => import('./report_region/DynamicSelectedRegion'),
            DynamicTnvedBySelectedRegion: () => import('./report_region/DynamicTnvedBySelectedRegion'),
            DynamicCountryBySelectedRegion: () => import('./report_region/DynamicCountryBySelectedRegion'),
        }
    }
</script>

<style scoped>

</style>