<template>
  <div class="report-by-tnved">
    <dynamic-selected-tnved
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            :tnved_list="tnved_list"
    ></dynamic-selected-tnved>
  </div>
</template>

<script>
    export default {
        name: "ReportByTnved",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        components: {
            DynamicSelectedTnved: () => import('./report_tnved/DynamicSelectedTnved')
        }
    }
</script>

<style scoped>

</style>