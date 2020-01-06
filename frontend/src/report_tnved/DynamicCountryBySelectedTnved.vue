<template>
  <div class="dynamic-selected-tnved">
    <h1>Вовлеченность стран в выбранные кода ТНВЭД</h1>
    <highcharts class="chart" :options="chartOptions" :deepCopyOnUpdate="true" :updateArgs="updateArgs"></highcharts>
    <h1>Динамика выбранных кодов ТНВЭД</h1>
    <div class="d-table">
      <div class="d-tr" v-for="(item, index) in dynamicTable" :key="index">
          <div class="d-td div-as-button" @click="countryDataRequest(item.short_label)">{{item.label}}</div>
          <div class="d-td">{{item.weight}}</div>
          <div class="d-td">{{item.dynamicWeight}}</div>
          <div class="d-td">{{item.stoim}}</div>
          <div class="d-td">{{item.dynamicStoim}}</div>
      </div>
    </div>
<!--    <h1>Сегментный бублик</h1>-->
<!--    <highcharts class="chart" :options="segmentPieOptions" :updateArgs="updateArgs"></highcharts>-->
<!--    <h1>Доля первого кода в вышестоящем</h1>-->
<!--    <highcharts class="chart" :options="firstTnvedPartsPieOptions" :updateArgs="updateArgs"></highcharts>-->
  </div>
</template>

