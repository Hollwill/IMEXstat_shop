<template>
  <div class="Base-market-summary">
    <market-summary :date="date" ref="marketSummary"></market-summary>
    <exp-imp-dynamics :date="date"
                      :params="params"
                      :interval="interval"
                      ref="expImpDynamics"
    ></exp-imp-dynamics>
    <turnover-structure
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            ref="turnoverStructure"
    ></turnover-structure>
    <country-statistic
            :date="date"
            :params="params"
            :interval="interval"
            :category="category"
            ref="CountryStatistic"
    ></country-statistic>
  </div>
</template>
<script>
    export default {
        name: "BaseMarketSummary",
        props: ['date', 'params', 'interval', 'category'],
        components: {
          MarketSummary: () => import('./market_summary/MarketSummary'),
          ExpImpDynamics: () => import('./market_summary/ExpImpDynamics'),
          TurnoverStructure: () => import('./market_summary/TurnoverStructure'),
          CountryStatistic: () => import('./market_summary/CountryStatistic')
        },
    }
</script>


<style scoped>

</style>