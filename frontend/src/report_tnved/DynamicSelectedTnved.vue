<template>
  <div class="dynamic-selected-tnved">
    <h1>Динамика выбранных кодов ТНВЭД</h1>
    <highcharts class="chart" :options="chartOptions" :deepCopyOnUpdate="true" :updateArgs="updateArgs"></highcharts>
    <h1>Динамика выбранных кодов ТНВЭД</h1>
    <div class="d-table">
      <div class="d-tr" v-for="(label, index) in table_data.labels" :key="index">
          <div class="d-td">{{label}}</div>
          <div class="d-td">{{table_data.weight[0][index]}}</div>
          <div class="d-td">{{table_data.weight[1][index]}}</div>
          <div class="d-td">{{table_data.stoim[0][index]}}</div>
          <div class="d-td">{{table_data.stoim[1][index]}}</div>
      </div>
    </div>
    <br>
    <h5>суммарный импорт по выбранным кодам</h5>
    <div class="d-table" style="width: 50% !important;">
      <div class="d-tr">
        <div class="d-td">{{imp_sum_table.stoim}}</div>
        <div class="d-td">$</div>
      </div>
      <div class="d-tr">
        <div class="d-td">{{imp_sum_table.weight}}</div>
        <div class="d-td">т</div>
      </div>
    </div>

    <h5>суммарный экспорт по выбранным кодам</h5>
    <div class="d-table" style="width: 50% !important;">
      <div class="d-tr">
        <div class="d-td">{{exp_sum_table.stoim}}</div>
        <div class="d-td">$</div>
      </div>
      <div class="d-tr">
        <div class="d-td">{{exp_sum_table.weight}}</div>
        <div class="d-td">т</div>
      </div>
    </div>
  </div>
</template>

<script>
    import Vue from "vue";
    import HighchartsVue from "highcharts-vue";
    import Highcharts from "highcharts/highcharts";
    import dataModule from "highcharts/modules/data";
    import {HTTP} from '../http-common'
    import qs from 'qs'
    import moment from 'moment'

    import threeDimensionsHC from "highcharts/highcharts-3d";
    dataModule(Highcharts);

    threeDimensionsHC(Highcharts);
    Vue.use(HighchartsVue);

    export default {
        name: "DynamicSelectedTnved",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        data () {
            return {
                imp_sum_table: {
                    stoim: null,
                    weight: null
                },
                exp_sum_table: {
                    stoim: null,
                    weight: null
                },
                table_data: {
                    labels: [],
                    stoim: [[], []],
                    weight: [[], []],
                },
                updateArgs: [true, true, true],
                chartOptions: {
                  xAxis: {
                      categories: null
                  },
                  title: {
                    text: 'Sin chart'
                  },
                  series: []
                }
            }
        },
        methods: {
            recount() {
                HTTP.get('statistic/tnved_dynamics/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(1, 'year').format('YYYY-MM'),
                        'interval': this.interval,
                        'params': this.params,
                        'category': this.category,
                        'tnved_list': this.tnved_list,
                        'tnved_list_length': this.tnved_list.length
                    },
                    paramsSerializer: params => {
                      return qs.stringify(params)
                    }
                })
                    .then(response => {
                        this.table_data.labels = response.data.labels;
                        this.table_data.stoim = response.data.table.stoim;
                        this.table_data.weight = response.data.table.weight;
                        this.chartOptions.series = response.data.chartdata;
                        this.chartOptions.xAxis.categories = response.data.labels;
                        this.imp_sum_table.stoim = response.data.imp_sum_table.stoim;
                        this.imp_sum_table.weight = response.data.imp_sum_table.weight;
                        this.exp_sum_table.stoim = response.data.exp_sum_table.stoim;
                        this.exp_sum_table.weight = response.data.exp_sum_table.weight;
                    })
                    .catch(error => {
                        window.console.log(error)
                    })
            },
        },
        created() {
            this.$eventHub.$on('recount', this.recount)
        },
        beforeDestroy(){
            this.$eventHub.$off('recount');
        },
        mounted() {
            // this.recount()
        }
    }
</script>

<style scoped>

</style>