<script>
    import Vue from "vue";
    import HighchartsVue from "highcharts-vue";
    import Highcharts from "highcharts/highcharts";
    import dataModule from "highcharts/modules/data";
    import drilldown from "highcharts/modules/drilldown";
    import {HTTP} from '../http-common'
    import qs from 'qs'
    import moment from 'moment'

    import threeDimensionsHC from "highcharts/highcharts-3d";
    dataModule(Highcharts);
    drilldown(Highcharts);

    threeDimensionsHC(Highcharts);
    Vue.use(HighchartsVue);

    export default {
        name: "DynamicCountryBySelectedTnved",
        props: ['date', 'params', 'interval', 'category', 'tnved_list'],
        data () {
            return {
                country_data: [],
                date_labels: [],
                updateArgs: [true, true, true],
                chartOptions: {
                  xAxis: {
                      categories: null
                  },
                  series: [
                      {
                          name: 'Импорт',
                          data: []
                      },
                      {
                          name: 'Экспорт',
                          data: []
                      },

                  ]
                }
            }
        },
        computed: {
            dynamicTable: function() {
                let value = [];
                let weight_arr = [];
                let stoim_arr = [];

                for (let data of this.country_data) {
                    let item = (this.category === 'ИМ') ? data.imp : data.exp
                    let weight = item.weight
                    let stoim = item.cost

                    weight_arr.push(weight)
                    stoim_arr.push(stoim)

                    value.push(
                        {
                            short_label: data.country_short,
                            label: data.country,
                            weight: weight,
                            stoim: stoim,
                        });
                }
                weight_arr = this.dynamics_array(weight_arr);
                stoim_arr = this.dynamics_array(stoim_arr);
                for (let i = 0; i < value.length; i++) {
                    value[i].dynamicWeight = weight_arr[i];
                    value[i].dynamicStoim = stoim_arr[i];
                }
                return value
            },
        },
        methods: {
            // updateFirstTnvedPartsPie(val) {
            //     this.firstTnvedPartsPieOptions.series[0].data = [];
            //     for (let i of val) {
            //         let data;
            //         if (this.category === 'ИМ') {
            //               data = (this.params === 'stoim') ? i.imp.stoim : i.imp.weight
            //           } else {
            //               data = (this.params === 'netto') ? i.exp.stoim : i.exp.weight
            //           }
            //         this.firstTnvedPartsPieOptions.series[0].data.push({
            //             name: i.tnved,
            //             y: data
            //         })
            //     }
            //
            // },
            // segmentPieData(val) {
            //
            //     this.segmentPieOptions.series[0].data = [
            //         {
            //             name: 'Импорт',
            //             y: (this.params === 'stoim') ? this.imp_sum_table.stoim : this.imp_sum_table.weight,
            //             drilldown: 'imp',
            //             color: '#0600FF'
            //         },
            //         {
            //             name: 'Экспорт',
            //             y: (this.params === 'stoim') ? this.exp_sum_table.stoim : this.exp_sum_table.weight,
            //             drilldown: 'exp',
            //             color: '#EBFF00'
            //         }
            //     ];
            //     this.segmentPieOptions.drilldown.series[0].data = [];
            //     this.segmentPieOptions.drilldown.series[1].data = [];
            //
            //     for (let i = 0; i < val.length; i++) {
            //         let imp_data = (this.params === 'stoim') ? val[i].imp.stoim : val[i].imp.weight
            //         let exp_data = (this.params === 'stoim') ? val[i].exp.stoim : val[i].exp.weight
            //         this.segmentPieOptions.drilldown.series[0].data.push([val[i].tnved, imp_data.reduce((a, b) => a + b, 0)])
            //         this.segmentPieOptions.drilldown.series[1].data.push([val[i].tnved, exp_data.reduce((a, b) => a + b, 0)])
            //     }
            //
            // },
            // sumTables(val) {
            //     let imp = {stoim: 0, weight: 0};
            //     let exp = {stoim: 0, weight: 0};
            //     for (let item of val) {
            //         imp.stoim += item.imp.stoim.reduce((a, b) => a + b, 0);
            //         imp.weight += item.imp.weight.reduce((a, b) => a + b, 0);
            //         exp.stoim += item.exp.stoim.reduce((a, b) => a + b, 0);
            //         exp.weight += item.exp.weight.reduce((a, b) => a + b, 0);
            //     }
            //     this.imp_sum_table = imp;
            //     this.exp_sum_table = exp;
            // },
            dynamics_array(arr) {
                let new_arr = [0];
                for (let i = 0; i < arr.length; i++) {
                    let val = (arr[i] === 0) ? 0 : ((arr[i+1] - arr[i])/arr[i] * 100).toFixed(2);
                    new_arr.push(val)
                }
                return new_arr
            },
            // updateLineChart(val) {
            //     this.chartOptions.series = [];
            //       for (let tnved_data of val) {
            //           let data;
            //           if (this.category === 'ИМ') {
            //               data = (this.params === 'stoim') ? tnved_data.imp.stoim : tnved_data.imp.weight
            //           } else {
            //               data = (this.params === 'netto') ? tnved_data.exp.stoim : tnved_data.exp.weight
            //           }
            //           this.chartOptions.series.push({name: tnved_data.tnved, data: data})
            //       }
            //       this.chartOptions.xAxis.categories = this.date_labels
            // },
            recount() {
                HTTP.get('statistic/country_report/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(3, 'year').format('YYYY-MM'),
                        'interval': this.interval,
                        'tnved_list': this.tnved_list,
                        'tnved_list_length': this.tnved_list.length
                    },
                    paramsSerializer: params => {
                      return qs.stringify(params)
                    }
                })
                    .then(response => {
                        this.country_data = response.data
                    })
            },
            countryDataRequest(country) {
                HTTP.get('statistic/detailed_country_report/', {
                    params: {
                        'date_to': (this.date.from != null && this.date.to != null) ? this.date.to  : moment(new Date()).format('YYYY-MM'),
                        'date_from': (this.date.from != null && this.date.to != null) ? this.date.from : moment(new Date()).subtract(3, 'year').format('YYYY-MM'),
                        'interval': this.interval,
                        'tnved_list': this.tnved_list,
                        'tnved_list_length': this.tnved_list.length,
                        'country': country
                    },
                    paramsSerializer: params => {
                      return qs.stringify(params)
                    }
                })
                    .then(response => {
                        this.chartOptions.series[0].data = (this.params === 'stoim') ? response.data.data.imp.cost : response.data.data.imp.weight;
                        this.chartOptions.series[1].data = (this.params === 'stoim') ? response.data.data.exp.cost : response.data.data.exp.weight;
                        this.chartOptions.xAxis.categories = response.data.labels
                    })
            }
        },
        created() {
            this.$eventHub.$on('recount', this.recount)
        },
        beforeDestroy(){
            this.$eventHub.$off('recount');
        },
    }
</script>

<style scoped>

</style>

